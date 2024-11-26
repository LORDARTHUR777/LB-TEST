import { useState, useRef } from 'react';
import { Search, List, Send, MessageCircle, PieChart, DollarSign, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface MessageType {
  id: string;
  label: string;
  color: string;
}

interface Prospect {
  id: number;
  account: string;
  list: string;
  status: string;
  messages: Record<string, string>;
}

const messageTypes: MessageType[] = [
  { id: 'first', label: '1er message', color: 'bg-blue-500' },
  { id: 'follow1', label: '1er Follow-up', color: 'bg-blue-500' },
  { id: 'follow2', label: '2ème Follow-up', color: 'bg-blue-500' },
  { id: 'follow3', label: '3ème Follow-up', color: 'bg-blue-500' },
  { id: 'follow4', label: '4ème Follow-up', color: 'bg-blue-500' },
  { id: 'lead', label: 'Lead chaud', color: 'bg-green-500' },
  { id: 'notInterested', label: 'Pas intéressé', color: 'bg-red-500' }
];

const FollowUpPage = () => {
  const [prospectData, setProspectData] = useState<Prospect[]>([
    {
      id: 1,
      account: 'floracbd',
      list: 'e-commerce CBD',
      status: '',
      messages: {}
    },
    // ... autres prospects
  ]);

  const scrollRef = useRef<HTMLDivElement>(null);

  const getDates = (): Date[] => {
    const dates: Date[] = [];
    for (let i = 0; i < 15; i++) {
      const date = new Date();
      date.setDate(date.getDate() + i);
      dates.push(date);
    }
    return dates;
  };

  const dates = getDates();

  const getStatusColor = (status: string): string => {
    const messageType = messageTypes.find(t => t.label === status);
    return messageType ? messageType.color : 'bg-gray-600';
  };

  const handleMessageSelect = (prospectId: number, date: Date, messageTypeId: string) => {
    setProspectData(prevData => {
      return prevData.map(prospect => {
        if (prospect.id === prospectId) {
          const newMessages = {
            ...prospect.messages,
            [date.toISOString()]: messageTypeId
          };

          const sortedDates = Object.keys(newMessages)
            .filter(dateKey => newMessages[dateKey] !== 'none')
            .sort((a, b) => new Date(b).getTime() - new Date(a).getTime());

          let newStatus = '';
          if (sortedDates.length > 0) {
            const latestMessageType = messageTypes.find(
              type => type.id === newMessages[sortedDates[0]]
            );
            newStatus = latestMessageType ? latestMessageType.label : '';
          }

          return {
            ...prospect,
            messages: newMessages,
            status: newStatus
          };
        }
        return prospect;
      });
    });
  };

  return (
    <div className="flex h-screen bg-gray-900">
      {/* Sidebar */}
      <div className="w-16 bg-blue-600 flex flex-col items-center py-4 space-y-8">
        <div className="w-full h-8 flex items-center justify-center text-white font-bold">
          LB
        </div>
        <Button variant="ghost" size="icon" className="text-white" aria-label="Search">
          <Search className="w-5 h-5" />
        </Button>
        <Button variant="ghost" size="icon" className="text-white bg-white/10" aria-label="Lists">
          <List className="w-5 h-5" />
        </Button>
        <Button variant="ghost" size="icon" className="text-white" aria-label="Send">
          <Send className="w-5 h-5" />
        </Button>
        <Button variant="ghost" size="icon" className="text-white" aria-label="Messages">
          <MessageCircle className="w-5 h-5" />
        </Button>
        <Button variant="ghost" size="icon" className="text-white" aria-label="Analytics">
          <PieChart className="w-5 h-5" />
        </Button>
        <Button variant="ghost" size="icon" className="text-white" aria-label="Billing">
          <DollarSign className="w-5 h-5" />
        </Button>
        <Button variant="ghost" size="icon" className="text-white mt-auto" aria-label="Settings">
          <Settings className="w-5 h-5" />
        </Button>
      </div>

      {/* Main content */}
      <div className="flex-1 p-6 overflow-hidden">
        <div className="relative overflow-hidden rounded-lg">
          <div className="flex">
            {/* Fixed columns */}
            <div className="relative" style={{ width: "600px", minWidth: "600px" }}>
              <table className="w-full">
                <thead>
                  <tr className="text-left">
                    <th className="w-64 p-4 bg-gray-800 rounded-lg mr-2" scope="col">
                      <span className="text-gray-400 font-normal">Compte Instagram</span>
                    </th>
                    <th className="w-48 p-4 bg-gray-800 rounded-lg mx-2" scope="col">
                      <span className="text-gray-400 font-normal">Liste</span>
                    </th>
                    <th className="w-48 p-4 bg-gray-800 rounded-lg mx-2" scope="col">
                      <span className="text-gray-400 font-normal">Statut</span>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {prospectData.map(prospect => (
                    <tr key={prospect.id} className="text-white">
                      <td className="w-64 p-4 bg-gray-800 rounded-lg mr-2">
                        {prospect.account}
                      </td>
                      <td className="w-48 p-4 bg-gray-800 rounded-lg mx-2">
                        {prospect.list}
                      </td>
                      <td className="w-48 p-4 bg-gray-800 rounded-lg mx-2">
                        <div className={`px-3 py-1 rounded-full text-sm inline-block ${getStatusColor(prospect.status)}`}>
                          {prospect.status || 'Non contacté'}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Scrollable date columns */}
            <div className="flex-1 overflow-x-auto" ref={scrollRef}>
              <table className="w-full">
                <thead>
                  <tr className="text-left">
                    {dates.map(date => (
                      <th 
                        key={date.toISOString()} 
                        className="p-4 bg-gray-800 rounded-lg mx-1" 
                        style={{ minWidth: "200px" }}
                        scope="col"
                      >
                        <span className="text-gray-400 font-normal">
                          {date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })}
                        </span>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {prospectData.map(prospect => (
                    <tr key={prospect.id}>
                      {dates.map(date => (
                        <td 
                          key={date.toISOString()} 
                          className="p-4 bg-gray-800 rounded-lg mx-1"
                          style={{ minWidth: "200px" }}
                        >
                          <Select
                            value={prospect.messages[date.toISOString()] || 'none'}
                            onValueChange={(value) => handleMessageSelect(prospect.id, date, value)}
                          >
                            <SelectTrigger className="w-full">
                              <SelectValue placeholder="Sélectionner" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="none">Aucun message</SelectItem>
                              {messageTypes.map(type => (
                                <SelectItem key={type.id} value={type.id}>
                                  {type.label}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FollowUpPage;