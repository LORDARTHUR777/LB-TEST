// src/components/ui/button-loading.tsx
import { forwardRef } from "react"
import { Button, ButtonProps } from "./button"
import { ButtonSpinner } from "./loading"
import { cn } from "@/lib/utils"

export interface ButtonLoadingProps extends ButtonProps {
  loading?: boolean;
  children: React.ReactNode;
}

const ButtonLoading = forwardRef<HTMLButtonElement, ButtonLoadingProps>(
  ({ className, loading = false, disabled, children, ...props }, ref) => {
    return (
      <Button
        ref={ref}
        className={cn("relative", className)}
        disabled={loading || disabled}
        {...props}
      >
        {loading && <ButtonSpinner />}
        <span className={cn(loading && "opacity-80")}>
          {children}
        </span>
      </Button>
    )
  }
)
ButtonLoading.displayName = "ButtonLoading"

export { ButtonLoading }
