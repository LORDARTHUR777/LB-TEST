import { useState, ChangeEvent } from 'react';
import { Search, List, Send, MessageCircle, PieChart, DollarSign, Settings, User, CreditCard, Bell, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Switch } from '@/components/ui/switch';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface FormData {
  email: string;
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
  notifications: boolean;
  marketingEmails: boolean;
}

interface SubscriptionInfo {
  plan: string;
  status: string;
  nextBilling: string;
  amount: string;
}

const SettingsPage = () => {
  const [formData, setFormData] = useState<FormData>({
    email: 'utilisateur@example.com',
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
    notifications: true,
    marketingEmails: false
  });

  const [subscriptionInfo] = useState<SubscriptionInfo>({
    plan: 'Pro',
    status: 'Actif',
    nextBilling: '22 Décembre 2024',
    amount: '49.99€'
  });

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }));
  };

  return (
    <div className="flex h-screen bg-gray-900">
      {/* Sidebar */}
      <div className="w-16 bg-blue-600 flex flex-col items-center py-4 space-y-8">
        <div className="w-full h-8 flex items-center justify-center text-white font-bold">LB</div>
        <Button variant="ghost" size="icon" className="text-white"><Search className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><List className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><Send className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><MessageCircle className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><PieChart className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><DollarSign className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white bg-white/10 mt-auto"><Settings className="w-5 h-5" /></Button>
      </div>

      {/* Main content */}
      <div className="flex-1 p-6 space-y-6 overflow-y-auto">
        <div className="grid grid-cols-3 gap-6">
          {/* Section Compte */}
          <Card className="col-span-2 bg-gray-800/50">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <User className="w-5 h-5" />
                Paramètres du compte
              </CardTitle>
              <CardDescription className="text-gray-400">
                Gérez vos informations personnelles et vos préférences de sécurité
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label htmlFor="email" className="text-sm text-gray-400 mb-2 block">Email</label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="bg-gray-700 border-gray-600 text-white"
                />
              </div>
              
              <div>
                <label htmlFor="currentPassword" className="text-sm text-gray-400 mb-2 block">Mot de passe actuel</label>
                <Input
                  id="currentPassword"
                  type="password"
                  name="currentPassword"
                  value={formData.currentPassword}
                  onChange={handleInputChange}
                  className="bg-gray-700 border-gray-600 text-white"
                />
              </div>
              
              <div>
                <label htmlFor="newPassword" className="text-sm text-gray-400 mb-2 block">Nouveau mot de passe</label>
                <Input
                  id="newPassword"
                  type="password"
                  name="newPassword"
                  value={formData.newPassword}
                  onChange={handleInputChange}
                  className="bg-gray-700 border-gray-600 text-white"
                />
              </div>
              
              <div>
                <label htmlFor="confirmPassword" className="text-sm text-gray-400 mb-2 block">Confirmer le nouveau mot de passe</label>
                <Input
                  id="confirmPassword"
                  type="password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  className="bg-gray-700 border-gray-600 text-white"
                />
              </div>

              <Button className="bg-blue-600 hover:bg-blue-700 text-white mt-4">
                Sauvegarder les modifications
              </Button>
            </CardContent>
          </Card>

          {/* Section Abonnement */}
          <div className="space-y-6">
            <Card className="bg-gray-800/50">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <CreditCard className="w-5 h-5" />
                  Abonnement
                </CardTitle>
                <CardDescription className="text-gray-400">
                  Gérez votre plan et vos paiements
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-400">Plan actuel</span>
                  <span className="text-white font-medium">{subscriptionInfo.plan}</span>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-400">Status</span>
                  <span className="text-green-500 font-medium">{subscriptionInfo.status}</span>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-400">Prochain paiement</span>
                  <span className="text-white">{subscriptionInfo.nextBilling}</span>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-400">Montant</span>
                  <span className="text-white font-medium">{subscriptionInfo.amount}</span>
                </div>
                <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white mt-4">
                  Gérer l'abonnement
                </Button>
              </CardContent>
            </Card>

            {/* Section Notifications */}
            <Card className="bg-gray-800/50">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Bell className="w-5 h-5" />
                  Notifications
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <div className="text-white">Notifications par email</div>
                    <div className="text-gray-400 text-sm">Recevoir des notifications de suivi</div>
                  </div>
                  <Switch
                    checked={formData.notifications}
                    onCheckedChange={(checked: boolean) => 
                      setFormData(prev => ({ ...prev, notifications: checked }))
                    }
                  />
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <div className="text-white">Emails marketing</div>
                    <div className="text-gray-400 text-sm">Recevoir des nouvelles et mises à jour</div>
                  </div>
                  <Switch
                    checked={formData.marketingEmails}
                    onCheckedChange={(checked: boolean) => 
                      setFormData(prev => ({ ...prev, marketingEmails: checked }))
                    }
                  />
                </div>
              </CardContent>
            </Card>

            {/* Bouton de déconnexion */}
            <Button variant="destructive" className="w-full flex items-center justify-center gap-2">
              <LogOut className="w-4 h-4" />
              Se déconnecter
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;