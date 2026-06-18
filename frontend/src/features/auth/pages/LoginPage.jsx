import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { loginSchema } from "../validation/loginSchema";
import { loginUser } from "../api/authApi";

import { useAuthStore } from "@/store/authStore";

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
      userId: "",
      password: "",
    },
  });

  const onSubmit = async (data) => {
    try {
      setServerError("");

      const response = await loginUser(data);

      login(response.access_token);

      // navigate("/dashboard");
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
    <div className="flex min-h-screen items-center justify-center bg-slate-50">
      <div className="w-full max-w-md rounded-lg border bg-white p-8 shadow-sm">

        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold">
            Hospital ERP
          </h1>

          <p className="mt-2 text-gray-500">
            Sign in to your account
          </p>
        </div>

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="space-y-4"
        >
          {/* userId */}
          <div>
            <label htmlFor="userId" className="mb-1 block">
              User Id
            </label>

            <input
              type="text"
              id="userId"
              {...register("userId")}
              placeholder="DOC-2026-00001"
              className="w-full rounded-md border p-2"
            />

            {errors.userId && (
              <p className="mt-1 text-sm text-red-500">
                {errors.userId.message}
              </p>
            )}
          </div>

          {/* Password */}
          <div>
            <label className="mb-1 block">
              Password
            </label>

            <input
              type="password"
              {...register("password")}
              placeholder="Enter password"
              className="w-full rounded-md border p-2"
            />

            {errors.password && (
              <p className="mt-1 text-sm text-red-500">
                {errors.password.message}
              </p>
            )}
          </div>

          {/* Server Error */}
          {serverError && (
            <div className="rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-600">
              {serverError}
            </div>
          )}

          {/* Submit */}
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-md bg-black px-4 py-2 text-white disabled:opacity-50"
          >
            {isSubmitting
              ? "Signing In..."
              : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;