// src/constants/index.ts
export const APP_NAME = 'LeadBuilder';

export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    FORGOT_PASSWORD: '/auth/forgot-password',
    RESET_PASSWORD: '/auth/reset-password',
    PROFILE: '/auth/profile'
  },
  INSTAGRAM: {
    SEARCH: '/instagram/search',
    PROFILE: '/instagram/profile',
    VERIFY: '/instagram/verify'
  },
  LISTS: {
    BASE: '/lists',
    PROFILES: (listId: number) => `/lists/${listId}/profiles`
  },
  MESSAGES: {
    TEMPLATES: '/messages/templates',
    FLOWS: '/messages/flows'
  }
};

export const MESSAGE_TYPES = {
  FIRST: { id: 'first', label: '1er message', color: 'bg-blue-500' },
  FOLLOW_1: { id: 'follow1', label: '1er Follow-up', color: 'bg-blue-500' },
  FOLLOW_2: { id: 'follow2', label: '2ème Follow-up', color: 'bg-blue-500' },
  FOLLOW_3: { id: 'follow3', label: '3ème Follow-up', color: 'bg-blue-500' },
  FOLLOW_4: { id: 'follow4', label: '4ème Follow-up', color: 'bg-blue-500' },
  LEAD: { id: 'lead', label: 'Lead chaud', color: 'bg-green-500' },
  NOT_INTERESTED: { id: 'notInterested', label: 'Pas intéressé', color: 'bg-red-500' }
};

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  SEARCH: '/search',
  RESULTS: '/results',
  LISTS: '/lists',
  FOLLOW_UP: '/follow-up',
  MESSAGE_FLOW: '/message-flow',
  CRM: '/crm',
  SETTINGS: '/settings',
  PRICING: '/pricing'
};

export const BREAKPOINTS = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px'
};
