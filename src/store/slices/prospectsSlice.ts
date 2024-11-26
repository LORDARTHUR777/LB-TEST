// src/store/slices/prospectsSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Message {
  type: 'first' | 'follow1' | 'follow2' | 'follow3' | 'follow4' | 'lead' | 'notInterested';
  date: string;
  content: string;
}

interface Prospect {
  id: number;
  account: string;
  list: string;
  status: string;
  messages: Record<string, string>; // Date -> Message Type
  info: {
    followers: number;
    following: number;
    posts: number;
    isVerified: boolean;
    bio: string;
    email?: string;
    website?: string;
  };
  lastContact?: string;
  nextFollowUp?: string;
}

interface ProspectsState {
  prospects: Prospect[];
  currentProspect: Prospect | null;
  filters: {
    list: string | null;
    status: string | null;
    dateRange: {
      start: string | null;
      end: string | null;
    };
  };
  messageTypes: {
    id: string;
    label: string;
    color: string;
  }[];
  isLoading: boolean;
  error: string | null;
}

const initialState: ProspectsState = {
  prospects: [],
  currentProspect: null,
  filters: {
    list: null,
    status: null,
    dateRange: {
      start: null,
      end: null
    }
  },
  messageTypes: [
    { id: 'first', label: '1er message', color: 'bg-blue-500' },
    { id: 'follow1', label: '1er Follow-up', color: 'bg-blue-500' },
    { id: 'follow2', label: '2ème Follow-up', color: 'bg-blue-500' },
    { id: 'follow3', label: '3ème Follow-up', color: 'bg-blue-500' },
    { id: 'follow4', label: '4ème Follow-up', color: 'bg-blue-500' },
    { id: 'lead', label: 'Lead chaud', color: 'bg-green-500' },
    { id: 'notInterested', label: 'Pas intéressé', color: 'bg-red-500' }
  ],
  isLoading: false,
  error: null
};

const prospectsSlice = createSlice({
  name: 'prospects',
  initialState,
  reducers: {
    // Ajouter un nouveau prospect
    addProspect(state, action: PayloadAction<Omit<Prospect, 'id' | 'messages'>>) {
      const newProspect = {
        ...action.payload,
        id: Date.now(),
        messages: {},
        status: ''
      };
      state.prospects.push(newProspect);
    },

    // Mettre à jour le statut d'un prospect
    updateProspectStatus(state, action: PayloadAction<{
      prospectId: number;
      date: string;
      messageType: string;
    }>) {
      const { prospectId, date, messageType } = action.payload;
      const prospect = state.prospects.find(p => p.id === prospectId);
      if (prospect) {
        prospect.messages[date] = messageType;
        // Mise à jour du statut basé sur le dernier message
        const messageTypeInfo = state.messageTypes.find(t => t.id === messageType);
        if (messageTypeInfo) {
          prospect.status = messageTypeInfo.label;
        }
      }
    },

    // Appliquer des filtres
    setFilters(state, action: PayloadAction<Partial<ProspectsState['filters']>>) {
      state.filters = {
        ...state.filters,
        ...action.payload
      };
    },

    // Sélectionner un prospect
    setCurrentProspect(state, action: PayloadAction<number>) {
      state.currentProspect = state.prospects.find(p => p.id === action.payload) || null;
    },

    // Planifier un suivi
    scheduleFollowUp(state, action: PayloadAction<{
      prospectId: number;
      date: string;
    }>) {
      const prospect = state.prospects.find(p => p.id === action.payload.prospectId);
      if (prospect) {
        prospect.nextFollowUp = action.payload.date;
      }
    },

    // Mettre à jour la dernière date de contact
    updateLastContact(state, action: PayloadAction<{
      prospectId: number;
      date: string;
    }>) {
      const prospect = state.prospects.find(p => p.id === action.payload.prospectId);
      if (prospect) {
        prospect.lastContact = action.payload.date;
      }
    },

    // Gestion du chargement et des erreurs
    startLoading(state) {
      state.isLoading = true;
      state.error = null;
    },

    setError(state, action: PayloadAction<string>) {
      state.isLoading = false;
      state.error = action.payload;
    },

    // Mise à jour des prospects depuis le serveur
    setProspects(state, action: PayloadAction<Prospect[]>) {
      state.prospects = action.payload;
      state.isLoading = false;
    }
  }
});

export const {
  addProspect,
  updateProspectStatus,
  setFilters,
  setCurrentProspect,
  scheduleFollowUp,
  updateLastContact,
  startLoading,
  setError,
  setProspects
} = prospectsSlice.actions;

export default prospectsSlice.reducer;
