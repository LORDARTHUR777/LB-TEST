import { Component, ErrorInfo, ReactNode } from 'react';
import { RefreshCw } from 'lucide-react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught:', error, errorInfo);
    // Ici vous pourriez envoyer l'erreur à un service de monitoring
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-900">
          <div className="text-center p-8">
            <h1 className="text-3xl font-bold text-white mb-4" role="alert">
              Oups ! Quelque chose s&apos;est mal passé
            </h1>
            <p className="text-gray-400 mb-8">
              Une erreur inattendue est survenue. Veuillez rafraîchir la page.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              aria-label="Rafraîchir la page"
              type="button"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Rafraîchir la page</span>
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}