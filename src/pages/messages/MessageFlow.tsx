import * as React from "react";
import { useState, useRef, useEffect } from "react";
import { Search, List, Send, MessageCircle, PieChart, DollarSign, Settings, Plus, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface Position {
  x: number;
  y: number;
}

interface Node {
  content: string;
  position: Position;
}

interface Nodes {
  [key: string]: Node;
}

interface ArrowCoordinates {
  startX: number;
  startY: number;
  endX: number;
  endY: number;
}

interface MessageNodeProps {
  id: string;
  content: string;
  position: Position;
  onDragEnd: (id: string, x: number, y: number) => void;
  selected: boolean;
  onClick: (id: string) => void;
  onDelete: (id: string) => void;
  onContentChange: (id: string, content: string) => void;
}

const MessageNode = React.forwardRef<HTMLDivElement, MessageNodeProps>(({
  id,
  content,
  position,
  onDragEnd,
  selected,
  onClick,
  onDelete,
  onContentChange
}, ref) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const dragStartPos = useRef<Position>({ x: 0, y: 0 });
  
  const handleDragStart = (e: React.DragEvent) => {
    const target = e.currentTarget;
    const rect = target.getBoundingClientRect();
    setIsDragging(true);
    dragStartPos.current = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };
  };

  const handleDragEnd = (e: React.DragEvent) => {
    setIsDragging(false);
    const x = e.clientX - dragStartPos.current.x;
    const y = e.clientY - dragStartPos.current.y;
    onDragEnd(id, x, y);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
  };

  const handleBlur = (e: React.FocusEvent<HTMLTextAreaElement>) => {
    setIsEditing(false);
    onContentChange(id, e.target.value);
  };

  return (
    <div
      ref={ref}
      className={cn(
        "absolute p-4 rounded-lg bg-gray-800/90 w-80",
        selected && "ring-2 ring-blue-500"
      )}
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`,
        cursor: isDragging ? "grabbing" : "grab"
      }}
      draggable
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
      onClick={() => onClick(id)}
    >
      <div className="flex justify-between items-center mb-2">
        <div className="text-sm text-gray-400">{id}</div>
        {isEditing && (
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onDelete(id);
            }}
            className="text-red-500 hover:text-red-400"
          >
            <Trash2 className="h-4 w-4" />
            <span className="sr-only">Delete message</span>
          </Button>
        )}
      </div>

      {isEditing ? (
  <div className="relative">
    <label htmlFor={`message-${id}`} className="sr-only">Edit message content</label>
    <textarea
      id={`message-${id}`}
      className="w-full h-32 p-2 mb-4 bg-gray-700 text-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      defaultValue={content}
      onBlur={handleBlur}
      autoFocus
      placeholder="Enter your message content"
      aria-label="Edit message content"
    />
  </div>
) : (
  <div className="text-gray-300 mb-4 min-h-[60px] whitespace-pre-line">
    {content}
  </div>
)}

      <div className="flex gap-2">
        <Button
          variant="secondary"
          className="bg-blue-600 hover:bg-blue-700 text-white"
          onClick={(e) => {
            e.stopPropagation();
            handleCopy();
          }}
        >
          Copy
        </Button>
        <Button
          variant="secondary"
          className="bg-blue-600 hover:bg-blue-700 text-white"
          onClick={(e) => {
            e.stopPropagation();
            setIsEditing(!isEditing);
          }}
        >
          {isEditing ? "Save" : "Edit"}
        </Button>
      </div>
    </div>
  );
});

MessageNode.displayName = "MessageNode";

const Arrow = React.forwardRef<SVGSVGElement, ArrowCoordinates>(({
  startX,
  startY,
  endX,
  endY
}, ref) => (
  <svg
    ref={ref}
    className="absolute top-0 left-0 w-full h-full pointer-events-none"
    style={{ zIndex: -1 }}
  >
    <path
      d={`M ${startX} ${startY} L ${endX} ${endY}`}
      stroke="#4B5563"
      strokeWidth="2"
      fill="none"
      strokeDasharray="5,5"
    />
  </svg>
));

Arrow.displayName = "Arrow";

export const MessageFlow = () => {
  const [nodes, setNodes] = useState<Nodes>({
    'Message 1': {
      content: "Bonjour,\n\nJe vous écris car vous êtes (métier).\n\nJ'ai fait un tour sur votre site et certains points marketing essentiels sont absents.\n\nJ'ai réalisé une vidéo de quelques minutes qui explique ce qui ne va pas sur votre site et comment l'améliorer pour augmenter vos ventes.\n\nEst ce que ça vous intéresserait que je vous l'envoie ?",
      position: { x: 50, y: 50 }
    },
    'Message 2': {
      content: "Ok, top! Je vous l'envoie maintenant. (lien)\n\nJe peux compter sur vous pour me retour une fois que vous l'aurez visionnée ?",
      position: { x: 400, y: 150 }
    },
    'Message 3': {
      content: "Par simple curiosité, quel serait votre objectif de chiffre d'affaires mensuel pour les 6 prochains mois ?",
      position: { x: 400, y: 300 }
    },
    'Message 4': {
      content: "Ce que je vous propose, c'est que nous reparlions dans un prochain message pour me donner vos avis.\n\nConcrètement, l'objectif sera d'analyser votre situation et de voir ensuite comment je pourrais vous aider à atteindre cet/ces mois.\n\nD'ailleurs, l'appel est offert et il n'y a rien à vendre (juste du consulting pour vous aider à développer votre business! )\n\nOn se programme ça ?",
      position: { x: 750, y: 150 }
    },
    'Message 5': {
      content: "Parfait, je vous envoie le lien de mon agenda pour convenir d'un appel!\n\nhttps://calendly.com\n\nSlots pour lundi vous sont réservés.",
      position: { x: 750, y: 400 }
    },
    'Follow-up message': {
      content: "(Prénom) êtes vous toujours là ?",
      position: { x: 50, y: 400 }
    }
  });

  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [connections] = useState<[string, string][]>([
    ['Message 1', 'Message 2'],
    ['Message 2', 'Message 3'],
    ['Message 3', 'Message 4'],
    ['Message 4', 'Message 5']
  ]);

  const [arrows, setArrows] = useState<ArrowCoordinates[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const updateArrows = () => {
      const newArrows = connections.map(([startId, endId]) => {
        const startElement = document.getElementById(startId);
        const endElement = document.getElementById(endId);

        if (!startElement || !endElement || !containerRef.current) return null;

        const startRect = startElement.getBoundingClientRect();
        const endRect = endElement.getBoundingClientRect();
        const containerRect = containerRef.current.getBoundingClientRect();

        return {
          startX: startRect.right - containerRect.left,
          startY: startRect.top + startRect.height / 2 - containerRect.top,
          endX: endRect.left - containerRect.left,
          endY: endRect.top + endRect.height / 2 - containerRect.top
        };
      }).filter((arrow): arrow is ArrowCoordinates => arrow !== null);

      setArrows(newArrows);
    };

    updateArrows();
    
    const observer = new MutationObserver(updateArrows);
    observer.observe(containerRef.current!, { 
      childList: true, 
      subtree: true, 
      attributes: true 
    });
    
    window.addEventListener('resize', updateArrows);
    
    return () => {
      window.removeEventListener('resize', updateArrows);
      observer.disconnect();
    };
  }, [connections, nodes]);

  const handleDragEnd = (id: string, x: number, y: number) => {
    setNodes(prev => ({
      ...prev,
      [id]: {
        ...prev[id],
        position: { x, y }
      }
    }));
  };

  const handleContentChange = (id: string, newContent: string) => {
    setNodes(prev => ({
      ...prev,
      [id]: {
        ...prev[id],
        content: newContent
      }
    }));
  };

  const handleDeleteNode = (id: string) => {
    setNodes(prev => {
      const newNodes = { ...prev };
      delete newNodes[id];
      return newNodes;
    });
  };

  const handleAddSection = () => {
    const existingNumbers = Object.keys(nodes)
      .filter(key => key.startsWith('Message '))
      .map(key => parseInt(key.split(' ')[1]))
      .filter(num => !isNaN(num));
    
    const nextNumber = existingNumbers.length > 0 
      ? Math.max(...existingNumbers) + 1 
      : 1;
    
    const newId = `Message ${nextNumber}`;
    const lastNode = Object.values(nodes)[Object.values(nodes).length - 1];
    const newPosition = {
      x: lastNode.position.x + 50,
      y: lastNode.position.y + 50
    };

    setNodes(prev => ({
      ...prev,
      [newId]: {
        content: "Nouveau message...",
        position: newPosition
      }
    }));
  };

  return (
    <div className="flex h-screen bg-gray-900">
      <nav className="w-16 bg-blue-600 flex flex-col items-center py-4 space-y-8">
        <div className="w-full h-8 flex items-center justify-center text-white font-bold">
          LB
        </div>
        {[
          { icon: Search, label: "Search" },
          { icon: List, label: "List" },
          { icon: Send, label: "Send" },
          { icon: MessageCircle, label: "Messages", active: true },
          { icon: PieChart, label: "Analytics" },
          { icon: DollarSign, label: "Billing" }
        ].map(({ icon: Icon, label, active }) => (
          <Button
            key={label}
            variant="ghost"
            size="icon"
            className={cn(
              "text-white",
              active && "bg-white/10"
            )}
          >
            <Icon className="h-5 w-5" />
            <span className="sr-only">{label}</span>
          </Button>
        ))}
        <Button
          variant="ghost"
          size="icon"
          className="text-white mt-auto"
        >
          <Settings className="h-5 w-5" />
          <span className="sr-only">Settings</span>
        </Button>
      </nav>

      <main className="flex-1 relative p-6">
        <div className="absolute top-4 right-4 z-10">
          <Button
            onClick={handleAddSection}
            className="bg-blue-600 hover:bg-blue-700 text-white"
          >
            <Plus className="h-4 w-4 mr-2" />
            Add section
          </Button>
        </div>

        <div ref={containerRef} className="relative w-full h-full">
          {arrows.map((arrow, index) => (
            <Arrow key={index} {...arrow} />
          ))}
          
          {Object.entries(nodes).map(([id, node]) => (
            <MessageNode
              key={id}
              id={id}
              content={node.content}
              position={node.position}
              onDragEnd={handleDragEnd}
              selected={selectedNode === id}
              onClick={setSelectedNode}
              onDelete={handleDeleteNode}
              onContentChange={handleContentChange}
            />
          ))}
        </div>
      </main>
    </div>
  );
};

export default MessageFlow;