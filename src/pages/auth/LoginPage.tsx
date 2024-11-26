import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Card } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ButtonLoading } from "@/components/ui/button-loading"
import { Input } from "@/components/ui/input"
import { useToast } from "@/hooks/use-toast"
import { useAuthError } from "@/hooks/useAuthError"
import { authService } from "@/services/auth.service"
import { LoginFormInputs, loginSchema } from "@/types/auth.types"

export default function LoginPage() {
  const navigate = useNavigate()
  const { toast } = useToast()
  const [isLoading, setIsLoading] = useState(false)
  const { error, handleError, clearError } = useAuthError()

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<LoginFormInputs>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      rememberMe: false
    }
  })

  const onSubmit = async (data: LoginFormInputs) => {
    try {
      setIsLoading(true)
      clearError()
      await authService.login(data)
      toast({
        variant: "success",
        title: "Succès",
        description: "Vous êtes maintenant connecté"
      })
      navigate("/dashboard")
    } catch (err) {
      handleError(err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-md p-6 space-y-4">
      <h1 className="text-2xl font-bold text-center">Connexion</h1>
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
          <Input
            {...register("password")}
            type="password"
            placeholder="Mot de passe"
            error={errors.password?.message}
          />
        </div>

        <ButtonLoading 
          type="submit"
          className="w-full"
          loading={isLoading}
        >
          {isLoading ? "Connexion..." : "Se connecter"}
        </ButtonLoading>
      </form>
    </Card>
  )
}