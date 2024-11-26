// src/pages/NotFoundPage.tsx
import { useNavigate } from 'react-router-dom';
import { MoveLeft, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';

const NotFoundPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 px-4">
      <div className="text-center space-y-8">
        <div className="relative">
          {/* Numéro d'erreur 404 */}
          <div className="text-[150px] font-bold text-gray-700/20">404</div>
          
          {/* Icône superposée */}
          <div className="absolute inset-0 flex items-center justify-center">
            <Search className="w-24 h-24 text-gray-500" />
          </div>
        </div>

        {/* Message d'erreur */}
        <div className="space-y-4">
          <h1 className="text-3xl font-bold text-white">Page non trouvée</h1>
          <p className="text-gray-400 max-w-md mx-auto">
            Désolé, la page que vous recherchez semble avoir disparu dans
            l'espace numérique. Vérifions d'autres endroits !
          </p>
        </div>

        {/* Boutons d'action */}
        <div className="flex justify-center gap-4">
          <Button
            onClick={() => navigate(-1)}
            variant="outline"
            className="flex items-center gap-2"
          >
            <MoveLeft className="w-4 h-4" />
            Retour
          </Button>
          
          <Button
            onClick={() => navigate('/search')}
            className="bg-blue-600 hover:bg-blue-700 text-white flex items-center gap-2"
          >
            <Search className="w-4 h-4" />
            Page de recherche
          </Button>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage;
