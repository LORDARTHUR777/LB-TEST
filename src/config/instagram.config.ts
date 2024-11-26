// src/config/instagram.config.ts
export interface InstagramConfig {
  apiUrl: string;
  clientId: string;
  clientSecret: string;
  redirectUri: string;
  scopes: string[];
  apiVersion: string;
}

export const instagramConfig = {
  apiUrl: process.env.NEXT_PUBLIC_INSTAGRAM_API_URL || 'https://api.your-domain.com/instagram',
  clientId: process.env.INSTAGRAM_CLIENT_ID || '',
  clientSecret: process.env.INSTAGRAM_CLIENT_SECRET || '',
  redirectUri: process.env.NEXT_PUBLIC_INSTAGRAM_REDIRECT_URI || 'http://localhost:3000/auth/instagram/callback',
  scopes: [
    'instagram_basic',
    'instagram_manage_insights',
    'pages_show_list',
    'pages_read_engagement',
    'business_management'
  ],
  apiVersion: 'v18.0'
} as const;