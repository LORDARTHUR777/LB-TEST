// src/store/slices/listsSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface List {
  id: number;
  name: string;
  count: number;
  prospects: Array<{
    id: number;
    username: string;
    profile_pic?: string;
    followers?: number;
    isVerified?: boolean;
  }>;
}

interface ListsState {
  lists: List[];
  currentList: List | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: ListsState = {
  lists: [],
  currentList: null,
  isLoading: false,
  error: null
};

const listsSlice = createSlice({
  name: 'lists',
  initialState,
  reducers: {
    // Création d'une nouvelle liste
    createList(state, action: PayloadAction<{ name: string }>) {
      const newList = {
        id: Date.now(),
        name: action.payload.name,
        count: 0,
        prospects: []
      };
      state.lists.push(newList);
    },

    // Suppression d'une liste
    deleteList(state, action: PayloadAction<number>) {
      state.lists = state.lists.filter(list => list.id !== action.payload);
    },

    // Modification du nom d'une liste
    updateListName(state, action: PayloadAction<{ id: number; name: string }>) {
      const list = state.lists.find(list => list.id === action.payload.id);
      if (list) {
        list.name = action.payload.name;
      }
    },

    // Ajout d'un prospect à une liste
    addProspectToList(state, action: PayloadAction<{ 
      listId: number;
      prospect: {
        id: number;
        username: string;
        profile_pic?: string;
        followers?: number;
        isVerified?: boolean;
      }
    }>) {
      const list = state.lists.find(list => list.id === action.payload.listId);
      if (list && !list.prospects.find(p => p.id === action.payload.prospect.id)) {
        list.prospects.push(action.payload.prospect);
        list.count++;
      }
    },

    // Suppression d'un prospect d'une liste
    removeProspectFromList(state, action: PayloadAction<{ 
      listId: number;
      prospectId: number;
    }>) {
      const list = state.lists.find(list => list.id === action.payload.listId);
      if (list) {
        list.prospects = list.prospects.filter(
          prospect => prospect.id !== action.payload.prospectId
        );
        list.count--;
      }
    },

    // Sélection d'une liste courante
    setCurrentList(state, action: PayloadAction<number>) {
      state.currentList = state.lists.find(list => list.id === action.payload) || null;
    },

    // Gestion du chargement
    startLoading(state) {
      state.isLoading = true;
      state.error = null;
    },

    // Gestion des erreurs
    setError(state, action: PayloadAction<string>) {
      state.isLoading = false;
      state.error = action.payload;
    },

    // Mise à jour des listes depuis le serveur
    setLists(state, action: PayloadAction<List[]>) {
      state.lists = action.payload;
      state.isLoading = false;
    }
  }
});

export const {
  createList,
  deleteList,
  updateListName,
  addProspectToList,
  removeProspectFromList,
  setCurrentList,
  startLoading,
  setError,
  setLists
} = listsSlice.actions;

export default listsSlice.reducer;
