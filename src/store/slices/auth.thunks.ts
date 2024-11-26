import { createAsyncThunk } from '@reduxjs/toolkit';
import { authService } from '@/services/auth.service';
import { startLoading, setError } from './authSlice';
import { toast } from '@/hooks/use-toast';
import { 
  LoginFormInputs, 
  ForgotPasswordFormInputs,
  ResetPasswordFormInputs,
  RegisterFormInputs,
  AuthError,
  AUTH_ERROR_CODES
} from '@/types/auth.types';

export const loginThunk = createAsyncThunk(
  'auth/login',
  async (credentials: LoginFormInputs, { dispatch }) => {
    try {
      dispatch(startLoading());
      const response = await authService.login(credentials);

      if (credentials.rememberMe) {
        localStorage.setItem('token', response.data?.token || '');
      } else {
        sessionStorage.setItem('token', response.data?.token || '');
      }

      toast({
        title: 'Connexion réussie',
        type: 'success'
      });

      return response;
    } catch (error: any) {
      const authError: AuthError = {
        message: error.message || 'Une erreur est survenue lors de la connexion',
        code: AUTH_ERROR_CODES.INVALID_CREDENTIALS,
        type: 'authentication'
      };
      dispatch(setError(authError));
      toast({
        title: 'Erreur de connexion',
        message: authError.message,
        type: 'error'
      });
      throw authError;
    }
  }
);

export const requestPasswordResetThunk = createAsyncThunk(
  'auth/requestPasswordReset',
  async (data: ForgotPasswordFormInputs, { dispatch }) => {
    try {
      const response = await authService.forgotPassword(data);
      toast({
        title: 'Email envoyé',
        message: 'Vérifiez votre boite mail pour réinitialiser votre mot de passe',
        type: 'success'
      });
      return response;
    } catch (error: any) {
      const authError: AuthError = {
        message: error.message || 'Erreur lors de la demande de réinitialisation',
        type: 'authentication'
      };
      dispatch(setError(authError));
      toast({
        title: 'Erreur',
        message: authError.message,
        type: 'error'
      });
      throw authError;
    }
  }
);

export const updateProfileThunk = createAsyncThunk(
  'auth/updateProfile',
  async (data: Partial<RegisterFormInputs>, { dispatch }) => {
    try {
      dispatch(startLoading());
      const response = await authService.updateProfile(data);
      toast({
        title: 'Profil mis à jour',
        type: 'success'
      });
      return response;
    } catch (error: any) {
      const authError: AuthError = {
        message: error.message || 'Erreur lors de la mise à jour du profil',
        type: 'validation'
      };
      dispatch(setError(authError));
      toast({
        title: 'Erreur',
        message: authError.message,
        type: 'error'
      });
      throw authError;
    }
  }
);