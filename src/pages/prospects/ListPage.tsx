import { useState } from 'react';
import { Search, List, Send, MessageCircle, PieChart, DollarSign, Settings, Plus, Pencil, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";

interface ListItem {
  id: number;
  name: string;
  count: number;
}

const ListPage = () => {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState<boolean>(false);
  const [newListName, setNewListName] = useState<string>('');
  const [lists, setLists] = useState<ListItem[]>([
    { id: 1, name: 'boutique de bijoux', count: 0 },
    { id: 2, name: 'Fleuriste', count: 1 },
    { id: 3, name: 'Institut de beauté', count: 0 }
  ]);
  const [editingList, setEditingList] = useState<ListItem | null>(null);

  const handleCreateList = () => {
    if (newListName.trim()) {
      setLists(prev => [...prev, {
        id: Date.now(),
        name: newListName.trim(),
        count: 0
      }]);
      setNewListName('');
      setIsCreateDialogOpen(false);
    }
  };

  const handleDeleteList = (id: number) => {
    setLists(prev => prev.filter(list => list.id !== id));
  };

  const handleEditList = (list: ListItem) => {
    setEditingList(list);
    setNewListName(list.name);
    setIsCreateDialogOpen(true);
  };

  const handleSaveEdit = () => {
    if (newListName.trim() && editingList) {
      setLists(prev => prev.map(list => 
        list.id === editingList.id ? { ...list, name: newListName.trim() } : list
      ));
      setNewListName('');
      setEditingList(null);
      setIsCreateDialogOpen(false);
    }
  };

  const filteredLists = lists.filter(list => 
    list.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="flex h-screen bg-gray-900">
      {/* Sidebar */}
      <div className="w-16 bg-blue-600 flex flex-col items-center py-4 space-y-8">
        <div className="w-full h-8 flex items-center justify-center text-white font-bold">LB</div>
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
      <div className="flex-1 p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="w-96">
            <Input
              className="bg-gray-800 border-gray-700 text-white"
              placeholder="Find a list by name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              aria-label="Search lists"
            />
          </div>
          <Button
            className="bg-blue-600 hover:bg-blue-700 text-white"
            onClick={() => {
              setEditingList(null);
              setNewListName('');
              setIsCreateDialogOpen(true);
            }}
          >
            <Plus className="w-4 h-4 mr-2" />
            Create a new list
          </Button>
        </div>

        {/* Lists Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredLists.map(list => (
            <div key={list.id} className="bg-gray-800/50 rounded-lg p-4 flex flex-col">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-2">
                  <img
                    src="/api/placeholder/24/24"
                    alt="Instagram"
                    className="rounded"
                  />
                  <span className="text-white">{list.name}</span>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleEditList(list)}
                    className="text-gray-400 hover:text-white"
                    aria-label={`Edit ${list.name}`}
                  >
                    <Pencil className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDeleteList(list.id)}
                    className="text-gray-400 hover:text-red-500"
                    aria-label={`Delete ${list.name}`}
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
              
              <div className="flex-grow">
                {list.count === 0 && (
                  <div className="text-gray-500 text-center py-12">Empty list.</div>
                )}
              </div>

              <div className="flex justify-between items-center mt-4">
                <span className="text-gray-400">{list.count} brands</span>
                <Button
                  className="bg-blue-600 hover:bg-blue-700 text-white"
                  size="sm"
                >
                  Add to campaign
                </Button>
              </div>
            </div>
          ))}
        </div>

        {/* Create/Edit List Dialog */}
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogContent className="bg-gray-800 text-white">
            <DialogHeader>
              <DialogTitle>{editingList ? 'Edit list' : 'Create a new list'}</DialogTitle>
            </DialogHeader>
            <Input
              className="bg-gray-700 border-gray-600 text-white"
              placeholder="List name"
              value={newListName}
              onChange={(e) => setNewListName(e.target.value)}
              aria-label="List name"
            />
            <DialogFooter>
              <Button
                className="bg-blue-600 hover:bg-blue-700 text-white"
                onClick={editingList ? handleSaveEdit : handleCreateList}
              >
                {editingList ? 'Save' : 'Create'}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
};

export default ListPage;