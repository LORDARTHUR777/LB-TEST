// src/services/instagram.service.ts
import axios from "axios";
import type { AxiosInstance, InternalAxiosRequestConfig } from "axios";
import type { 
  SearchFilters,
  SearchResponse,
} from "@/types/instagram.types";
import { ERROR_MESSAGES } from "@/types/instagram.types";
import { instagramConfig } from "@/config/instagram.config";

export class InstagramService {
  private readonly api: AxiosInstance;
  private readonly baseURL: string;

  constructor() {
    this.baseURL = instagramConfig.apiUrl;
    this.api = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
    });
    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    this.api.interceptors.request.use(
      (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
        const token = localStorage.getItem("instagram_access_token");
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error: unknown) => Promise.reject(error instanceof Error ? error : new Error("Unknown error"))
    );
  }

  async searchProfiles(
    query: string,
    filters: SearchFilters = {},
    cursor?: string,
    limit = 20
  ): Promise<SearchResponse> {
    try {
      const { data } = await this.api.get<SearchResponse>("/search", {
        params: {
          q: query,
          cursor,
          limit,
          ...filters,
        },
      });
      return data;
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(ERROR_MESSAGES.API_ERROR);
      }
      throw new Error("An unknown error occurred");
    }
  }
}