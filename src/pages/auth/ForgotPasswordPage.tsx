import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Card } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ButtonLoading } from "@/components/ui/button-loading"
import { Input } from "@/components/ui/input"
import { useToast } from "@/hooks/use-toast"
import { useAuthError } from "@/hooks/useAuthError"
import { authService } from "@/services/auth.service"
import { ForgotPasswordFormInputs, forgotPasswordSchema } from "@/types/auth.types"

export default function ForgotPasswordPage() {
  const { toast } = useToast()
  const [isLoading, setIsLoading] = useState(false)
  const { error, handleError, clearError } = useAuthError()
  
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<ForgotPasswordFormInputs>({
    resolver: zodResolver(forgotPasswordSchema)
  })

  const onSubmit = async (data: ForgotPasswordFormInputs) => {
    try {
      setIsLoading(true)
      clearError()
      await authService.forgotPassword(data.email)
      toast({
        variant: "success",
        title: "Email envoyé",
        description: "Si un compte existe avec cet email, vous recevrez les instructions pour réinitialiser votre mot de passe."
      })
    } catch (err) {
      handleError(err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-md p-6 space-y-4">
      <h1 className="text-2xl font-bold text-center">Mot de passe oublié</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {error?.message && (
          <Alert variant="destructive">
            <AlertDescription>{error.message}</AlertDescription>
          </Alert>
        )}
        
        <div className="space-y-2">
          <Input
            {...register("email")}
            type="email"
            placeholder="Email"
            error={errors.email?.message}
          />
        </div>

        <ButtonLoading 
          type="submit"
          className="w-full"
          loading={isLoading}
        >
          {isLoading ? "Envoi..." : "Envoyer les instructions"}
        </ButtonLoading>
      </form>
    </Card>
  )
}