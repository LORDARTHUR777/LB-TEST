import React, { Suspense } from 'react';
import { Provider } from 'react-redux';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { store } from '@/store';
import { ErrorBoundary } from '@/components/error/error-boundary';
import { Loading } from '@/components/ui/loading';
import PrivateRoute from '@/components/auth/PrivateRoute';
import PublicRoute from '@/components/auth/PublicRoute';
import { Sidebar } from '@/components/Layout';

// Lazy loading des pages avec types
const LoginPage = React.lazy(() => import('@/pages/auth/LoginPage'));
const RegisterPage = React.lazy(() => import('@/pages/auth/RegisterPage'));
const ForgotPasswordPage = React.lazy(() => import('@/pages/auth/ForgotPasswordPage'));
const ResetPasswordPage = React.lazy(() => import('@/pages/auth/ResetPasswordPage'));
const SearchPage = React.lazy(() => import('@/pages/search/SearchPage'));
const SearchResultsPage = React.lazy(() => import('@/pages/search/SearchResultsPage'));
const ListPage = React.lazy(() => import('@/pages/prospects/ListPage'));
const FollowUpPage = React.lazy(() => import('@/pages/prospects/FollowUpPage'));
const MessageFlowPage = React.lazy(() => import('@/pages/messages/MessageFlow'));
const CRMPage = React.lazy(() => import('@/pages/dashboard/CRMDashboard'));
const SettingsPage = React.lazy(() => import('@/pages/settings/SettingsPage'));
const PricingPage = React.lazy(() => import('@/pages/pricing/PricingPage'));
const NotFoundPage = React.lazy(() => import('@/pages/not-found'));

// Composant de chargement pour Suspense
const LoadingFallback = () => <Loading fullScreen size="lg" />;

// Layout pour les pages authentifiées
const AuthenticatedLayout = ({ children }: { children: React.ReactNode }) => (
  <div className="flex">
    <Sidebar />
    <main className="flex-1 p-6">{children}</main>
  </div>
);

// Routes de l'application
const AppRoutes = () => {
  return (
    <Routes>
      {/* Route par défaut */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />

      {/* Routes publiques */}
      <Route path="/login" element={
        <PublicRoute restricted>
          <Suspense fallback={<LoadingFallback />}>
            <LoginPage />
          </Suspense>
        </PublicRoute>
      } />
      
      <Route path="/register" element={
        <PublicRoute restricted>
          <Suspense fallback={<LoadingFallback />}>
            <RegisterPage />
          </Suspense>
        </PublicRoute>
      } />

      <Route path="/forgot-password" element={
        <PublicRoute restricted>
          <Suspense fallback={<LoadingFallback />}>
            <ForgotPasswordPage />
          </Suspense>
        </PublicRoute>
      } />

      <Route path="/reset-password" element={
        <PublicRoute restricted>
          <Suspense fallback={<LoadingFallback />}>
            <ResetPasswordPage />
          </Suspense>
        </PublicRoute>
      } />

      <Route path="/pricing" element={
        <PublicRoute>
          <Suspense fallback={<LoadingFallback />}>
            <PricingPage />
          </Suspense>
        </PublicRoute>
      } />

      {/* Routes privées avec Layout */}
      <Route path="/dashboard" element={
        <PrivateRoute>
          <AuthenticatedLayout>
            <Suspense fallback={<LoadingFallback />}>
              <CRMPage />
            </Suspense>
          </AuthenticatedLayout>
        </PrivateRoute>
      } />

      <Route path="/search" element={
        <PrivateRoute>
          <AuthenticatedLayout>
            <Suspense fallback={<LoadingFallback />}>
              <SearchPage />
            </Suspense>
          </AuthenticatedLayout>
        </PrivateRoute>
      } />

      <Route path="/search/results" element={
        <PrivateRoute>
          <AuthenticatedLayout>
            <Suspense fallback={<LoadingFallback />}>
              <SearchResultsPage />
            </Suspense>
          </AuthenticatedLayout>
        </PrivateRoute>
      } />

      <Route path="/prospects" element={
        <PrivateRoute>
          <AuthenticatedLayout>
            <Suspense fallback={<LoadingFallback />}>
              <ListPage />
            </Suspense>
          </AuthenticatedLayout>
        </PrivateRoute>
      } />

      <Route path="/prospects/follow-up" element={
        <PrivateRoute>
          <AuthenticatedLayout>
            <Suspense fallback={<LoadingFallback />}>
              <FollowUpPage />
            </Suspense>
          </AuthenticatedLayout>
        </PrivateRoute>
      } />

      <Route path="/messages" element={
        <PrivateRoute>
          <AuthenticatedLayout>
            <Suspense fallback={<LoadingFallback />}>
              <MessageFlowPage />
            </Suspense>
          </AuthenticatedLayout>
        </PrivateRoute>
      } />

      <Route path="/settings" element={
        <PrivateRoute>
          <AuthenticatedLayout>
            <Suspense fallback={<LoadingFallback />}>
              <SettingsPage />
            </Suspense>
          </AuthenticatedLayout>
        </PrivateRoute>
      } />

      {/* Page 404 */}
      <Route path="*" element={
        <Suspense fallback={<LoadingFallback />}>
          <NotFoundPage />
        </Suspense>
      } />
    </Routes>
  );
};

// Configuration principale de l'application
const MainAppConfiguration = () => {
  return (
    <Provider store={store}>
      <ErrorBoundary>
        <BrowserRouter>
          <AppRoutes />
        </BrowserRouter>
      </ErrorBoundary>
    </Provider>
  );
};

export default MainAppConfiguration;