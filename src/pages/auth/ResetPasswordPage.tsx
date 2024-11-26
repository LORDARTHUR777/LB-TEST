// ResetPasswordPage.tsx
import { useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Card } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ButtonLoading } from "@/components/ui/button-loading"
import { Input } from "@/components/ui/input"
import { useToast } from "@/hooks/use-toast"
import { useAuthError } from "@/hooks/useAuthError"
import { authService } from "@/services/auth.service"
import { ResetPasswordFormInputs, resetPasswordSchema } from "@/types/auth.types"

export default function ResetPasswordPage() {
  const navigate = useNavigate()
  const { token } = useParams()
  const { toast } = useToast()
  const [isLoading, setIsLoading] = useState(false)
  const { error, handleError, clearError } = useAuthError()

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<ResetPasswordFormInputs>({
    resolver: zodResolver(resetPasswordSchema)
  })

  const onSubmit = async (data: ResetPasswordFormInputs) => {
    if (!token) {
      handleError(new Error("Token de réinitialisation manquant"))
      return
    }

    try {
      setIsLoading(true)
      clearError()
      await authService.resetPassword({ token, password: data.password })
      toast({
        variant: "success",
        title: "Succès",
        description: "Votre mot de passe a été réinitialisé. Vous pouvez maintenant vous connecter."
      })
      navigate("/login")
    } catch (err) {
      handleError(err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-md p-6 space-y-4">
      <h1 className="text-2xl font-bold text-center">Réinitialisation du mot de passe</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {error?.message && (
          <Alert variant="destructive">
            <AlertDescription>{error.message}</AlertDescription>
          </Alert>
        )}
        
        <div className="space-y-2">
          <Input
            {...register("password")}
            type="password"
            placeholder="Nouveau mot de passe"
            error={errors.password?.message}
          />
          <Input
            {...register("confirmPassword")}
            type="password"
            placeholder="Confirmer le mot de passe"
            error={errors.confirmPassword?.message}
          />
        </div>

        <ButtonLoading
          type="submit"
          className="w-full"
          loading={isLoading}
        >
          {isLoading ? "Réinitialisation..." : "Réinitialiser le mot de passe"}
        </ButtonLoading>
      </form>
    </Card>
  )
}