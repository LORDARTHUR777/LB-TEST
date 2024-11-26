Leadbuilder
Leadbuilder est une application web conçue pour aider à la gestion des prospects, des utilisateurs, et des processus liés à la prospection et à l'acquisition de clients. Ce projet utilise React avec TypeScript, Redux pour la gestion d'état, et Vite pour la configuration et le bundling.

📂 Structure du projet
Voici une vue d'ensemble des principaux répertoires et fichiers du projet :

graphq
src/
├── assets/               # Fichiers statiques (images, icônes, etc.)
├── components/           # Composants réutilisables
│   ├── auth/             # Composants liés à l'authentification
│   │   ├── PrivateRoute.tsx
│   │   ├── PublicRoute.tsx
│   └── toast/            # Composants liés aux notifications
│   └── ui/               # Composants UI réutilisables (boutons, inputs, etc.)
├── config/               # Configuration globale (vite, etc.)
├── hooks/                # Custom hooks (use-toast, useAuthError, etc.)
├── layout/               # Gestion des layouts
├── middleware/           # Middlewares (authentification, etc.)
├── pages/                # Pages de l'application
│   ├── auth/             # Pages liées à l'authentification (login, register)
│   ├── dashboard/        # Pages liées au dashboard CRM
│   ├── pricing/          # Page de tarification
│   ├── search/           # Pages liées à la recherche
│   └── settings/         # Pages liées aux paramètres
├── services/             # Services API (authentification, requêtes, etc.)
├── slices/               # Slices Redux (auth, CRM, etc.)
├── styles/               # Styles CSS globaux
├── types/                # Types TypeScript pour les données
├── utils/                # Fonctions utilitaires
├── main.tsx              # Point d'entrée principal de l'application
└── app.tsx               # Conteneur principal (composition des Providers, Routes)
⚙️ Configuration
tsconfig.json
Le projet utilise des alias pour simplifier les imports :

@/ : Référence au dossier src/.
json
Copier le code
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
Vite Configuration
Le projet utilise Vite comme bundler pour une configuration rapide et optimisée. Les fichiers de configuration se trouvent dans :

vite-config.ts
vite-env.d.ts
🛠 Fonctionnalités principales
1. Authentification
Middleware auth-middleware.tsx : Gère les sessions utilisateurs (redirections et validation de tokens).
Redux Slice authSlice.ts : Stocke l'état utilisateur (isAuthenticated, token, etc.).
2. Notifications
Composants Toast : Gérés via un ToastProvider dans app.tsx.
3. CRM
Pages et composants pour la gestion des prospects.
Redux Slice crmSlice.ts.
4. UI Réutilisable
Répertoire ui/ contient des composants génériques tels que :
Boutons (button.tsx, button-loading.tsx)
Inputs (input.tsx)
Dialogues (dialog.tsx).
🚀 Démarrage rapide
Prérequis
Node.js version 16 ou supérieure
NPM ou Yarn
Installation
Clonez le projet :
bash
Copier le code
git clone https://github.com/votre-repo/leadbuilder.git
Accédez au dossier :
bash
Copier le code
cd leadbuilder
Installez les dépendances :
bash
Copier le code
npm install
# ou
yarn install
Lancer le projet
Pour démarrer en mode développement :

bash
Copier le code
npm run dev
# ou
yarn dev
🧪 Tests
Ajoutez des instructions spécifiques pour exécuter les tests si le projet en contient (par exemple Jest ou React Testing Library).

📚 Documentation des fichiers
Middleware
auth-middleware.tsx :
Valide les tokens stockés dans le localStorage.
Redirige les utilisateurs non authentifiés.
Slices
authSlice.ts :
Actions principales : loginSuccess, logout, setError.
crmSlice.ts :
Gère l'état des prospects et des données CRM.
Types
auth.types.ts :
Définitions de types pour les utilisateurs (AuthState), les erreurs (AuthError), et les codes (AUTH_ERROR_CODES).
Composants
error-boundary.tsx :
Gestionnaire global des erreurs JavaScript.
📂 Bonnes pratiques
Structure :

Séparez les composants réutilisables dans ui/.
Conservez les pages spécifiques dans pages/.
Gestion des états :

Utilisez Redux pour l'état global.
Créez des selectors clairs dans vos slices.
Organisation des fichiers :

Groupez les fichiers par fonctionnalité (auth, CRM, etc.).
🖥 Déploiement
Ajoutez des instructions pour le déploiement si applicable (par exemple sur Vercel, Netlify, ou un serveur dédié).

🏗 Technologies utilisées
React
Redux Toolkit
TypeScript
Vite
React Router
Tailwind CSS (si applicable)
📄 Licence
Ajoutez une licence si nécessaire, par exemple :

Copier le code
MIT License
Ce README.md est complet et peut être adapté selon vos besoins spécifiques. Dites-moi si vous souhaitez ajouter ou modifier certaines sections.






