import React from 'react';
import { Textarea } from '../ui/textarea';
import { Select } from '../ui/select';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Checkbox } from '../ui/checkbox';

export interface SummaryData {
  callSummary: string;
  summaryAccuracy?: 'Unknown' | 'Very accurate' | 'Somewhat accurate' | 'Not accurate';
  summaryFeedback?: string;
  locationOfIssue?: 'Unknown' | 'Home (own)' | 'Home (other)' | 'Educational Establishment' | 'Institution' | 'Online' | 'Public place' | 'Other';
  otherLocation?: string;
  actionTaken?: 'Direct interventions by the child helpline' | 'Provision of information about SafeSpot' | 'Recommendations of resources' | 'Recommendation that young person contact SafeSpot' | 'Referrals to child protection agencies' | 'Referrals to law enforcement agencies' | 'Referrals to general healthcare professionals' | 'Referrals to mental health services' | 'Referrals to other organisations' | 'Referrals to school counsellors' | 'Reports to Child Sexual Abuse Material';
  outcomeOfContact?: 'Resolved' | 'Follow up by next shift' | 'Follow up with external entity';
  howDidYouKnowAboutOurLine?: 'AI' | 'Advertisement' | 'Social media' | 'SMS/Text Message' | 'Traditional Media' | 'Word of Mouth';
  repeatCaller?: boolean;
  keepConfidential: boolean;
  okForCaseWorkerToCall?: boolean;
  didTheChildFeelWeSolvedTheirProblem?: boolean;
  wouldTheChildRecommendUsToAFriend?: boolean;
  didYouDiscussRightsWithTheChild?: boolean;
}

interface SummaryFormProps {
  data: SummaryData;
  onChange: (field: keyof SummaryData, value: any) => void;
  errors: Partial<Record<keyof SummaryData, string>>;
}

