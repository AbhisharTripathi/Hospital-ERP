import React, { useState } from 'react'
import { useForm } from 'react-hook-form';
import { registerUser } from '../api/adminApi';
import { useNavigate } from 'react-router-dom';

import FormField from "@/components/forms/FormField.jsx";
import Input from "@/components/forms/Input.jsx";
import Select from "@/components/forms/Select.jsx";
import Textarea from "@/components/forms/Textarea.jsx";
import SubmitButton from "@/components/forms/SubmitButton.jsx";

function UserRegisterPage() {

    const [ serverError, setServerError] = useState(null);
    const navigate = useNavigate();

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting }
    } = useForm({
        defaultValues: {
            metadata: "{}"
        }
    });

    const departments = [
        "CARDIOLOGY",
        "NEUROLOGY",
        "ONCOLOGY",
        "PEDS",
        "RADIOLOGY",
        "SURGERY",
        "ANESTHESIOLOGY",
        "ORTHEPEDICS",
        "Dermatology",
        "GASTROENTEROLOGY",
        "GYNECOLOGY",
        "ENT",
        "OTHER"
    ];

    const onSubmit = async (data) => {
        try {
            setServerError(null);
            let metadata = {};

            if (data.metadata) {
                try {
                    metadata = JSON.parse(data.metadata);
                } catch (parseError) {
                    setServerError("Metadata must be valid JSON.");
                    return;
                }
            }

            const payload = {
                first_name: data.first_name,
                last_name: data.last_name,
                email: data.email,
                phone: data.phone,
                role: data.role,
                department_id: data.department_id,
                department: data.department,
                address: data.address,
                metadata,
            };

            const response = await registerUser(payload);
            console.log(`${data.first_name} registered with user id ${response.user_id}`);
            navigate("/");
        } catch(err) {
            console.error(err);
            setServerError(
                err?.response?.data?.detail ||
                "Invalid credentials"
            );
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
                    label="First Name"
                    required
                    error={errors.first_name}
                >
                    <Input
                        {...register("first_name", { required: "First name is required" })}
                    />
                </FormField>

                <FormField
                    label="Last Name"
                    error={errors.last_name}
                >
                    <Input {...register("last_name")} />
                </FormField>

                <FormField
                    label="Email"
                    required
                    error={errors.email}
                >
                    <Input type="email" {...register("email", { required: "Email is required" })} />
                </FormField>

                <FormField
                    label="Phone"
                    error={errors.phone}
                >
                    <Input {...register("phone")} />
                </FormField>

                <FormField
                    label="Role"
                    required
                    error={errors.role}
                >
                    <Select {...register("role", { required: "Role is required" })}>
                        <option value="">Select Role</option>
                        <option value="SUPER_ADMIN">Super Admin</option>
                        <option value="ADMIN">Admin</option>
                        <option value="DOCTOR">Doctor</option>
                        <option value="RECEPTIONIST">Receptionist</option>
                    </Select>
                </FormField>

                <FormField
                    label="Department ID"
                    error={errors.department_id}
                >
                    <Input {...register("department_id")} />
                </FormField>

                <FormField
                    label="Department"
                    error={errors.department}
                >
                    <Select {...register("department")} >
                        <option value="">Select</option>
                        {
                            departments.map((dept) => (
                                <option key={dept} value={dept}>{dept}</option>
                            ))
                        }
                    </Select>
                </FormField>

                <FormField
                    label="Address"
                    error={errors.address}
                >
                    <Textarea rows={4} {...register("address")} />
                </FormField>

                <FormField
                    label="Metadata (JSON)"
                    error={errors.metadata}
                >
                    <Textarea
                        rows={4}
                        placeholder='e.g. { "additionalProp1": {} }'
                        {...register("metadata")}
                    />
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