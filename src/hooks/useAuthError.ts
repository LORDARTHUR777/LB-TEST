// src/hooks/useAuthError.ts
import { useState } from 'react';
import { useToast } from './use-toast';

interface AuthErrorState {
  message: string | null;
  code?: string;
  field?: string;
}

export const useAuthError = () => {
  const { toast } = useToast();
  const [errorState, setErrorState] = useState<AuthErrorState>({ 
    message: null 
  });

  const handleError = (error: unknown) => {
    let errorMessage = "Une erreur inattendue s'est produite";
    let errorCode: string | undefined;
    let errorField: string | undefined;

    if (error instanceof Error) {
      errorMessage = error.message;
      if ('code' in error) errorCode = (error as any).code;
      if ('field' in error) errorField = (error as any).field;
    }

    setErrorState({
      message: errorMessage,
      code: errorCode,
      field: errorField
    });

    toast({
      variant: "destructive",
      title: "Erreur",
      description: errorMessage
    });
  };

  const clearError = () => {
    setErrorState({ message: null });
  };

  return {
    error: errorState,
    handleError,
    clearError,
    isError: Boolean(errorState.message)
  };
};

// Types d'erreurs spécifiques à exporter
export class AuthenticationError extends Error {
  constructor(message: string, public code?: string) {
    super(message);
    this.name = 'AuthenticationError';
  }
}

export class ValidationError extends Error {
  constructor(message: string, public field?: string) {
    super(message);
    this.name = 'ValidationError';
  }
}
