// src/layouts/AuthLayout.tsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import { Card } from '@/components/ui/card';

export const AuthLayout = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md p-6">
        <div className="flex justify-center mb-8">
          <img src="/logo.svg" alt="Logo" className="h-12" />
        </div>
        <Card className="w-full p-6 shadow-lg">
          <Outlet />
        </Card>
      </div>
    </div>
  );
};