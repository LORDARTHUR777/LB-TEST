// Sidebar.tsx
import { useLocation, useNavigate } from 'react-router-dom';
import { useAppDispatch } from '@/store/hooks';
import { logout } from '@/store/slices/authSlice';
import { Search, List, Send, MessageCircle, PieChart, DollarSign } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';

interface NavItem {
  icon: LucideIcon;
  path: string;
  label: string;
}

const navItems: NavItem[] = [
  { icon: Search, path: '/search', label: 'Recherche' },
  { icon: List, path: '/lists', label: 'Listes' },
  { icon: Send, path: '/follow-up', label: 'Suivi' },
  { icon: MessageCircle, path: '/message-flow', label: 'Messages' },
  { icon: PieChart, path: '/crm', label: 'CRM' },
  { icon: DollarSign, path: '/pricing', label: 'Abonnement' }
];

export default function Sidebar() {  // Changé pour un export par défaut
  const location = useLocation();
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  const handleLogout = () => {
    dispatch(logout());
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <div className="w-16 bg-blue-600 flex flex-col items-center py-4 space-y-4">
      {navItems.map((item) => {
        const Icon = item.icon;
        return (
          <button
            key={item.path}
            onClick={() => navigate(item.path)}
            className={`p-2 rounded-lg hover:bg-blue-700 transition-colors ${
              location.pathname === item.path ? 'bg-blue-700' : ''
            }`}
            title={item.label}
          >
            <Icon className="w-6 h-6 text-white" />
          </button>
        );
      })}
      <button
        onClick={handleLogout}
        className="mt-auto p-2 rounded-lg hover:bg-blue-700 transition-colors"
        title="Déconnexion"
      >
        <List className="w-6 h-6 text-white" />
      </button>
    </div>
  );
}