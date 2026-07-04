import React, { useState } from 'react'
import { useForm } from 'react-hook-form';
import { registerUser } from '../api/adminApi';
import { useNavigate } from 'react-router-dom';

import FormField from "@/components/forms/FormField.jsx";
import Input from "@/components/forms/Input.jsx";
import Select from "@/components/forms/Select.jsx";
import SubmitButton from "@/components/forms/SubmitButton.jsx";

function UserRegisterPage() {

    const [ serverError, setServerError] = useState(null);
    const navigate = useNavigate();

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting }
    } = useForm();

    const onSubmit = async (data) => {
        try {
            setServerError(null);
            const response = await registerUser(data);
            console.log(`${data.username} registered with user id ${response.user_id}`);
            navigate("/");
        } catch(err) {
            console.error(err);
            serverError(
                err?.response?.data?.detail ||
                "Invalid credentials"
            )
        }
    }

  return (

    <div className="flex min-h-5 items-center justify-center bg-slate-50">
        <div className="w-full max-w-md rounded-lg border border-slate-200 bg-white shadow-sm">

            <div className="mb-4text-center bg-blue-100 h-25 flex flex-col items-center justify-center rounded-t-lg p-4">
                <h1 className="text-3xl font-bold text-blue-700">
                    Hospital ERP
                </h1>

                <p className="mt-2 text-gray-500">
                    Register new user
                </p>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 p-8" >
                <FormField
                    label="Username"
                    required
                    error={errors.username}
                >
                    <Input {...register("username")} />
                </FormField>

                <FormField
                    label="Email"
                    required
                    error={errors.email}
                >
                    <Input type="email" {...register("email")} />
                </FormField>

                <FormField
                    label="Password"
                    required
                    error={errors.password}
                >
                    <Input type="password" {...register("password")} />
                </FormField>

                <FormField
                    label="Role"
                    required
                    error={errors.role}
                >
                    <Select {...register("role")}>
                        <option value="">Select Role</option>
                        <option value="DOCTOR">Doctor</option>
                        <option value="RECEPTIONIST">Receptionist</option>
                        <option value="ADMIN">Admin</option>
                    </Select>
                </FormField>

                {serverError && (
                    <div className="rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-600">
                        {serverError}
                    </div>
                )}                  

                <SubmitButton isLoading={isSubmitting} className="w-full">
                    {isSubmitting ? "Registering..." : "Register"}
                </SubmitButton>

            </form>
        </div>
    </div>
  )
}

export default UserRegisterPage