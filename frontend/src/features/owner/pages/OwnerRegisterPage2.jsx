import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate, Link } from "react-router-dom";

import { zodResolver } from "@hookform/resolvers/zod";

import {
  Building2,
  ShieldCheck,
  CalendarDays,
  Users,
  Pill,
  ChevronRight,
  Mail,
  Phone,
  User,
  Lock,
  Eye,
  EyeOff,
} from "lucide-react";

import FormField from "@/components/forms/FormField";
import Input from "@/components/forms/Input";
import SubmitButton from "@/components/forms/SubmitButton";

import { registerOwner } from "../api/ownerApi";
import { ownerRegisterSchema } from "../validation/ownerSchema";

function OwnerRegisterPage() {
  const navigate = useNavigate();

  const [serverError, setServerError] = useState(null);

  const {
    register,
    handleSubmit,
    formState: {
      errors,
      isSubmitting,
    },
  } = useForm({
    resolver: zodResolver(ownerRegisterSchema),
  });

  const onSubmit = async (data) => {
    try {
      setServerError(null);

      await registerOwner(data);

      navigate("/auth/login");
    } catch (err) {
      setServerError(err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-slate-50 to-sky-100">

      <div className="mx-auto flex min-h-screen max-w-7xl items-center justify-center px-6 py-12">

        <div className="grid w-full overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-2xl lg:grid-cols-2">

          {/* ================= LEFT PANEL ================= */}

          <div className="hidden lg:flex flex-col gap-6 justify-between bg-gradient-to-br from-slate-950 via-slate-900 to-blue-900 p-12 text-white">

            <div>

              <div className="mb-10 flex items-center gap-4">

                <div className="rounded-2xl bg-white/20 p-4 backdrop-blur">
                  <Building2 size={36} />
                </div>

                <div>
                  <h1 className="text-3xl font-bold">
                    Hospital ERP
                  </h1>

                  <p className="text-blue-100">
                    Hospital Management System
                  </p>
                </div>

              </div>

              <h2 className="max-w-md text-5xl font-bold leading-tight">
                Build your hospital's digital workspace.
              </h2>

              <p className="mt-6 max-w-md text-lg text-blue-100">
                Manage patients, appointments, pharmacy,
                laboratory, billing and staff from one secure
                platform.
              </p>

              <div className="mt-10 space-y-5">

                <Feature
                  icon={<Users size={20} />}
                  text="Patient & Staff Management"
                />

                <Feature
                  icon={<CalendarDays size={20} />}
                  text="Appointment Scheduling"
                />

                <Feature
                  icon={<Pill size={20} />}
                  text="Pharmacy & Inventory"
                />

                <Feature
                  icon={<ShieldCheck size={20} />}
                  text="Secure Role-Based Access"
                />

              </div>

            </div>

            <div className="rounded-2xl border border-white/20 bg-white/10 p-6 backdrop-blur">

              <p className="text-lg font-semibold">
                Trusted Healthcare Platform
              </p>

              <p className="mt-2 text-blue-100">
                Designed to simplify hospital operations while
                keeping patient information secure.
              </p>

            </div>

          </div>

          {/* ================= RIGHT PANEL ================= */}

          <div className="flex items-center justify-center p-8 md:p-12">

            <div className="w-full max-w-xl">

              <h2 className="text-4xl font-bold text-slate-900">
                Create Hospital Account
              </h2>

              <p className="mt-3 text-slate-600">
                Register your hospital and start managing
                everything from one place.
              </p>

              {serverError && (
                <div className="mt-6 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600">
                  {serverError}
                </div>
              )}

              <form
                onSubmit={handleSubmit(onSubmit)}
                className="mt-8 space-y-6"
              >

                <div className="grid gap-5 sm:grid-cols-2">

                <div className="sm:col-span-2">
                    <FormField
                    label="Hospital Name"
                    required
                    error={errors.hospital_name}
                    >
                    <Input
                        {...register("hospital_name")}
                        placeholder="ABC Multi Speciality Hospital"
                    />
                    </FormField>
                </div>

                <FormField
                    label="First Name"
                    required
                    error={errors.owner_first_name}
                >
                    <Input
                    {...register("owner_first_name")}
                    placeholder="John"
                    />
                </FormField>

                <FormField
                    label="Last Name"
                    error={errors.owner_last_name}
                >
                    <Input
                    {...register("owner_last_name")}
                    placeholder="Doe"
                    />
                </FormField>

                <div className="sm:col-span-2">
                    <FormField
                    label="Email Address"
                    required
                    error={errors.owner_email}
                    >
                    <Input
                        {...register("owner_email")}
                        type="email"
                        placeholder="john@example.com"
                    />
                    </FormField>
                </div>

                <div className="sm:col-span-2">
                    <FormField
                    label="Phone Number"
                    error={errors.owner_phone}
                    >
                    <Input
                        {...register("owner_phone")}
                        placeholder="+91 9876543210"
                    />
                    </FormField>
                </div>

                <FormField
                    label="Password"
                    required
                    error={errors.owner_password}
                >
                    <Input
                    {...register("owner_password")}
                    type="password"
                    placeholder="••••••••"
                    />
                </FormField>

                <FormField
                    label="Confirm Password"
                    required
                    error={errors.owner_password_confirm}
                >
                    <Input
                    {...register("owner_password_confirm")}
                    type="password"
                    placeholder="••••••••"
                    />
                </FormField>

                </div>

                <div className="rounded-xl bg-slate-50 border border-slate-200 p-4">

                    <p className="text-sm text-slate-600">
                        By creating an account, you agree to our
                        <span className="font-semibold text-blue-600 cursor-pointer">
                        {" "}Terms of Service
                        </span>
                        {" "}and
                        <span className="font-semibold text-blue-600 cursor-pointer">
                        {" "}Privacy Policy
                        </span>.
                    </p>

                </div>

                <SubmitButton
                  isLoading={isSubmitting}
                  className="flex w-full items-center justify-center gap-2"
                >
                  Create Hospital

                  <ChevronRight size={18} />
                </SubmitButton>

              </form>

              <p className="mt-8 text-center text-sm text-slate-600">

                Already have an account?

                <Link
                  to="/auth/login"
                  className="ml-2 font-semibold text-blue-600 hover:text-blue-700"
                >
                  Sign In
                </Link>

              </p>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

function Feature({ icon, text }) {
  return (
    <div className="flex items-center gap-4">

      <div className="rounded-xl bg-white/15 p-3">
        {icon}
      </div>

      <p className="text-lg">
        {text}
      </p>

    </div>
  );
}

export default OwnerRegisterPage;