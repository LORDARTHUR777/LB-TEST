import { z } from "zod"

// Classes d'erreur personnalisées
export class AuthenticationError extends Error {
  constructor(message: string, public code?: string, public field?: string) {
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

// Schéma de connexion
export const loginSchema = z.object({
  email: z.string().email("Email invalide"),
  password: z.string().min(6, "Le mot de passe doit contenir au moins 6 caractères"),
  rememberMe: z.boolean().optional().default(false)
})

export type LoginFormInputs = z.infer<typeof loginSchema>

// Schéma du formulaire mot de passe oublié
export const forgotPasswordSchema = z.object({
  email: z.string().email("Email invalide")
})

export type ForgotPasswordFormInputs = z.infer<typeof forgotPasswordSchema>

// Schéma de réinitialisation du mot de passe
export const resetPasswordSchema = z.object({
  password: z
    .string()
    .min(6, "Le mot de passe doit contenir au moins 6 caractères")
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$/,
      "Le mot de passe doit contenir au moins une majuscule, une minuscule et un chiffre"
    ),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Les mots de passe ne correspondent pas",
  path: ["confirmPassword"]
})

export type ResetPasswordFormInputs = z.infer<typeof resetPasswordSchema>

// Schéma d'inscription
export const registerSchema = z.object({
  fullName: z.string().min(2, "Le nom complet doit contenir au moins 2 caractères"),
  email: z.string().email("Email invalide"),
  password: z
    .string()
    .min(6, "Le mot de passe doit contenir au moins 6 caractères")
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$/,
      "Le mot de passe doit contenir au moins une majuscule, une minuscule et un chiffre"
    ),
  confirmPassword: z.string(),
  acceptTerms: z.boolean().refine((val) => val === true, {
    message: "Vous devez accepter les conditions d'utilisation"
  })
}).refine((data) => data.password === data.confirmPassword, {
  message: "Les mots de passe ne correspondent pas",
  path: ["confirmPassword"]
})

export type RegisterFormInputs = z.infer<typeof registerSchema>

// Types pour les réponses du service d'authentification
export interface AuthResponse {
  success: boolean
  message: string
  data?: {
    token?: string
    user?: {
      id: string
      email: string
      fullName: string
    }
  }
}

// Type d'erreur amélioré pour l'authentification
export interface AuthError {
  message: string
  code?: string
  field?: string
  type?: 'authentication' | 'validation' | 'network' | 'unknown'
}

// État global d'authentification
export interface AuthState {
  user: {
    id: string
    email: string
    fullName: string
  } | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: AuthError | null
}

// Constants pour les codes d'erreur
export const AUTH_ERROR_CODES = {
  INVALID_CREDENTIALS: 'INVALID_CREDENTIALS',
  INVALID_TOKEN: 'INVALID_TOKEN',
  EMAIL_EXISTS: 'EMAIL_EXISTS',
  NETWORK_ERROR: 'NETWORK_ERROR',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  SERVER_ERROR: 'SERVER_ERROR',
} as const

export type AuthErrorCode = typeof AUTH_ERROR_CODES[keyof typeof AUTH_ERROR_CODES]