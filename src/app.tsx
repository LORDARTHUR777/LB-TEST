// app.tsx
import React from 'react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { ErrorBoundary } from '@/components/error/error-boundary';
import { ToastProvider } from './components/toast/toast-provider';
import { AuthMiddleware } from '@/middleware/auth-middleware';
import { store } from '@/store';
import App from './app';
import '@/styles/index.css';

const root = document.getElementById('root');
if (!root) throw new Error('Root element not found');

export default function AppRoot() {
  return (
    <React.StrictMode>
      <Provider store={store}>
        <BrowserRouter>
          <ErrorBoundary>
            <ToastProvider>
              <AuthMiddleware>
                <App />
              </AuthMiddleware>
            </ToastProvider>
          </ErrorBoundary>
        </BrowserRouter>
      </Provider>
    </React.StrictMode>
  );
}