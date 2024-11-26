import { useState } from "react";
import { useToast } from "@/hooks/use-toast";
import {
  type AuthError,
  loginSchema,
  registerSchema,
  forgotPasswordSchema,
  resetPasswordSchema,
  type LoginFormInputs,
  type RegisterFormInputs,
  type ForgotPasswordFormInputs,
  type ResetPasswordFormInputs,
} from "../../types/auth.types";

// Common hook for form error handling
export const useAuthError = () => {
  const [error, setError] = useState<AuthError | null>(null);
  const clearError = () => setError(null);
  return { error, setError, clearError };
};

// Common toast configuration
export const useAuthToast = () => {
  const { toast } = useToast();

  const showSuccessToast = (message: string) => {
    toast({
      variant: "success",
      title: "Succès",
      description: message,
      duration: 3000,
    });
  };

  const showErrorToast = (message: string) => {
    toast({
      variant: "destructive", 
      title: "Erreur",
      description: message,
      duration: 3000,
    });
  };

  return { showSuccessToast, showErrorToast };
};