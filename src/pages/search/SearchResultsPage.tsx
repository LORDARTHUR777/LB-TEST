import React, { useState } from 'react';
import { Search, List, Send, MessageCircle, PieChart, DollarSign, Settings, Bell } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface Profile {
  id: number;
  name: string;
  imageUrl: string;
}

// Données simulées pour l'exemple
const profiles: Profile[] = Array.from({ length: 321 }, (_, i) => ({
  id: i + 1,
  name: `profile_${i + 1}`,
  imageUrl: `/api/placeholder/150/150`
}));

const existingLists: string[] = [
  'e-commerce mode',
  'Coach de sport',
  'e-commerce CBD',
  'Yoga',
  'e-commerce bijoux',
  'Fleuriste'
];

const SearchResultsPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedProfiles, setSelectedProfiles] = useState(new Set<number>());
  const [isSelectionMode, setIsSelectionMode] = useState(false);
  const [isListDialogOpen, setIsListDialogOpen] = useState(false);
  
  const toggleProfileSelection = (profileId: number): void => {
    if (!isSelectionMode) return;
    
    const newSelection = new Set(selectedProfiles);
    if (newSelection.has(profileId)) {
      newSelection.delete(profileId);
    } else {
      newSelection.add(profileId);
    }
    setSelectedProfiles(newSelection);
  };

  const handleSelectAll = (): void => {
    if (selectedProfiles.size === profiles.length) {
      setSelectedProfiles(new Set());
    } else {
      setSelectedProfiles(new Set(profiles.map(p => p.id)));
    }
  };

  const handleAddToList = (): void => {
    setIsListDialogOpen(true);
  };

  const handleAddToExistingList = (listName: string): void => {
    console.log('Adding selected profiles to list:', listName);
    setIsListDialogOpen(false);
    setSelectedProfiles(new Set());
    setIsSelectionMode(false);
  };

  return (
    <div className="flex h-screen bg-gray-900">
      {/* Sidebar */}
      <div className="w-16 bg-blue-600 flex flex-col items-center py-4 space-y-8">
        <div className="w-full h-8 flex items-center justify-center text-white font-bold">LB</div>
        <Button variant="ghost" size="icon" className="text-white bg-white/10"><Search className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><List className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><Send className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><MessageCircle className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><PieChart className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white"><DollarSign className="w-5 h-5" /></Button>
        <Button variant="ghost" size="icon" className="text-white mt-auto"><Settings className="w-5 h-5" /></Button>
      </div>

      {/* Main content */}
      <div className="flex-1 p-6">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          {/* Search bar */}
          <div className="flex-1 mx-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                className="w-full h-10 pl-10 pr-4 rounded-lg bg-gray-800 border-0 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Find a brand by name..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>
          
          {/* User profile */}
          <div className="flex items-center gap-4">
            <Bell className="w-5 h-5 text-gray-400" />
            <div className="w-8 h-8 rounded-full bg-orange-500 flex items-center justify-center text-white">
              AL
            </div>
          </div>
        </div>

        {/* Results header */}
        <div className="flex justify-between items-center mb-6">
          <div className="text-gray-300">321 matches</div>
          <div className="flex gap-3">
            {isSelectionMode && (
              <>
                <Button
                  onClick={handleAddToList}
                  className="bg-blue-600 text-white"
                >
                  Add to list
                </Button>
                <Button
                  onClick={handleSelectAll}
                  className="bg-blue-600 text-white"
                >
                  Select all
                </Button>
              </>
            )}
            <Button
              onClick={() => setIsSelectionMode(!isSelectionMode)}
              className="bg-blue-600 text-white"
            >
              Select profiles
            </Button>
          </div>
        </div>

        {/* Profiles grid */}
        <div className="grid grid-cols-9 gap-4">
          {profiles.map((profile) => (
            <div
              key={profile.id}
              className={`
                relative aspect-square rounded-lg overflow-hidden cursor-pointer
                ${isSelectionMode ? 'hover:ring-2 hover:ring-blue-500' : ''}
                ${selectedProfiles.has(profile.id) ? 'ring-2 ring-blue-500' : ''}
              `}
              onClick={() => toggleProfileSelection(profile.id)}
            >
              <img
                src={profile.imageUrl}
                alt={profile.name}
                className="w-full h-full object-cover"
              />
              <div className="absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-black/80 to-transparent">
                <div className="text-white text-sm truncate">{profile.name}</div>
                <div className="text-gray-300 text-xs">followers</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* List selection dialog */}
      <Dialog open={isListDialogOpen} onOpenChange={setIsListDialogOpen}>
        <DialogContent className="bg-gray-800 text-white">
          <DialogHeader>
            <DialogTitle>Add to list</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              {existingLists.map((list) => (
                <Button
                  key={list}
                  className="w-full bg-gray-700 hover:bg-gray-600"
                  onClick={() => handleAddToExistingList(list)}
                >
                  {list}
                </Button>
              ))}
            </div>

            <Button 
              className="w-full bg-blue-600 hover:bg-blue-700"
              onClick={() => setIsListDialogOpen(false)}
            >
              Add
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default SearchResultsPage;