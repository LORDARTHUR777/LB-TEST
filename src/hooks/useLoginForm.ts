// src/hooks/useLoginForm.ts
import { useState } from 'react';
import { useAppDispatch, useAppSelector } from '@/store/hooks';
import { loginThunk } from '@/store/slices/auth.thunks';
import { selectAuth } from '@/store/slices/authSlice';
import { useNavigate } from 'react-router-dom';
import { useAuthError } from './useAuthError';  // Ajoutez cette ligne

export const useLoginForm = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { isLoading } = useAppSelector(selectAuth);
  const { error, handleError, clearError } = useAuthError();  // Utilisez le nouveau hook
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false
  });

  const updateFormData = (field: keyof typeof formData, value: any) => {
    clearError();  // Effacez l'erreur quand l'utilisateur modifie le formulaire
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await dispatch(loginThunk(formData)).unwrap();
      navigate('/dashboard');
    } catch (error) {
      handleError(error);  // Utilisez le nouveau gestionnaire d'erreurs
    }
  };

  return {
    formData,
    updateFormData,
    handleSubmit,
    isLoading,
    error,
    clearError
  };
};