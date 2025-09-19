import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, Wand2, Send, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { apiService, FormData } from '../services/api';

interface FormSectionProps {
  sessionId: string;
}

interface FormErrors {
  name?: string;
  email?: string;
  phone?: string;
  address?: string;
  notes?: string;
}

const FormSection: React.FC<FormSectionProps> = ({ sessionId }) => {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    phone: '',
    address: '',
    notes: '',
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [isAutoFilling, setIsAutoFilling] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [submitMessage, setSubmitMessage] = useState('');

  // Validation functions
  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePhone = (phone: string): boolean => {
    const phoneRegex = /^[+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(phone.replace(/\s|-|\(|\)/g, ''));
  };

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email';
    }

    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone is required';
    } else if (!validatePhone(formData.phone)) {
      newErrors.phone = 'Please enter a valid phone number';
    }

    if (!formData.address.trim()) {
      newErrors.address = 'Address is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));

    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: undefined,
      }));
    }

    // Reset submit status when form is modified
    setSubmitStatus('idle');
  };

  const handleAutoFill = async () => {
    setIsAutoFilling(true);
    try {
      const response = await apiService.autoFill(sessionId);
      
      // Create form data object from response
      const autoFilledData: Partial<FormData> = {};
      if (response.name) autoFilledData.name = response.name;
      if (response.email) autoFilledData.email = response.email;
      if (response.phone) autoFilledData.phone = response.phone;
      if (response.address) autoFilledData.address = response.address;
      if (response.notes) autoFilledData.notes = response.notes;
      
      if (Object.keys(autoFilledData).length > 0) {
        setFormData(prev => ({
          ...prev,
          ...autoFilledData,
        }));
        
        // Clear any existing errors for auto-filled fields
        const clearedErrors: FormErrors = {};
        Object.keys(autoFilledData).forEach(key => {
          if (autoFilledData[key as keyof FormData]) {
            clearedErrors[key as keyof FormErrors] = undefined;
          }
        });
        setErrors(prev => ({
          ...prev,
          ...clearedErrors,
        }));
      }
    } catch (error) {
      console.error('Error auto-filling form:', error);
      setSubmitStatus('error');
      setSubmitMessage('Failed to auto-fill form. Please try again.');
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
      const response = await apiService.submitForm(sessionId, formData);
      
      if (response.success) {
        setSubmitStatus('success');
        setSubmitMessage(
          response.caseId 
            ? `Form submitted successfully! Case ID: ${response.caseId}`
            : 'Form submitted successfully!'
        );
        
        // Reset form after successful submission
        setTimeout(() => {
          setFormData({
            name: '',
            email: '',
            phone: '',
            address: '',
            notes: '',
          });
          setSubmitStatus('idle');
          setSubmitMessage('');
        }, 3000);
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      setSubmitStatus('error');
      setSubmitMessage('Failed to submit form. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const isFormValid = formData.name && formData.email && formData.phone && formData.address;

  return (
    <Card className="h-full flex flex-col">
      <CardHeader className="pb-3">
        <CardTitle className="text-xl font-semibold flex items-center gap-2">
          <FileText className="w-6 h-6 text-primary" />
          Contact Information
        </CardTitle>
      </CardHeader>
      
      <CardContent className="flex-1 p-4 pt-0">
        <form onSubmit={handleSubmit} className="space-y-4">
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
              Auto Fill
            </Button>
          </div>

          {/* Form Fields */}
          <div className="grid gap-4">
            {/* Name Field */}
            <div className="space-y-2">
              <Label htmlFor="name">Full Name *</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                placeholder="Enter your full name"
                className={errors.name ? 'border-destructive' : ''}
              />
              {errors.name && (
                <p className="text-xs text-destructive flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" />
                  {errors.name}
                </p>
              )}
            </div>

            {/* Email Field */}
            <div className="space-y-2">
              <Label htmlFor="email">Email Address *</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                placeholder="Enter your email address"
                className={errors.email ? 'border-destructive' : ''}
              />
              {errors.email && (
                <p className="text-xs text-destructive flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" />
                  {errors.email}
                </p>
              )}
            </div>

            {/* Phone Field */}
            <div className="space-y-2">
              <Label htmlFor="phone">Phone Number *</Label>
              <Input
                id="phone"
                type="tel"
                value={formData.phone}
                onChange={(e) => handleInputChange('phone', e.target.value)}
                placeholder="Enter your phone number"
                className={errors.phone ? 'border-destructive' : ''}
              />
              {errors.phone && (
                <p className="text-xs text-destructive flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" />
                  {errors.phone}
                </p>
              )}
            </div>

            {/* Address Field */}
            <div className="space-y-2">
              <Label htmlFor="address">Address *</Label>
              <Textarea
                id="address"
                value={formData.address}
                onChange={(e) => handleInputChange('address', e.target.value)}
                placeholder="Enter your full address"
                className={`min-h-[80px] ${errors.address ? 'border-destructive' : ''}`}
              />
              {errors.address && (
                <p className="text-xs text-destructive flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" />
                  {errors.address}
                </p>
              )}
            </div>

            {/* Notes Field */}
            <div className="space-y-2">
              <Label htmlFor="notes">Additional Notes</Label>
              <Textarea
                id="notes"
                value={formData.notes}
                onChange={(e) => handleInputChange('notes', e.target.value)}
                placeholder="Any additional information you'd like to share..."
                className="min-h-[100px]"
              />
            </div>
          </div>

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
