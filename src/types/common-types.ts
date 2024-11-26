// src/types/index.ts
export * from './auth.types';
export * from './instagram.types';
export * from './lists.types';
export * from './messages.types';
export * from './api.types';

// src/types/auth.types.ts
export interface User {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  company?: string;
  avatar?: string;
  role: 'user' | 'admin';
  createdAt: string;
  updatedAt: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface RegisterData {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
  company?: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}

// src/types/instagram.types.ts
export interface InstagramProfile {
  id: string;
  username: string;
  fullName?: string;
  bio?: string;
  website?: string;
  email?: string;
  phoneNumber?: string;
  isPrivate: boolean;
  isVerified: boolean;
  followers: number;
  following: number;
  postsCount: number;
  profilePicUrl: string;
  externalUrl?: string;
  categoryName?: string;
  businessContactMethod?: string;
  businessEmail?: string;
  businessPhoneNumber?: string;
  hasYoutube?: boolean;
}

export interface SearchFilters {
  hashtags?: string[];
  bio?: string[];
  mention?: string[];
  username?: string[];
  region?: string[];
  language?: string[];
  country?: string[];
  city?: string[];
  filters: {
    hasEmail: boolean;
    hasYoutube: boolean;
    hideExisting: boolean;
    minFollowers?: number;
    maxFollowers?: number;
  };
}

export interface SearchResults {
  profiles: InstagramProfile[];
  total: number;
  page: number;
  limit: number;
  hasMore: boolean;
}

// src/types/lists.types.ts
export interface List {
  id: number;
  name: string;
  description?: string;
  profiles: InstagramProfile[];
  count: number;
  createdAt: string;
  updatedAt: string;
}

export interface ListInput {
  name: string;
  description?: string;
}

export interface ListStats {
  totalProfiles: number;
  responseRate: number;
  conversionRate: number;
  averageFollowers: number;
}

// src/types/messages.types.ts
export interface MessageNode {
  id: string;
  content: string;
  position: {
    x: number;
    y: number;
  };
}

export interface MessageConnection {
  fromId: string;
  toId: string;
}

export interface MessageFlow {
  id: number;
  name: string;
  description?: string;
  nodes: Record<string, MessageNode>;
  connections: MessageConnection[];
  createdAt: string;
  updatedAt: string;
}

export interface MessageTemplate {
  id: number;
  name: string;
  subject?: string;
  content: string;
  type: 'first' | 'follow1' | 'follow2' | 'follow3' | 'follow4' | 'lead' | 'notInterested';
  tags?: string[];
  createdAt: string;
  updatedAt: string;
}

export interface MessageStatus {
  id: number;
  listId: number;
  profileId: number;
  status: MessageTemplate['type'];
  sentAt: string;
  responseAt?: string;
}

// src/types/api.types.ts
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
  status: number;
}

export interface PaginationParams {
  page?: number;
  limit?: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  hasMore: boolean;
}

// src/types/ui.types.ts
export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface Toast {
  id: string;
  title: string;
  message?: string;
  type: ToastType;
  duration?: number;
}

export interface Modal {
  id: string;
  type: string;
  props?: Record<string, any>;
}
