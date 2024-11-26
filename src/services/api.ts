// src/services/api.ts
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Intercepteur pour ajouter le token aux requêtes
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token') || sessionStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Intercepteur pour gérer les erreurs
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expiré ou invalide
      localStorage.removeItem('token');
      sessionStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// src/services/auth.service.ts
import api from './api';
import { User, LoginCredentials, RegisterData } from '../types';

export const authService = {
  async login(credentials: LoginCredentials) {
    const response = await api.post<{token: string; user: User}>('/auth/login', credentials);
    return response.data;
  },

  async register(data: RegisterData) {
    const response = await api.post<{token: string; user: User}>('/auth/register', data);
    return response.data;
  },

  async forgotPassword(email: string) {
    const response = await api.post('/auth/forgot-password', { email });
    return response.data;
  },

  async resetPassword(token: string, password: string) {
    const response = await api.post('/auth/reset-password', { token, password });
    return response.data;
  },

  async getProfile() {
    const response = await api.get<User>('/auth/profile');
    return response.data;
  },

  async updateProfile(data: Partial<User>) {
    const response = await api.patch<User>('/auth/profile', data);
    return response.data;
  },

  logout() {
    localStorage.removeItem('token');
    sessionStorage.removeItem('token');
  }
};

// src/services/instagram.service.ts
import api from './api';
import { SearchFilters, SearchResults, InstagramProfile } from '../types';

export const instagramService = {
  async search(filters: SearchFilters) {
    const response = await api.post<SearchResults>('/instagram/search', filters);
    return response.data;
  },

  async getProfile(username: string) {
    const response = await api.get<InstagramProfile>(`/instagram/profile/${username}`);
    return response.data;
  },

  async verifyAccount(username: string) {
    const response = await api.post<{verified: boolean}>('/instagram/verify', { username });
    return response.data;
  },

  async getFollowers(username: string, limit: number = 20) {
    const response = await api.get(`/instagram/followers/${username}`, {
      params: { limit }
    });
    return response.data;
  },

  async getFollowing(username: string, limit: number = 20) {
    const response = await api.get(`/instagram/following/${username}`, {
      params: { limit }
    });
    return response.data;
  }
};

// src/services/lists.service.ts
import api from './api';
import { List, ListInput } from '../types';

export const listsService = {
  async getLists() {
    const response = await api.get<List[]>('/lists');
    return response.data;
  },

  async createList(data: ListInput) {
    const response = await api.post<List>('/lists', data);
    return response.data;
  },

  async updateList(id: number, data: Partial<ListInput>) {
    const response = await api.patch<List>(`/lists/${id}`, data);
    return response.data;
  },

  async deleteList(id: number) {
    await api.delete(`/lists/${id}`);
  },

  async addProfileToList(listId: number, profileId: number) {
    const response = await api.post(`/lists/${listId}/profiles`, { profileId });
    return response.data;
  },

  async removeProfileFromList(listId: number, profileId: number) {
    await api.delete(`/lists/${listId}/profiles/${profileId}`);
  }
};

// src/services/messages.service.ts
import api from './api';
import { MessageTemplate, MessageFlow } from '../types';

export const messagesService = {
  async getTemplates() {
    const response = await api.get<MessageTemplate[]>('/messages/templates');
    return response.data;
  },

  async createTemplate(data: MessageTemplate) {
    const response = await api.post<MessageTemplate>('/messages/templates', data);
    return response.data;
  },

  async updateTemplate(id: number, data: Partial<MessageTemplate>) {
    const response = await api.patch<MessageTemplate>(`/messages/templates/${id}`, data);
    return response.data;
  },

  async deleteTemplate(id: number) {
    await api.delete(`/messages/templates/${id}`);
  },

  async getMessageFlow(id: number) {
    const response = await api.get<MessageFlow>(`/messages/flows/${id}`);
    return response.data;
  },

  async saveMessageFlow(data: MessageFlow) {
    const response = await api.post<MessageFlow>('/messages/flows', data);
    return response.data;
  }
};
