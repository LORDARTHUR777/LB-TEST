// src/types/instagram.types.ts
export interface InstagramProfile {
  username: string;
  full_name: string;
  profile_picture_url: string;
  is_verified: boolean;
  followers_count: number;
  following_count?: number;
  engagement_rate?: number;
  average_likes?: number;
  category?: string;
  location?: string;
}

export interface SearchFilters {
  category?: string;
  location?: string;
  min_followers?: number;
  max_followers?: number;
}

export interface SearchResponse {
  data: InstagramProfile[];
  cursor?: string;
  has_more: boolean;
}

export const ERROR_MESSAGES = {
  API_ERROR: "Instagram API error",
  INVALID_TOKEN: "Invalid access token",
  NETWORK_ERROR: "Network error occurred",
  RATE_LIMIT: "Rate limit exceeded"
} as const;