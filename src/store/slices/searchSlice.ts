// src/store/slices/searchSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface SearchState {
  inputValues: {
    hashtags: string;
    bio: string;
    mention: string;
    username: string;
    region: string;
    language: string;
    country: string;
    city: string;
  };
  tags: {
    hashtags: string[];
    bio: string[];
    mention: string[];
    username: string[];
    region: string[];
    language: string[];
    country: string[];
    city: string[];
  };
  filters: {
    hasEmail: boolean;
    hasYoutube: boolean;
    hideExisting: boolean;
    minFollowers: string;
    maxFollowers: string;
  };
  results: any[];
  isLoading: boolean;
  error: string | null;
}

const initialState: SearchState = {
  inputValues: {
    hashtags: '',
    bio: '',
    mention: '',
    username: '',
    region: '',
    language: '',
    country: '',
    city: ''
  },
  tags: {
    hashtags: [],
    bio: [],
    mention: [],
    username: [],
    region: [],
    language: [],
    country: [],
    city: []
  },
  filters: {
    hasEmail: false,
    hasYoutube: false,
    hideExisting: false,
    minFollowers: '',
    maxFollowers: ''
  },
  results: [],
  isLoading: false,
  error: null
};

const searchSlice = createSlice({
  name: 'search',
  initialState,
  reducers: {
    setInputValue(state, action: PayloadAction<{ field: string; value: string }>) {
      const { field, value } = action.payload;
      state.inputValues[field] = value;
    },
    addTag(state, action: PayloadAction<{ field: string; tag: string }>) {
      const { field, tag } = action.payload;
      state.tags[field].push(tag);
    },
    removeTag(state, action: PayloadAction<{ field: string; tag: string }>) {
      const { field, tag } = action.payload;
      state.tags[field] = state.tags[field].filter(t => t !== tag);
    },
    setFilter(state, action: PayloadAction<{ key: string; value: any }>) {
      const { key, value } = action.payload;
      state.filters[key] = value;
    },
    startSearch(state) {
      state.isLoading = true;
      state.error = null;
    },
    searchSuccess(state, action: PayloadAction<any[]>) {
      state.results = action.payload;
      state.isLoading = false;
    },
    searchFailure(state, action: PayloadAction<string>) {
      state.error = action.payload;
      state.isLoading = false;
    }
  }
});

export const { 
  setInputValue, 
  addTag, 
  removeTag, 
  setFilter,
  startSearch,
  searchSuccess,
  searchFailure
} = searchSlice.actions;

export default searchSlice.reducer;
