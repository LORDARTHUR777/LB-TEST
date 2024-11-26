// auth-middleware.tsx
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch } from '@/store/hooks';
import { loginSuccess, logout } from '@/store/slices/authSlice';
import { useToast } from '@/hooks/use-toast';
import { AuthState, AuthError, AUTH_ERROR_CODES } from '@/types/auth.types';
import type { ReactNode } from 'react';

export const AuthMiddleware = ({ children }: { children: ReactNode }) => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { toast } = useToast();

  useEffect(() => {
    const initAuth = async () => {
      const userStr = localStorage.getItem('user');
      const token = localStorage.getItem('token');

      if (!userStr || !token) {
        dispatch(logout());
        return;
      }

      try {
        const user = JSON.parse(userStr) as NonNullable<AuthState['user']>;
        dispatch(loginSuccess({ user, token }));
      } catch {
        const authError: AuthError = {
          message: "Votre session a expiré. Veuillez vous reconnecter.",
          code: AUTH_ERROR_CODES.INVALID_TOKEN,

          type: 'authentication'
        };

        localStorage.removeItem('token');
        localStorage.removeItem('user');
        dispatch(logout());
        
        toast({
          variant: "destructive",
          title: "Erreur d'authentification",
          description: authError.message
        });
        
        navigate('/auth/login');
      }
    };

    initAuth();
  }, [dispatch, navigate, toast]);

  return <>{children}</>;
};