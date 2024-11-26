// src/store/slices/messagesSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface MessageNode {
  id: string;
  content: string;
  position: {
    x: number;
    y: number;
  };
}

interface Connection {
  fromId: string;
  toId: string;
}

interface MessagesState {
  nodes: Record<string, MessageNode>;
  connections: Connection[];
  selectedNode: string | null;
  templates: {
    id: string;
    name: string;
    messages: Record<string, MessageNode>;
    connections: Connection[];
  }[];
  activeTemplate: string | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: MessagesState = {
  nodes: {
    'Message 1': {
      id: 'Message 1',
      content: "Bonjour,\n\nJe vous écris car vous êtes (métier).\n\nJ'ai fait un tour sur votre site et certains points marketing essentiels sont absents.\n\nJ'ai réalisé une vidéo de quelques minutes qui explique ce qui ne va pas sur votre site et comment l'améliorer pour augmenter vos ventes.\n\nEst ce que ça vous intéresserait que je vous l'envoie ?",
      position: { x: 50, y: 50 }
    },
    'Message 2': {
      id: 'Message 2',
      content: "Ok, top! Je vous l'envoie maintenant. (lien)\n\nJe peux compter sur vous pour me retour une fois que vous l'aurez visionnée ?",
      position: { x: 400, y: 150 }
    },
    'Message 3': {
      id: 'Message 3',
      content: "Par simple curiosité, quel serait votre objectif de chiffre d'affaires mensuel pour les 6 prochains mois ?",
      position: { x: 400, y: 300 }
    }
  },
  connections: [
    { fromId: 'Message 1', toId: 'Message 2' },
    { fromId: 'Message 2', toId: 'Message 3' }
  ],
  selectedNode: null,
  templates: [],
  activeTemplate: null,
  isLoading: false,
  error: null
};

const messagesSlice = createSlice({
  name: 'messages',
  initialState,
  reducers: {
    // Gestion des nodes (messages)
    addNode(state, action: PayloadAction<{
      id: string;
      content: string;
      position: { x: number; y: number }
    }>) {
      const { id, content, position } = action.payload;
      state.nodes[id] = { id, content, position };
    },

    updateNodeContent(state, action: PayloadAction<{
      id: string;
      content: string;
    }>) {
      const { id, content } = action.payload;
      if (state.nodes[id]) {
        state.nodes[id].content = content;
      }
    },

    updateNodePosition(state, action: PayloadAction<{
      id: string;
      position: { x: number; y: number }
    }>) {
      const { id, position } = action.payload;
      if (state.nodes[id]) {
        state.nodes[id].position = position;
      }
    },

    deleteNode(state, action: PayloadAction<string>) {
      const nodeId = action.payload;
      // Supprimer le node
      delete state.nodes[nodeId];
      // Supprimer les connexions associées
      state.connections = state.connections.filter(
        conn => conn.fromId !== nodeId && conn.toId !== nodeId
      );
    },

    // Gestion des connexions
    addConnection(state, action: PayloadAction<Connection>) {
      state.connections.push(action.payload);
    },

    removeConnection(state, action: PayloadAction<{
      fromId: string;
      toId: string;
    }>) {
      state.connections = state.connections.filter(
        conn => !(conn.fromId === action.payload.fromId && conn.toId === action.payload.toId)
      );
    },

    // Gestion des templates
    saveAsTemplate(state, action: PayloadAction<{
      name: string;
    }>) {
      const newTemplate = {
        id: Date.now().toString(),
        name: action.payload.name,
        messages: { ...state.nodes },
        connections: [...state.connections]
      };
      state.templates.push(newTemplate);
    },

    loadTemplate(state, action: PayloadAction<string>) {
      const template = state.templates.find(t => t.id === action.payload);
      if (template) {
        state.nodes = { ...template.messages };
        state.connections = [...template.connections];
        state.activeTemplate = template.id;
      }
    },

    deleteTemplate(state, action: PayloadAction<string>) {
      state.templates = state.templates.filter(t => t.id !== action.payload);
      if (state.activeTemplate === action.payload) {
        state.activeTemplate = null;
      }
    },

    // Sélection de node
    setSelectedNode(state, action: PayloadAction<string | null>) {
      state.selectedNode = action.payload;
    },

    // Gestion du chargement
    startLoading(state) {
      state.isLoading = true;
      state.error = null;
    },

    setError(state, action: PayloadAction<string>) {
      state.isLoading = false;
      state.error = action.payload;
    }
  }
});

export const {
  addNode,
  updateNodeContent,
  updateNodePosition,
  deleteNode,
  addConnection,
  removeConnection,
  saveAsTemplate,
  loadTemplate,
  deleteTemplate,
  setSelectedNode,
  startLoading,
  setError
} = messagesSlice.actions;

export default messagesSlice.reducer;
