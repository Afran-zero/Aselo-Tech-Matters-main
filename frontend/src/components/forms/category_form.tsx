import React from 'react';
import { Label } from '../ui/label';
import { Checkbox } from '../ui/checkbox';

export interface CategoryData {
  missing_children?: Array<'Child abduction' | 'Lost, unaccounted for or otherwise missing child' | 'Runaway' | 'Unspecified/Other'>;
  violence?: Array<'Bullying in school' | 'Bullying out of school' | 'Child labour (general)' | 'Child labour (domestic)' | 'Cyberbullying' | 'Emotional maltreatment/abuse' | 'Exposure to criminal violence' | 'Exposure to domestic violence' | 'Exposure to pornography' | 'Gender-based harmful traditional practices (other than FGM)' | 'Harmful traditional practices other than child marriage and FGM' | 'Inappropriate sex talk' | 'Indecent assault' | 'Neglect (emotional)' | 'Neglect (education)' | 'Neglect (health & nutrition)' | 'Neglect (physical)' | 'Neglect (or negligent treatment)' | 'Online child sexual abuse and exploitation' | 'Physical maltreatment/abuse' | 'Sexual violence' | 'Verbal maltreatment/abuse' | 'Unspecified/Other'>;
  trafficking?: Array<'Child begging' | 'Child used for criminal activity' | 'Commercial sexual exploitation (offline)' | 'Commercial sexual exploitation (online)' | 'Labour exploitation (domestic servitude)'>;
  mental_health?: Array<'Addictive behaviours and substance use' | 'Behavioural problems' | 'Concerns about the self' | 'Emotional distress - anger problems' | 'Emotional distress - fear and anxiety problems' | 'Emotional distress - mood problems' | 'Hyperactivity/attention deficit' | 'Neurodevelopmental concerns' | 'Problems with eating behaviour' | 'Self-esteem issues' | 'Self-harming behaviour' | 'Sleep disorders' | 'Stress' | 'Suicidal thoughts and suicide attempts' | 'Traumatic distress' | 'Wellbeing support' | 'Unspecified/Other'>;
  physical_health?: Array<'COVID-19' | 'General medical or lifestyle concerns' | 'Medical or lifestyle information about HIV/AIDS' | 'Pregnancy and maternal care' | 'Sexual and reproductive health' | 'Nutrition' | 'Unspecified/Other'>;
  accessibility?: Array<'Career Guidance' | 'Education' | 'Essential needs (food, shelter, water, clothing)' | 'Financial services' | 'General healthcare services' | 'Legal services and advice' | 'Mental health services' | 'Sexual health services' | 'Socio-economical services' | 'Unspecified/Other'>;
  discrimination_and_exclusion?: Array<'Ethnicity/nationality' | 'Financial situation' | 'Gender' | 'Gender identity or expression and sexual orientation' | 'Health' | 'Philosophical or religious beliefs' | 'Socio-economic situation' | 'Street children' | 'Unspecified/Other'>;
  family_relationships?: Array<'Adoption, fostering, and extended family placement' | 'Child in children\'s home' | 'Divorce/separation of parents' | 'Family health and wellbeing' | 'Family problems/disputes - conflict between parents/caregivers' | 'Family problems/disputes - conflict between parents/caregivers and child' | 'Family problems/disputes - conflict between child and other members of the family' | 'General family issues' | 'Grief/bereavement - family' | 'Left behind children' | 'Mental health - parental/relative' | 'Relationship with sibling(s)' | 'Relationship to caregiver'>;
  peer_relationships?: Array<'Friends and friendships' | 'Grief/bereavement - peers' | 'Partner relationships' | 'Classmates/colleagues relationships' | 'Unspecified/Other'>;
  education_and_occupation?: Array<'Academic issues' | 'Challenges with online schooling' | 'Child not attending school' | 'Child truanting from school' | 'Corporal punishment' | 'Homework/study tips' | 'Learning problems' | 'Performance anxiety' | 'Problems at work' | 'Teacher and school problems' | 'Unspecified/Other'>;
  sexuality?: Array<'Sexual orientation and gender identity' | 'Sexual behaviours' | 'Unspecified/Other'>;
  disability?: Array<'Intellectual disability' | 'Hearing disability' | 'Physical disability' | 'Visual disability'>;
  non_counselling_contacts?: Array<'Complaints about the child helpline' | 'Questions about the child helpline' | 'Questions about other services' | '"Thank you for your assistance"' | 'Unspecified/Other'>;
}

interface CategoryFormProps {
  data: CategoryData;
  onChange: (field: keyof CategoryData, value: any) => void;
}

