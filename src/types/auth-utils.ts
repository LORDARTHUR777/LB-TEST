// types/auth-utils.ts

/**
 * Type utilitaire pour les réponses API
 */
export type ApiResponse<T> = {
  data: T;
  message?: string;
  success: boolean;
};

/**
 * Type pour les champs de formulaire communs
 */
export interface FormFields {
  email: string;
  password: string;
}

/**
 * Type utilitaire pour gérer les états de chargement des formulaires
 */
export interface FormState {
  isLoading: boolean;
  error: string | null;
  success: boolean;
}

/**
 * Types d'erreurs possibles dans l'authentification
 */
export enum AuthErrorType {
  INVALID_CREDENTIALS = 'INVALID_CREDENTIALS',
  NETWORK_ERROR = 'NETWORK_ERROR',
  SERVER_ERROR = 'SERVER_ERROR',
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  TOKEN_EXPIRED = 'TOKEN_EXPIRED',
  UNAUTHORIZED = 'UNAUTHORIZED'
}

/**
 * Configuration des règles de validation
 */
export interface ValidationRules {
  password: {
    minLength: number;
    requireNumbers: boolean;
    requireUppercase: boolean;
    requireSpecialChars: boolean;
  };
  email: {
    allowedDomains?: string[];
    blockDisposableEmails?: boolean;
  };
}
