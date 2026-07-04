import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { loginSchema } from "../validation/loginSchema";
import { loginUser } from "../api/authApi";

import { useAuthStore } from "@/store/authStore";

import FormField from "@/components/forms/FormField.jsx";
import Input from "@/components/forms/Input.jsx";
import SubmitButton from "@/components/forms/SubmitButton.jsx";


function LoginPage() {
  const navigate = useNavigate();

  const [serverError, setServerError] = useState("");

  // const { user, token, isAuthenticated, login, logout, setUser } = useAuthStore();
  const login = useAuthStore((state) => state.login);

  const {
    register,
    handleSubmit,
    formState: {
      errors,
      isSubmitting,
    },
  } = useForm({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = async (data) => {
    try {
      setServerError("");

      const response = await loginUser(data);
      console.log(response);

      login(response.access_token);

      navigate("/");
    } catch (error) {
      console.error(error);

      setServerError(
        error?.response?.data?.detail ||
          "Invalid credentials"
      );
    }
  };

  return (
    <div className="flex min-h-full items-center justify-center bg-slate-50">
      <div className="w-full max-w-md rounded-lg border border-slate-200 bg-white shadow-sm">

        <div className="mb-4 text-center bg-blue-100 h-25 flex flex-col items-center justify-center rounded-t-lg p-4">
          <h1 className="text-3xl font-bold text-blue-700">
            Hospital ERP
          </h1>

          <p className="mt-2 text-gray-500">
            Sign in to your account
          </p>
        </div>

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="space-y-6 p-8"
        >
          
          <FormField
          label="Email"
          error={errors.email}
          required
          >
            <Input {...register("email")}
              placeholder="Enter your email"
            />
          </FormField>

          <FormField
            label="Password"
            error={errors.password}
            required
          >
            <Input
              type="password"
              {...register("password")}
              placeholder="Enter password"
            />
          </FormField>

          {serverError && (
            <div className="rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-600">
              {serverError}
            </div>
          )}

          <SubmitButton isLoading={isSubmitting} className="w-full">
            Sign In
          </SubmitButton>

        </form>
      </div>
    </div>
  );
}

export default LoginPage;