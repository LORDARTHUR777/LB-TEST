// src/components/Layout.tsx
import { useAppDispatch } from '../store/hooks';
import { logout } from '../store/slices/authSlice';
import { Button } from './ui/button';
import { LogOut } from 'lucide-react';

export const Sidebar = () => {
  const dispatch = useAppDispatch();

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <aside className="w-64 bg-gray-800 min-h-screen p-4">
      <Button
        variant="ghost"
        className="w-full text-gray-300 hover:text-white"
        onClick={handleLogout}
      >
        <LogOut className="mr-2 h-4 w-4" />
        Déconnexion
      </Button>
    </aside>
  );
};