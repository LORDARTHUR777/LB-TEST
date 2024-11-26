// authSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { AuthState, AuthError, AUTH_ERROR_CODES } from '@/types/auth.types';

const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
};

export const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginSuccess: (
      state,
      action: PayloadAction<{
        user: NonNullable<AuthState['user']>;
        token: string;
      }>
    ) => {
      state.isAuthenticated = true;
      state.user = action.payload.user;
      state.token = action.payload.token;
      state.error = null;
      state.isLoading = false;
    },

    loginFailure: (state, action: PayloadAction<AuthError>) => {
      state.isAuthenticated = false;
      state.user = null;
      state.token = null;
      state.error = action.payload;
      state.isLoading = false;
    },

    logout: (state) => {
      // Reset state properties manually to avoid conflicts
      state.isAuthenticated = false;
      state.user = null;
      state.token = null;
      state.error = null;
      state.isLoading = false;
    },

    updateProfile: (state, action: PayloadAction<Partial<NonNullable<AuthState['user']>>>) => {
      if (state.user) {
        state.user = { ...state.user, ...action.payload };
      }
    },

    setError: (state, action: PayloadAction<AuthError>) => {
      state.error = action.payload;
      state.isLoading = false;
    },

    clearError: (state) => {
      state.error = null;
    },
  },
});

export const {
  loginSuccess,
  loginFailure,
  logout,
  updateProfile,
  setError,
  clearError,
} = authSlice.actions;

interface RootState {
  auth: AuthState;
}

// Selectors
export const selectAuth = (state: RootState) => state.auth;
export const selectIsAuthenticated = (state: RootState) => state.auth.isAuthenticated;
export const selectUser = (state: RootState) => state.auth.user;
export const selectIsLoading = (state: RootState) => state.auth.isLoading;
export const selectError = (state: RootState) => state.auth.error;

// Utility function for creating an AuthError
export const createAuthError = (
  message: string,
  code: keyof typeof AUTH_ERROR_CODES, // Ensure compatibility with AUTH_ERROR_CODES
  field?: string,
  type: AuthError['type'] = 'authentication'
): AuthError => ({
  message,
  code,
  field,
  type,
});

export default authSlice.reducer;