const categoryGroups = {
  missing_children: {
    label: 'Missing Children',
    options: ['Child abduction', 'Lost, unaccounted for or otherwise missing child', 'Runaway', 'Unspecified/Other'],
  },
  violence: {
    label: 'Violence',
    options: ['Bullying in school', 'Bullying out of school', 'Child labour (general)', 'Child labour (domestic)', 'Cyberbullying', 'Emotional maltreatment/abuse', 'Exposure to criminal violence', 'Exposure to domestic violence', 'Exposure to pornography', 'Gender-based harmful traditional practices (other than FGM)', 'Harmful traditional practices other than child marriage and FGM', 'Inappropriate sex talk', 'Indecent assault', 'Neglect (emotional)', 'Neglect (education)', 'Neglect (health & nutrition)', 'Neglect (physical)', 'Neglect (or negligent treatment)', 'Online child sexual abuse and exploitation', 'Physical maltreatment/abuse', 'Sexual violence', 'Verbal maltreatment/abuse', 'Unspecified/Other'],
  },
  trafficking: {
    label: 'Trafficking',
    options: ['Child begging', 'Child used for criminal activity', 'Commercial sexual exploitation (offline)', 'Commercial sexual exploitation (online)', 'Labour exploitation (domestic servitude)'],
  },
  mental_health: {
    label: 'Mental Health',
    options: ['Addictive behaviours and substance use', 'Behavioural problems', 'Concerns about the self', 'Emotional distress - anger problems', 'Emotional distress - fear and anxiety problems', 'Emotional distress - mood problems', 'Hyperactivity/attention deficit', 'Neurodevelopmental concerns', 'Problems with eating behaviour', 'Self-esteem issues', 'Self-harming behaviour', 'Sleep disorders', 'Stress', 'Suicidal thoughts and suicide attempts', 'Traumatic distress', 'Wellbeing support', 'Unspecified/Other'],
  },
  physical_health: {
    label: 'Physical Health',
    options: ['COVID-19', 'General medical or lifestyle concerns', 'Medical or lifestyle information about HIV/AIDS', 'Pregnancy and maternal care', 'Sexual and reproductive health', 'Nutrition', 'Unspecified/Other'],
  },
  accessibility: {
    label: 'Accessibility',
    options: ['Career Guidance', 'Education', 'Essential needs (food, shelter, water, clothing)', 'Financial services', 'General healthcare services', 'Legal services and advice', 'Mental health services', 'Sexual health services', 'Socio-economical services', 'Unspecified/Other'],
  },
  discrimination_and_exclusion: {
    label: 'Discrimination and Exclusion',
    options: ['Ethnicity/nationality', 'Financial situation', 'Gender', 'Gender identity or expression and sexual orientation', 'Health', 'Philosophical or religious beliefs', 'Socio-economic situation', 'Street children', 'Unspecified/Other'],
  },
  family_relationships: {
    label: 'Family Relationships',
    options: ['Adoption, fostering, and extended family placement', 'Child in children\'s home', 'Divorce/separation of parents', 'Family health and wellbeing', 'Family problems/disputes - conflict between parents/caregivers', 'Family problems/disputes - conflict between parents/caregivers and child', 'Family problems/disputes - conflict between child and other members of the family', 'General family issues', 'Grief/bereavement - family', 'Left behind children', 'Mental health - parental/relative', 'Relationship with sibling(s)', 'Relationship to caregiver'],
  },
  peer_relationships: {
    label: 'Peer Relationships',
    options: ['Friends and friendships', 'Grief/bereavement - peers', 'Partner relationships', 'Classmates/colleagues relationships', 'Unspecified/Other'],
  },
  education_and_occupation: {
    label: 'Education and Occupation',
    options: ['Academic issues', 'Challenges with online schooling', 'Child not attending school', 'Child truanting from school', 'Corporal punishment', 'Homework/study tips', 'Learning problems', 'Performance anxiety', 'Problems at work', 'Teacher and school problems', 'Unspecified/Other'],
  },
  sexuality: {
    label: 'Sexuality',
    options: ['Sexual orientation and gender identity', 'Sexual behaviours', 'Unspecified/Other'],
  },
  disability: {
    label: 'Disability',
    options: ['Intellectual disability', 'Hearing disability', 'Physical disability', 'Visual disability'],
  },
  non_counselling_contacts: {
    label: 'Non-Counselling Contacts',
    options: ['Complaints about the child helpline', 'Questions about the child helpline', 'Questions about other services', '"Thank you for your assistance"', 'Unspecified/Other'],
  },
};

const CategoryForm: React.FC<CategoryFormProps> = ({ data, onChange }) => {
  return (
    <div className="space-y-6">
      {Object.entries(categoryGroups).map(([key, { label, options }]) => (
        <div key={key} className="space-y-2">
          <Label>{label}</Label>
          <div className="grid grid-cols-2 gap-2">
            {options.map(option => (
              <div key={option} className="flex items-center space-x-2">
                <Checkbox
                  id={`${key}-${option}`}
                  checked={((data[key as keyof CategoryData] as string[] | undefined) ?? []).includes(option)}
                  onCheckedChange={(checked) => {
                    const currentValues = (data[key as keyof CategoryData] as string[] | undefined) ?? [];
                    const newValues = checked
                      ? [...currentValues, option]
                      : currentValues.filter(v => v !== option);
                    onChange(key as keyof CategoryData, newValues);
                  }}
                />
                <Label htmlFor={`${key}-${option}`}>{option}</Label>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default CategoryForm;