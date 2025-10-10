import React from 'react';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';
import { Select } from '../ui/select'; // Assuming Select is a custom component handling <select>
import { Label } from '../ui/label';
import { Checkbox } from '../ui/checkbox';

export interface ChildData {
  firstName: string;
  lastName?: string;
  gender?: 'Male' | 'Female' | 'Other' | 'Unknown';
  age?: 'Unborn' | '0' | '01' | '02' | '03' | '04' | '05' | '06' | '07' | '08' | '09' | '10' | '11' | '12' | '13' | '14' | '15' | '16' | '17' | '18' | '19' | '20' | '21' | '22' | '23' | '24' | '25' | '>25' | 'Unknown';
  streetAddress?: string;
  parish?: 'Kingston' | 'St. Andrew' | 'St. Thomas' | 'St. Catherine' | 'Clarendon' | 'Manchester' | 'St. Elizabeth' | 'Westmoreland' | 'Hanover' | 'St. James' | 'Trelawny' | 'St. Ann' | 'St. Mary' | 'Portland' | 'Unknown';
  phone1?: string;
  phone2?: string;
  nationality?: string;
  schoolName?: string;
  gradeLevel?: string;
  livingSituation?: 'Alternative care' | 'Group residential facility' | 'Homeless or marginally housed' | 'In detention' | 'Living independently' | 'With parent(s)' | 'With relatives' | 'Other' | 'Unknown';
  vulnerableGroups?: Array<'Child in conflict with the law' | 'Child living in conflict zone' | 'Child living in poverty' | 'Child member of an ethnic, racial or religious minority' | 'Child on the move (involuntarily)' | 'Child on the move (voluntarily)' | 'Child with disability' | 'LGBTQI+/SOGIESC child' | 'Out-of-school child' | 'Other'>;
  region?: 'Unknown' | 'Cities' | 'Rural areas' | 'Town & semi-dense areas';
}

interface ChildFormProps {
  data: ChildData;
  onChange: (field: keyof ChildData, value: any) => void;
  errors: Partial<Record<keyof ChildData, string>>;
}

const vulnerableOptions = [
  'Child in conflict with the law',
  'Child living in conflict zone',
  'Child living in poverty',
  'Child member of an ethnic, racial or religious minority',
  'Child on the move (involuntarily)',
  'Child on the move (voluntarily)',
  'Child with disability',
  'LGBTQI+/SOGIESC child',
  'Out-of-school child',
  'Other',
];

