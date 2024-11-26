import { useToast as useToastUI } from "@/components/ui/use-toast";
import type { ToastProps } from "@/types/toast";

export function useToast() {
  const { toast: originalToast } = useToastUI();
  
  return {
    toast: (props: ToastProps) => {
      originalToast({
        ...props,
        duration: props.duration || 3000,
      });
    }
  };
}