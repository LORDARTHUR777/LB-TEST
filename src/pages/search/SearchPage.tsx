import React, { useState } from 'react';
import { Search, List, Send, MessageCircle, PieChart, DollarSign, Settings, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

// Types
type FieldType = 'hashtags' | 'bio' | 'mention' | 'username' | 'region' | 'language' | 'country' | 'city';

type SelectOption = {
  code: string;
  name: string;
};

// Data
const languages: SelectOption[] = [
  { code: 'en', name: 'English' },
  { code: 'fr', name: 'French' },
  { code: 'es', name: 'Spanish' },
  { code: 'de', name: 'German' },
  { code: 'it', name: 'Italian' },
  { code: 'pt', name: 'Portuguese' },
  { code: 'ru', name: 'Russian' },
  { code: 'ja', name: 'Japanese' },
  { code: 'ko', name: 'Korean' },
  { code: 'zh', name: 'Chinese' },
  { code: 'ar', name: 'Arabic' },
  { code: 'hi', name: 'Hindi' },
  { code: 'bn', name: 'Bengali' },
].sort((a, b) => a.name.localeCompare(b.name));

const countries: SelectOption[] = [
  { code: 'FR', name: 'France' },
  { code: 'US', name: 'United States' },
  { code: 'GB', name: 'United Kingdom' },
  { code: 'DE', name: 'Germany' },
  { code: 'IT', name: 'Italy' },
  { code: 'ES', name: 'Spain' },
  { code: 'CA', name: 'Canada' },
  { code: 'AU', name: 'Australia' },
  { code: 'JP', name: 'Japan' },
  { code: 'BR', name: 'Brazil' },
  { code: 'IN', name: 'India' },
  { code: 'RU', name: 'Russia' },
  { code: 'CN', name: 'China' },
].sort((a, b) => a.name.localeCompare(b.name));

// Components
interface TagProps {
  text: string;
  onRemove: () => void;
}

const Tag: React.FC<TagProps> = ({ text, onRemove }) => (
  <div className="inline-flex items-center bg-blue-600 text-white rounded-md px-3 py-1 mr-2 text-sm">
    {text}
    <button
      onClick={onRemove}
      className="ml-2"
      aria-label={`Remove ${text}`}
    >
      <X className="h-3 w-3" />
    </button>
  </div>
);

interface SearchFieldProps {
  field: FieldType;
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onKeyPress?: (e: React.KeyboardEvent<HTMLInputElement>) => void;
  tags?: string[];
  onRemoveTag?: (field: FieldType, tag: string) => void;
  operator?: boolean;
  onOperatorClick?: (field: FieldType, operator: string) => void;
  isOperatorActive?: boolean;
  placeholder: string;
  operatorLabel?: string;
  isSelect?: boolean;
  selectOptions?: SelectOption[];
  onSelectChange?: (field: FieldType, value: string) => void;
}

const SearchField: React.FC<SearchFieldProps> = ({
  field,
  value = '',
  onChange = () => {},
  onKeyPress = () => {},
  tags = [],
  onRemoveTag = () => {},
  operator = false,
  onOperatorClick = () => {},
  isOperatorActive = false,
  placeholder = '',
  operatorLabel = '',
  isSelect = false,
  selectOptions = [],
  onSelectChange = () => {},
}) => (
  <div className="space-y-2">
    <div className="flex gap-2 items-center">
      {isSelect ? (
        <Select onValueChange={(value) => onSelectChange(field, value)}>
          <SelectTrigger className="bg-gray-800 border-gray-700 text-white">
            <SelectValue placeholder={placeholder} />
          </SelectTrigger>
          <SelectContent>
            {selectOptions.map((option) => (
              <SelectItem key={option.code} value={option.code}>
                {option.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      ) : (
        <Input
          className="bg-gray-800 border-gray-700 text-white"
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          onKeyPress={onKeyPress}
          aria-label={placeholder}
        />
      )}
      {operator && (
        <Button 
          variant={isOperatorActive ? "default" : "secondary"}
          className={`min-w-[60px] ${
            isOperatorActive 
              ? 'bg-blue-600 hover:bg-blue-700 text-white' 
              : 'bg-gray-700 text-gray-200 hover:bg-gray-600'
          }`}
          onClick={() => onOperatorClick(field, operatorLabel)}
          aria-label={`Toggle ${operatorLabel} operator for ${field}`}
        >
          <span>{operatorLabel}</span>
        </Button>
      )}
    </div>
    <div className="flex flex-wrap gap-2">
      {tags?.map((tag, index) => (
        <Tag key={index} text={tag} onRemove={() => onRemoveTag(field, tag)} />
      ))}
    </div>
  </div>
);

const SearchPage: React.FC = () => {
  const [inputValues, setInputValues] = useState<Record<FieldType, string>>({
    hashtags: '',
    bio: '',
    mention: '',
    username: '',
    region: '',
    language: '',
    country: '',
    city: ''
  });

  const [activeOperator, setActiveOperator] = useState<{ field: FieldType | null; operator: string | null }>({
    field: null,
    operator: null
  });

  const [tags, setTags] = useState<Record<FieldType, string[]>>({
    hashtags: [],
    bio: [],
    mention: [],
    username: [],
    region: [],
    language: [],
    country: [],
    city: []
  });

  const handleSelectChange = (field: FieldType, value: string) => {
    const option = field === 'language' 
      ? languages.find(l => l.code === value)
      : countries.find(c => c.code === value);

    if (option) {
      setTags(prev => ({
        ...prev,
        [field]: [...prev[field], option.name],
      }));
    }
  };

  const handleKeyPress = (field: FieldType, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && inputValues[field].trim()) {
      const newTag = inputValues[field].trim();
      setTags(prev => {
        let updatedTags;
        if (activeOperator.field === field) {
          const lastTag = prev[field][prev[field].length - 1];
          const combinedTag = `${lastTag} ${activeOperator.operator} ${newTag}`;
          updatedTags = [...prev[field].slice(0, -1), combinedTag];
          setActiveOperator({ field: null, operator: null });
        } else {
          updatedTags = [...prev[field], newTag];
        }
        return { ...prev, [field]: updatedTags };
      });
      setInputValues(prev => ({ ...prev, [field]: '' }));
    }
  };

  const removeTag = (field: FieldType, tagToRemove: string) => {
    setTags(prev => ({
      ...prev,
      [field]: prev[field].filter(tag => tag !== tagToRemove),
    }));
  };

  const handleOperatorClick = (field: FieldType, operator: string) => {
    setActiveOperator(prev => ({
      field: prev.field === field && prev.operator === operator ? null : field,
      operator: prev.field === field && prev.operator === operator ? null : operator
    }));
  };

  const sidebarItems = [
    { icon: Search, label: 'Search' },
    { icon: List, label: 'Lists' },
    { icon: Send, label: 'Send' },
    { icon: MessageCircle, label: 'Messages' },
    { icon: PieChart, label: 'Analytics' },
    { icon: DollarSign, label: 'Billing' },
  ];

  return (
    <div className="flex h-screen bg-gray-900">
      {/* Sidebar */}
      <div className="w-16 bg-blue-600 flex flex-col items-center py-4 space-y-8">
        <div className="w-full h-8 flex items-center justify-center text-white font-bold">
          LB
        </div>
        {sidebarItems.map(({ icon: Icon, label }) => (
          <Button 
            key={label} 
            variant="ghost" 
            size="icon" 
            className="text-white"
            aria-label={label}
          >
            <Icon className="w-5 h-5" />
          </Button>
        ))}
        <Button 
          variant="ghost" 
          size="icon" 
          className="text-white mt-auto"
          aria-label="Settings"
        >
          <Settings className="w-5 h-5" />
        </Button>
      </div>

      {/* Main content */}
      <div className="flex-1 p-6 space-y-6">
        <div className="grid grid-cols-2 gap-6">
          {/* Hashtags */}
          <SearchField
            field="hashtags"
            placeholder="Add hashtags..."
            value={inputValues.hashtags}
            onChange={(e) => setInputValues(prev => ({ ...prev, hashtags: e.target.value }))}
            onKeyPress={(e) => handleKeyPress('hashtags', e)}
            tags={tags.hashtags}
            onRemoveTag={removeTag}
            operator={true}
            onOperatorClick={handleOperatorClick}
            isOperatorActive={activeOperator.field === 'hashtags'}
            operatorLabel="OR"
          />

          {/* Bio */}
          <SearchField
            field="bio"
            placeholder="Search in bio..."
            value={inputValues.bio}
            onChange={(e) => setInputValues(prev => ({ ...prev, bio: e.target.value }))}
            onKeyPress={(e) => handleKeyPress('bio', e)}
            tags={tags.bio}
            onRemoveTag={removeTag}
            operator={true}
            onOperatorClick={handleOperatorClick}
            isOperatorActive={activeOperator.field === 'bio'}
            operatorLabel="OR"
          />

          {/* Language */}
          <SearchField
            field="language"
            placeholder="Select language..."
            isSelect={true}
            selectOptions={languages}
            onSelectChange={handleSelectChange}
            tags={tags.language}
            onRemoveTag={removeTag}
          />

          {/* Country */}
          <SearchField
            field="country"
            placeholder="Select country..."
            isSelect={true}
            selectOptions={countries}
            onSelectChange={handleSelectChange}
            tags={tags.country}
            onRemoveTag={removeTag}
          />
        </div>
      </div>
    </div>
  );
};

export default SearchPage;