const ChildForm: React.FC<ChildFormProps> = ({ data, onChange, errors }) => {
  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="firstName">First Name *</Label>
        <Input
          id="firstName"
          value={data.firstName}
          onChange={(e) => onChange('firstName', e.target.value)}
          placeholder="Enter first name"
          className={errors.firstName ? 'border-destructive' : ''}
        />
        {errors.firstName && <p className="text-xs text-destructive">{errors.firstName}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="lastName">Last Name</Label>
        <Input
          id="lastName"
          value={data.lastName || ''}
          onChange={(e) => onChange('lastName', e.target.value)}
          placeholder="Enter last name"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="gender">Gender</Label>
        <Select
          id="gender"
          value={data.gender || ''}
          onChange={(e) => onChange('gender', e.target.value)}
        >
          <option value="">Select gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
          <option value="Unknown">Unknown</option>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="age">Age</Label>
        <Select
          id="age"
          value={data.age || ''}
          onChange={(e) => onChange('age', e.target.value)}
        >
          <option value="">Select age</option>
          <option value="Unborn">Unborn</option>
          {Array.from({ length: 26 }, (_, i) => i.toString().padStart(2, '0').slice(-2)).map(age => (
            <option key={age} value={age}>{age}</option>
          ))}
          <option value=">25">{'>25'}</option>
          <option value="Unknown">Unknown</option>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="streetAddress">Street Address</Label>
        <Textarea
          id="streetAddress"
          value={data.streetAddress || ''}
          onChange={(e) => onChange('streetAddress', e.target.value)}
          placeholder="Enter street address"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="parish">Parish</Label>
        <Select
          id="parish"
          value={data.parish || ''}
          onChange={(e) => onChange('parish', e.target.value)}
        >
          <option value="">Select parish</option>
          <option value="Kingston">Kingston</option>
          <option value="St. Andrew">St. Andrew</option>
          <option value="St. Thomas">St. Thomas</option>
          <option value="St. Catherine">St. Catherine</option>
          <option value="Clarendon">Clarendon</option>
          <option value="Manchester">Manchester</option>
          <option value="St. Elizabeth">St. Elizabeth</option>
          <option value="Westmoreland">Westmoreland</option>
          <option value="Hanover">Hanover</option>
          <option value="St. James">St. James</option>
          <option value="Trelawny">Trelawny</option>
          <option value="St. Ann">St. Ann</option>
          <option value="St. Mary">St. Mary</option>
          <option value="Portland">Portland</option>
          <option value="Unknown">Unknown</option>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="phone1">Phone #1</Label>
        <Input
          id="phone1"
          type="tel"
          value={data.phone1 || ''}
          onChange={(e) => onChange('phone1', e.target.value)}
          placeholder="Enter phone #1"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="phone2">Phone #2</Label>
        <Input
          id="phone2"
          type="tel"
          value={data.phone2 || ''}
          onChange={(e) => onChange('phone2', e.target.value)}
          placeholder="Enter phone #2"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="nationality">Nationality</Label>
        <Input
          id="nationality"
          value={data.nationality || ''}
          onChange={(e) => onChange('nationality', e.target.value)}
          placeholder="Enter nationality"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="schoolName">School Name</Label>
        <Input
          id="schoolName"
          value={data.schoolName || ''}
          onChange={(e) => onChange('schoolName', e.target.value)}
          placeholder="Enter school name"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="gradeLevel">Grade Level</Label>
        <Input
          id="gradeLevel"
          value={data.gradeLevel || ''}
          onChange={(e) => onChange('gradeLevel', e.target.value)}
          placeholder="Enter grade level"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="livingSituation">Living Situation</Label>
        <Select
          id="livingSituation"
          value={data.livingSituation || ''}
          onChange={(e) => onChange('livingSituation', e.target.value)}
        >
          <option value="">Select living situation</option>
          <option value="Alternative care">Alternative care</option>
          <option value="Group residential facility">Group residential facility</option>
          <option value="Homeless or marginally housed">Homeless or marginally housed</option>
          <option value="In detention">In detention</option>
          <option value="Living independently">Living independently</option>
          <option value="With parent(s)">With parent(s)</option>
          <option value="With relatives">With relatives</option>
          <option value="Other">Other</option>
          <option value="Unknown">Unknown</option>
        </Select>
      </div>

      <div className="space-y-2">
        <Label>Vulnerable Groups</Label>
        <div className="grid grid-cols-2 gap-2">
          {vulnerableOptions.map(option => (
            <div key={option} className="flex items-center space-x-2">
              <Checkbox
                id={`vulnerable-${option}`}
                checked={(data.vulnerableGroups || []).includes(option as any)}
                onCheckedChange={(checked) => {
                  const newGroups = checked
                    ? [...(data.vulnerableGroups || []), option as any]
                    : (data.vulnerableGroups || []).filter(g => g !== option);
                  onChange('vulnerableGroups', newGroups);
                }}
              />
              <Label htmlFor={`vulnerable-${option}`}>{option}</Label>
            </div>
          ))}
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="region">Region</Label>
        <Select
          id="region"
          value={data.region || ''}
          onChange={(e) => onChange('region', e.target.value)}
        >
          <option value="">Select region</option>
          <option value="Unknown">Unknown</option>
          <option value="Cities">Cities</option>
          <option value="Rural areas">Rural areas</option>
          <option value="Town & semi-dense areas">Town & semi-dense areas</option>
        </Select>
      </div>
    </div>
  );
};

export default ChildForm;