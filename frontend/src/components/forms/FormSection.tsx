import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, Wand2, Send, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '../ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { apiService } from '../../services/api';
import ChildForm from './child_form';
import CategoryForm from './category_form';
import SummaryForm from './summary_form';
import type { ChildData } from './child_form';
import type { CategoryData } from './category_form';
import type { SummaryData } from './summary_form';

interface FormData {
  child: ChildData;
  category: CategoryData;
  summary: SummaryData;
  additional_fields?: Record<string, any>;
}

interface FormErrors {
  child?: Partial<Record<keyof ChildData, string>>;
  category?: Partial<Record<keyof CategoryData, string>>;
  summary?: Partial<Record<keyof SummaryData, string>>;
}

interface FormSectionProps {
  sessionId: string;
}

const FormSection: React.FC<FormSectionProps> = ({ sessionId }) => {
  const [activeTab, setActiveTab] = useState<'child' | 'category' | 'summary'>('child');
  const [formData, setFormData] = useState<FormData>({
    child: { firstName: '' },
    category: {},
    summary: { callSummary: '', keepConfidential: true },
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isAutoFilling, setIsAutoFilling] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [submitMessage, setSubmitMessage] = useState('');

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {
      child: {},
      summary: {},
    };
    if (!formData.child.firstName?.trim()) {
      newErrors.child!.firstName = 'First Name is required';
    }
    if (!formData.summary.callSummary?.trim()) {
      newErrors.summary!.callSummary = 'Contact Summary is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors.child || {}).length === 0 && Object.keys(newErrors.summary || {}).length === 0;
  };

  const handleChildChange = (field: keyof ChildData, value: any) => {
    setFormData(prev => ({
      ...prev,
      child: { ...prev.child, [field]: value },
    }));
    setErrors(prev => ({
      ...prev,
      child: { ...prev.child, [field]: undefined },
    }));
    setSubmitStatus('idle');
  };

  const handleCategoryChange = (field: keyof CategoryData, value: any) => {
    setFormData(prev => ({
      ...prev,
      category: { ...prev.category, [field]: value },
    }));
    setSubmitStatus('idle');
  };

  const handleSummaryChange = (field: keyof SummaryData, value: any) => {
    setFormData(prev => ({
      ...prev,
      summary: { ...prev.summary, [field]: value },
    }));
    setErrors(prev => ({
      ...prev,
      summary: { ...prev.summary, [field]: undefined },
    }));
    setSubmitStatus('idle');
  };

  // Clean and validate backend data
  const cleanChildData = (data: any): Partial<ChildData> => {
    const cleaned: any = {};
    
    // Valid enum values
    const validGenders = ['Male', 'Female', 'Other', 'Unknown'];
    const validParishes = ['Kingston', 'St. Andrew', 'St. Thomas', 'St. Catherine', 'Clarendon', 'Manchester', 'St. Elizabeth', 'Westmoreland', 'Hanover', 'St. James', 'Trelawny', 'St. Ann', 'St. Mary', 'Portland', 'Unknown'];
    const validLivingSituations = ['Alternative care', 'Group residential facility', 'Homeless or marginally housed', 'In detention', 'Living independently', 'With parent(s)', 'With relatives', 'Other', 'Unknown'];
    const validRegions = ['Unknown', 'Cities', 'Rural areas', 'Town & semi-dense areas'];

    // Clean each field
    Object.entries(data).forEach(([key, value]) => {
      if (value === null || value === undefined) return;
      
      const strValue = String(value).trim();
      
      // Skip invalid strings like "-null" or strings with explanations
      if (strValue.startsWith('-') || strValue.includes('(') || strValue.toLowerCase().includes('null')) {
        console.log(`Skipping invalid value for ${key}:`, strValue);
        return;
      }

      switch (key) {
        case 'gender':
          if (validGenders.includes(strValue)) cleaned[key] = strValue;
          break;
        case 'parish':
          if (validParishes.includes(strValue)) cleaned[key] = strValue;
          break;
        case 'livingSituation':
          if (validLivingSituations.includes(strValue)) cleaned[key] = strValue;
          break;
        case 'region':
          if (validRegions.includes(strValue)) cleaned[key] = strValue;
          break;
        case 'phone1':
        case 'phone2':
          // Extract just the phone number, remove any text in parentheses
          const phoneMatch = strValue.match(/[\d-]+/);
          if (phoneMatch) cleaned[key] = phoneMatch[0];
          break;
        case 'age':
          // Only accept valid age formats
          if (['Unborn', '>25', 'Unknown'].includes(strValue) || /^\d{2}$/.test(strValue)) {
            cleaned[key] = strValue;
          }
          break;
        case 'vulnerableGroups':
          if (Array.isArray(value)) {
            cleaned[key] = value.filter(v => v && typeof v === 'string' && v !== 'null');
          }
          break;
        default:
          // For text fields, just use the string value
          if (typeof value === 'string' && strValue) {
            cleaned[key] = strValue;
          }
      }
    });

    console.log('Cleaned child data:', cleaned);
    return cleaned;
  };

  const handleAutoFill = async () => {
    setIsAutoFilling(true);
    setSubmitStatus('idle');
    setSubmitMessage('');
    
    try {
      console.log('🔍 Starting auto-fill for session:', sessionId);
      const response = await apiService.autoFill(sessionId);
      console.log('📥 Raw backend response:', JSON.stringify(response, null, 2));

      // Clean and validate the data
      const cleanedChild = cleanChildData(response.child || {});
      console.log('✅ Cleaned child data:', cleanedChild);

      // Filter category data (arrays only)
      const cleanedCategory: any = {};
      if (response.category) {
        Object.entries(response.category).forEach(([key, value]) => {
          if (Array.isArray(value) && value.length > 0) {
            cleanedCategory[key] = value;
          }
        });
      }
      console.log('✅ Cleaned category data:', cleanedCategory);

      // Filter summary data (remove nulls)
      const cleanedSummary: any = {};
      if (response.summary) {
        Object.entries(response.summary).forEach(([key, value]) => {
          if (value !== null && value !== undefined) {
            cleanedSummary[key] = value;
          }
        });
      }
      console.log('✅ Cleaned summary data:', cleanedSummary);

      // Update state
      setFormData(prev => {
        const updated = {
          ...prev,
          child: { ...prev.child, ...cleanedChild },
          category: { ...prev.category, ...cleanedCategory },
          summary: { ...prev.summary, ...cleanedSummary },
          additional_fields: {
            ...prev.additional_fields,
            ...(response.metadata || {}),
          },
        };
        console.log('🎯 Final updated form data:', updated);
        return updated;
      });

      setErrors({ child: {}, category: {}, summary: {} });
      
      // Show success message
      setSubmitStatus('success');
      setSubmitMessage(`Form auto-filled! Applied ${Object.keys(cleanedChild).length} child fields, ${Object.keys(cleanedCategory).length} categories.`);
      setTimeout(() => {
        setSubmitStatus('idle');
        setSubmitMessage('');
      }, 5000);

    } catch (error) {
      console.error('❌ Auto-fill error:', error);
      setSubmitStatus('error');
      setSubmitMessage(
        error instanceof Error 
          ? `Failed to auto-fill: ${error.message}` 
          : 'Failed to auto-fill form. Please try again.'
      );
    } finally {
      setIsAutoFilling(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) {
      return;
    }
    setIsSubmitting(true);
    setSubmitStatus('idle');
    try {
      const submissionData = {
        child: formData.child,
        category: formData.category,
        summary: formData.summary,
        metadata: formData.additional_fields || {},
      };
      console.log('Submitting form data:', submissionData);
      const response = await apiService.submitForm(sessionId, submissionData as any);
      
      if (response.success) {
        setSubmitStatus('success');
        setSubmitMessage(
          response.caseId
            ? `Form submitted successfully! Case ID: ${response.caseId}`
            : 'Form submitted successfully!'
        );
        setTimeout(() => {
          setFormData({
            child: { firstName: '' },
            category: {},
            summary: { callSummary: '', keepConfidential: true },
          });
          setSubmitStatus('idle');
          setSubmitMessage('');
        }, 3000);
      }
    } catch (error) {
      console.error('Submit error:', error);
      setSubmitStatus('error');
      setSubmitMessage(
        error instanceof Error
          ? `Failed to submit: ${error.message}`
          : 'Failed to submit form. Please try again.'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const isFormValid = !!formData.child.firstName && !!formData.summary.callSummary;

  return (
    <Card className="h-full flex flex-col">
      <CardHeader className="pb-3">
        <CardTitle className="text-xl font-semibold flex items-center gap-2">
          <FileText className="w-6 h-6 text-primary" />
          Form Sections
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 p-4 pt-0 overflow-auto">
        {/* Tab Navigation */}
        <div className="flex gap-2 mb-4">
          <Button 
            type="button" 
            variant={activeTab === 'child' ? 'default' : 'outline'} 
            onClick={() => setActiveTab('child')}
          >
            Child
          </Button>
          <Button 
            type="button" 
            variant={activeTab === 'category' ? 'default' : 'outline'} 
            onClick={() => setActiveTab('category')}
          >
            Category
          </Button>
          <Button 
            type="button" 
            variant={activeTab === 'summary' ? 'default' : 'outline'} 
            onClick={() => setActiveTab('summary')}
          >
            Summary
          </Button>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Auto-fill Button */}
          <div className="flex justify-end">
            <Button
              type="button"
              onClick={handleAutoFill}
              disabled={isAutoFilling || isSubmitting}
              variant="outline"
              className="flex items-center gap-2"
            >
              {isAutoFilling ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Wand2 className="w-4 h-4" />
              )}
              {isAutoFilling ? 'Auto Filling...' : 'Auto Fill'}
            </Button>
          </div>

          {/* Tab Panels */}
          {activeTab === 'child' && (
            <div className="space-y-2">
              <h3 className="text-lg font-medium">Child Details</h3>
              <ChildForm
                data={formData.child}
                onChange={handleChildChange}
                errors={errors.child || {}}
              />
            </div>
          )}
          {activeTab === 'category' && (
            <div className="space-y-2">
              <h3 className="text-lg font-medium">Categories / Issues</h3>
              <CategoryForm
                data={formData.category}
                onChange={handleCategoryChange}
              />
            </div>
          )}
          {activeTab === 'summary' && (
            <div className="space-y-2">
              <h3 className="text-lg font-medium">Summary Info</h3>
              <SummaryForm
                data={formData.summary}
                onChange={handleSummaryChange}
                errors={errors.summary || {}}
              />
            </div>
          )}

          {/* Submit Status */}
          {submitStatus !== 'idle' && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`p-3 rounded-md flex items-center gap-2 ${
                submitStatus === 'success'
                  ? 'bg-green-500/10 text-green-500 border border-green-500/20'
                  : 'bg-destructive/10 text-destructive border border-destructive/20'
              }`}
            >
              {submitStatus === 'success' ? (
                <CheckCircle className="w-4 h-4" />
              ) : (
                <AlertCircle className="w-4 h-4" />
              )}
              <p className="text-sm">{submitMessage}</p>
            </motion.div>
          )}

          {/* Submit Button */}
          <Button
            type="submit"
            disabled={!isFormValid || isSubmitting || isAutoFilling}
            className="w-full flex items-center gap-2"
          >
            {isSubmitting ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
            {isSubmitting ? 'Submitting...' : 'Submit Form'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};

export default FormSection;