const SummaryForm: React.FC<SummaryFormProps> = ({ data, onChange, errors }) => {
  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="callSummary">Contact Summary *</Label>
        <Textarea
          id="callSummary"
          value={data.callSummary}
          onChange={(e) => onChange('callSummary', e.target.value)}
          placeholder="Enter contact summary"
          className={errors.callSummary ? 'border-destructive' : ''}
        />
        {errors.callSummary && <p className="text-xs text-destructive">{errors.callSummary}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="summaryAccuracy">Summary Accuracy</Label>
        <Select
          id="summaryAccuracy"
          value={data.summaryAccuracy || ''}
          onChange={(e) => onChange('summaryAccuracy', e.target.value)}
        >
          <option value="">Select accuracy</option>
          <option value="Unknown">Unknown</option>
          <option value="Very accurate">Very accurate</option>
          <option value="Somewhat accurate">Somewhat accurate</option>
          <option value="Not accurate">Not accurate</option>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="summaryFeedback">Summary Feedback</Label>
        <Textarea
          id="summaryFeedback"
          value={data.summaryFeedback || ''}
          onChange={(e) => onChange('summaryFeedback', e.target.value)}
          placeholder="Enter summary feedback"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="locationOfIssue">Location of Issue</Label>
        <Select
          id="locationOfIssue"
          value={data.locationOfIssue || ''}
          onChange={(e) => onChange('locationOfIssue', e.target.value)}
        >
          <option value="">Select location</option>
          <option value="Unknown">Unknown</option>
          <option value="Home (own)">Home (own)</option>
          <option value="Home (other)">Home (other)</option>
          <option value="Educational Establishment">Educational Establishment</option>
          <option value="Institution">Institution</option>
          <option value="Online">Online</option>
          <option value="Public place">Public place</option>
          <option value="Other">Other</option>
        </Select>
      </div>

      {data.locationOfIssue === 'Other' && (
        <div className="space-y-2">
          <Label htmlFor="otherLocation">Other Location</Label>
          <Input
            id="otherLocation"
            value={data.otherLocation || ''}
            onChange={(e) => onChange('otherLocation', e.target.value)}
            placeholder="Specify other location"
          />
        </div>
      )}

      <div className="space-y-2">
        <Label htmlFor="actionTaken">Action Taken</Label>
        <Select
          id="actionTaken"
          value={data.actionTaken || ''}
          onChange={(e) => onChange('actionTaken', e.target.value)}
        >
          <option value="">Select action</option>
          <option value="Direct interventions by the child helpline">Direct interventions by the child helpline</option>
          <option value="Provision of information about SafeSpot">Provision of information about SafeSpot</option>
          <option value="Recommendations of resources">Recommendations of resources</option>
          <option value="Recommendation that young person contact SafeSpot">Recommendation that young person contact SafeSpot</option>
          <option value="Referrals to child protection agencies">Referrals to child protection agencies</option>
          <option value="Referrals to law enforcement agencies">Referrals to law enforcement agencies</option>
          <option value="Referrals to general healthcare professionals">Referrals to general healthcare professionals</option>
          <option value="Referrals to mental health services">Referrals to mental health services</option>
          <option value="Referrals to other organisations">Referrals to other organisations</option>
          <option value="Referrals to school counsellors">Referrals to school counsellors</option>
          <option value="Reports to Child Sexual Abuse Material">Reports to Child Sexual Abuse Material</option>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="outcomeOfContact">Outcome of Contact</Label>
        <Select
          id="outcomeOfContact"
          value={data.outcomeOfContact || ''}
          onChange={(e) => onChange('outcomeOfContact', e.target.value)}
        >
          <option value="">Select outcome</option>
          <option value="Resolved">Resolved</option>
          <option value="Follow up by next shift">Follow up by next shift</option>
          <option value="Follow up with external entity">Follow up with external entity</option>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="howDidYouKnowAboutOurLine">How Did You Know About Our Line</Label>
        <Select
          id="howDidYouKnowAboutOurLine"
          value={data.howDidYouKnowAboutOurLine || ''}
          onChange={(e) => onChange('howDidYouKnowAboutOurLine', e.target.value)}
        >
          <option value="">Select source</option>
          <option value="AI">AI</option>
          <option value="Advertisement">Advertisement</option>
          <option value="Social media">Social media</option>
          <option value="SMS/Text Message">SMS/Text Message</option>
          <option value="Traditional Media">Traditional Media</option>
          <option value="Word of Mouth">Word of Mouth</option>
        </Select>
      </div>

      <div className="space-y-2">
        <div className="flex items-center space-x-2">
          <Checkbox
            id="repeatCaller"
            checked={data.repeatCaller || false}
            onCheckedChange={(checked) => onChange('repeatCaller', checked)}
          />
          <Label htmlFor="repeatCaller">Repeat Caller</Label>
        </div>

        <div className="flex items-center space-x-2">
          <Checkbox
            id="keepConfidential"
            checked={data.keepConfidential}
            onCheckedChange={(checked) => onChange('keepConfidential', checked)}
          />
          <Label htmlFor="keepConfidential">Keep Confidential</Label>
        </div>

        <div className="flex items-center space-x-2">
          <Checkbox
            id="okForCaseWorkerToCall"
            checked={data.okForCaseWorkerToCall || false}
            onCheckedChange={(checked) => onChange('okForCaseWorkerToCall', checked)}
          />
          <Label htmlFor="okForCaseWorkerToCall">OK for Case Worker to Call</Label>
        </div>

        <div className="flex items-center space-x-2">
          <Checkbox
            id="didTheChildFeelWeSolvedTheirProblem"
            checked={data.didTheChildFeelWeSolvedTheirProblem || false}
            onCheckedChange={(checked) => onChange('didTheChildFeelWeSolvedTheirProblem', checked)}
          />
          <Label htmlFor="didTheChildFeelWeSolvedTheirProblem">Did the Child Feel We Solved Their Problem</Label>
        </div>

        <div className="flex items-center space-x-2">
          <Checkbox
            id="wouldTheChildRecommendUsToAFriend"
            checked={data.wouldTheChildRecommendUsToAFriend || false}
            onCheckedChange={(checked) => onChange('wouldTheChildRecommendUsToAFriend', checked)}
          />
          <Label htmlFor="wouldTheChildRecommendUsToAFriend">Would the Child Recommend Us to a Friend</Label>
        </div>

        <div className="flex items-center space-x-2">
          <Checkbox
            id="didYouDiscussRightsWithTheChild"
            checked={data.didYouDiscussRightsWithTheChild || false}
            onCheckedChange={(checked) => onChange('didYouDiscussRightsWithTheChild', checked)}
          />
          <Label htmlFor="didYouDiscussRightsWithTheChild">Did You Discuss Rights With the Child</Label>
        </div>
      </div>
    </div>
  );
};

export default SummaryForm;