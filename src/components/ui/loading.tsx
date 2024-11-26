// src/components/ui/loading.tsx
import { Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface LoadingProps {
  size?: 'sm' | 'md' | 'lg';
  fullScreen?: boolean;
  className?: string;
}

const sizeMap = {
  sm: 'w-4 h-4',
  md: 'w-8 h-8',
  lg: 'w-12 h-12'
};

export const Loading = ({ 
  size = 'md',
  fullScreen = false,
  className 
}: LoadingProps) => {
  const Wrapper = fullScreen ? LoadingFullScreen : LoadingInline;
  return (
    <Wrapper>
      <Loader2 
        className={cn(
          "animate-spin text-blue-500",
          sizeMap[size],
          className
        )} 
      />
    </Wrapper>
  );
};

const LoadingInline = ({ children }: { children: React.ReactNode }) => (
  <div className="flex justify-center items-center p-4">
    {children}
  </div>
);

const LoadingFullScreen = ({ children }: { children: React.ReactNode }) => (
  <div className="fixed inset-0 flex justify-center items-center bg-gray-900/50 z-50">
    {children}
  </div>
);

// Composant spinner plus petit pour les boutons
export const ButtonSpinner = () => (
  <Loader2 className="w-4 h-4 animate-spin mr-2" />
);
