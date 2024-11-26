// src/store/slices/crmSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ListStats {
  name: string;
  count: number;
  responseRate: number;
  conversionRate: number;
}

interface FunnelStage {
  stage: string;
  count: number;
  percentage: number;
}

interface TimelineData {
  date: string;
  messagesCount: number;
  responsesCount: number;
  leadsCount: number;
}

interface KPIData {
  totalMessages: number;
  totalResponses: number;
  totalLeads: number;
  conversionRate: number;
  responseRate: number;
  averageResponseTime: number;
}

interface CRMState {
  timeFilter: 'allTime' | 'monthToDate' | 'week' | 'today' | 'yesterday' | 'custom';
  customDateRange: {
    start: string | null;
    end: string | null;
  };
  listStats: ListStats[];
  funnelData: FunnelStage[];
  timelineData: TimelineData[];
  kpiData: KPIData;
  compareMode: boolean;
  comparisonData: {
    current: KPIData;
    previous: KPIData;
  } | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: CRMState = {
  timeFilter: 'monthToDate',
  customDateRange: {
    start: null,
    end: null
  },
  listStats: [
    { name: 'e-commerce mode', count: 131, responseRate: 25.3, conversionRate: 8.4 },
    { name: 'Coach de sport', count: 280, responseRate: 31.2, conversionRate: 12.1 },
    { name: 'e-commerce CBD', count: 125, responseRate: 28.7, conversionRate: 9.8 }
  ],
  funnelData: [
    { stage: '1er message', count: 280, percentage: 100 },
    { stage: '1er Follow-up', count: 183, percentage: 65.3 },
    { stage: '2ème Follow-up', count: 128, percentage: 45.7 },
    { stage: '3ème Follow-up', count: 35, percentage: 12.5 },
    { stage: 'Lead chaud', count: 29, percentage: 10.3 },
    { stage: 'Pas intéressé', count: 18, percentage: 6.4 }
  ],
  timelineData: [],
  kpiData: {
    totalMessages: 0,
    totalResponses: 0,
    totalLeads: 0,
    conversionRate: 0,
    responseRate: 0,
    averageResponseTime: 0
  },
  compareMode: false,
  comparisonData: null,
  isLoading: false,
  error: null
};

const crmSlice = createSlice({
  name: 'crm',
  initialState,
  reducers: {
    // Gestion des filtres temporels
    setTimeFilter(state, action: PayloadAction<CRMState['timeFilter']>) {
      state.timeFilter = action.payload;
    },

    setCustomDateRange(state, action: PayloadAction<{
      start: string;
      end: string;
    }>) {
      state.customDateRange = action.payload;
    },

    // Mise à jour des données de liste
    updateListStats(state, action: PayloadAction<ListStats[]>) {
      state.listStats = action.payload;
    },

    // Mise à jour des données de l'entonnoir
    updateFunnelData(state, action: PayloadAction<FunnelStage[]>) {
      state.funnelData = action.payload;
    },

    // Mise à jour des données temporelles
    updateTimelineData(state, action: PayloadAction<TimelineData[]>) {
      state.timelineData = action.payload;
    },

    // Mise à jour des KPIs
    updateKPIData(state, action: PayloadAction<KPIData>) {
      state.kpiData = action.payload;
    },

    // Gestion du mode comparaison
    toggleCompareMode(state) {
      state.compareMode = !state.compareMode;
      if (!state.compareMode) {
        state.comparisonData = null;
      }
    },

    // Mise à jour des données de comparaison
    setComparisonData(state, action: PayloadAction<{
      current: KPIData;
      previous: KPIData;
    }>) {
      state.comparisonData = action.payload;
    },

    // Ajout d'un nouvel événement
    addEvent(state, action: PayloadAction<{
      type: 'message' | 'response' | 'lead';
      date: string;
      listName: string;
    }>) {
      // Mettre à jour les statistiques en fonction de l'événement
      const { type, date, listName } = action.payload;
      
      // Mise à jour des KPIs
      if (type === 'message') {
        state.kpiData.totalMessages++;
      } else if (type === 'response') {
        state.kpiData.totalResponses++;
      } else if (type === 'lead') {
        state.kpiData.totalLeads++;
      }

      // Recalculer les taux
      state.kpiData.responseRate = (state.kpiData.totalResponses / state.kpiData.totalMessages) * 100;
      state.kpiData.conversionRate = (state.kpiData.totalLeads / state.kpiData.totalMessages) * 100;
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
    }
  }
});

export const {
  setTimeFilter,
  setCustomDateRange,
  updateListStats,
  updateFunnelData,
  updateTimelineData,
  updateKPIData,
  toggleCompareMode,
  setComparisonData,
  addEvent,
  startLoading,
  setError
} = crmSlice.actions;

export default crmSlice.reducer;
