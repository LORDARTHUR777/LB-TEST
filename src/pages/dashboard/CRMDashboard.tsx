import React, { useState } from 'react';
import { Search, List, Send, MessageCircle, PieChart, DollarSign, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';

const timeFilters = [
  { id: 'allTime', label: 'All the time' },
  { id: 'monthToDate', label: 'Month to date' },
  { id: 'week', label: 'Week' },
  { id: 'today', label: 'Today' },
  { id: 'yesterday', label: 'Yesterday' },
  { id: 'custom', label: 'Custom' },
  { id: 'compare', label: 'Compare' }
];

const listData = [
  { name: 'e-commerce mode', count: 131 },
  { name: 'Coach de sport', count: 280 },
  { name: 'Consultant', count: 32 },
  { name: 'e-commerce CBD', count: 125 },
  { name: 'Yoga', count: 82 },
  { name: 'Avocat', count: 93 },
  { name: 'e-commerce bijoux', count: 275 },
  { name: 'Fleuriste', count: 95 },
  { name: 'Graphiste', count: 46 }
];

const funnelData = [
  { stage: '1er message', count: 280 },
  { stage: '1er Follow-up', count: 183 },
  { stage: '2ème Follow-up', count: 128 },
  { stage: '3ème Follow-up', count: 35 },
  { stage: 'Pas intéressé', count: 18 },
  { stage: 'Lead chaud', count: 29 }
];

const kpiData = [
  { label: 'Lead/DM total', value: '10,35%' },
  { label: 'Pas intéressé/DM total', value: '6,42%' },
  { label: 'Pas de réponse', value: '83,21%' }
];

const CRMDashboard = () => {
  const [selectedFilter, setSelectedFilter] = useState('monthToDate');

  return (
    <div className="flex h-screen bg-gray-900">
      {/* Sidebar */}
      <div className="w-16 bg-blue-600 flex flex-col items-center py-4 space-y-8">
        <div className="w-full h-8 flex items-center justify-center text-white font-bold">LB</div>
        <Button variant="ghost" size="icon" className="text-white"><Search className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><List className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><Send className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><MessageCircle className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white bg-white/10"><PieChart className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><DollarSign className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white mt-auto"><Settings className="w-5 h-5" /></Button>
      </div>

      {/* Main content */}
      <div className="flex-1 p-6 space-y-6">
        {/* Lists Overview Card */}
        <Card className="bg-gray-800/50">
          <CardContent className="p-6">
            <h2 className="text-lg text-gray-200 mb-4">Nombre de personnes contactées par liste</h2>
            <div className="grid grid-cols-3 gap-4">
              {listData.map((item, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-800/80 rounded-lg">
                  <span className="text-gray-300">{item.name}</span>
                  <span className="text-blue-500 font-semibold">{item.count}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Time Filters */}
        <div className="flex gap-2">
          {timeFilters.map((filter) => (
            <Button
              key={filter.id}
              variant="ghost"
              className={`
                ${selectedFilter === filter.id ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-300'}
                hover:bg-blue-700
              `}
              onClick={() => setSelectedFilter(filter.id)}
            >
              {filter.label}
            </Button>
          ))}
        </div>

        <div className="grid grid-cols-4 gap-6">
          {/* Funnel */}
          <div className="col-span-3 bg-gray-800/50 rounded-lg p-6">
            <div className="space-y-4">
              {funnelData.map((stage, index) => (
                <div key={index} className="relative">
                  <div 
                    className="bg-blue-600/20 h-16 rounded-lg flex items-center justify-between px-4"
                    style={{
                      width: `${(stage.count / funnelData[0].count) * 100}%`,
                      minWidth: '200px'
                    }}
                  >
                    <span className="text-gray-200">{stage.stage}</span>
                    <span className="text-blue-500 font-semibold">{stage.count}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* KPIs */}
          <div className="space-y-4">
            {kpiData.map((kpi, index) => (
              <div key={index} className="bg-gray-800/50 p-4 rounded-lg">
                <div className="text-gray-400 mb-2">{kpi.label}</div>
                <div className="text-blue-500 text-xl font-semibold">{kpi.value}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CRMDashboard;
