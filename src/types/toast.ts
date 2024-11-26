export interface ToastProps {
  id?: string
  title?: string
  description?: string
  variant?: 'success' | 'destructive' | 'default'
  duration?: number
  open?: boolean
  onOpenChange?: (open: boolean) => void
}

export type ToastActionElement = React.ReactElement