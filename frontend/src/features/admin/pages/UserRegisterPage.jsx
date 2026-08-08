import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import {
    registerUser,
    createDoctor,
    getDepartments,
} from "@/features/admin/api/adminApi.js";

import FormField from "@/components/forms/FormField";
import Input from "@/components/forms/Input";
import Select from "@/components/forms/Select";
import SubmitButton from "@/components/forms/SubmitButton";

function UserRegisterPage() {
    const navigate = useNavigate();

    const [step, setStep] = useState(1);
    const [userId, setUserId] = useState(null);
    const [departmentId, setDepartmentId] = useState(null);
    const [serverError, setServerError] = useState(null);
    const [departments, setDepartments] = useState([]);

    // USER FORM
    const {
        register,
        handleSubmit,
        watch,
        formState: { errors, isSubmitting },
    } = useForm();

    // DOCTOR FORM
    const {
        register: registerDoctor,
        handleSubmit: handleDoctorSubmit,
        formState: {
            errors: doctorErrors,
            isSubmitting: isDoctorSubmitting,
        },
    } = useForm();

    useEffect(() => {
        const fetchDepartments = async () => {
            try {
                const { data } = await getDepartments();
                setDepartments(data);
            } catch (err) {
                console.error(err);
            }
        };

        fetchDepartments();
    }, []);

    const role = watch("role");

    const onSubmitUser = async (data) => {
        try {
            setServerError(null);

            const payload = {
                first_name: data.first_name,
                last_name: data.last_name,
                email: data.email,
                phone: data.phone,
                role: data.role,
                department_id: data.department,
                address: data.address,
                metadata: {},
            };

            const response = await registerUser(payload);

            // If not a doctor, we're done.
            if (data.role !== "DOCTOR") {
                navigate("/");
                return;
            }

            setUserId(response.user_id);
            setDepartmentId(data.department);
            setStep(2);
        } catch (err) {
            setServerError(
                err?.response?.data?.detail ||
                    "Something went wrong."
            );
        }
    };

    const onSubmitDoctor = async (data) => {
        try {
            const payload = {
                user_id: userId,
                department_id: departmentId,
                license_number: data.license_number,
                qualification: data.qualification,
                gender: data.gender,
                specialization: data.specialization,
                experience_years: Number(
                    data.experience_years
                ),
                consultation_fee: Number(
                    data.consultation_fee
                ),
            };
            await createDoctor(payload);

            navigate("/");
        } catch (err) {
            console.log(err.response?.data);
            setServerError(
                err?.response?.data?.detail ||
                    "Unable to create doctor profile."
            );
        }
    };

    return (
        <div className="flex justify-center p-8">
            <div className="w-full max-w-lg rounded-lg border bg-white shadow">
                {/* STEPPER */}
                <div className="flex">
                    <div
                        className={`flex-1 p-4 text-center font-semibold ${
                            step === 1
                                ? "bg-blue-600 text-white"
                                : "bg-gray-200"
                        }`}
                    >
                        User Details
                    </div>

                    <div
                        className={`flex-1 p-4 text-center font-semibold ${
                            step === 2
                                ? "bg-blue-600 text-white"
                                : "bg-gray-200"
                        }`}
                    >
                        Doctor Details
                    </div>
                </div>

                <div className="p-8">
                    {step === 1 && (
                        <form
                            onSubmit={handleSubmit(
                                onSubmitUser
                            )}
                            className="space-y-4"
                        >
                            <FormField
                                label="First Name"
                                error={errors.first_name}
                            >
                                <Input
                                    {...register(
                                        "first_name",
                                        {
                                            required:
                                                "Required",
                                        }
                                    )}
                                />
                            </FormField>

                            <FormField
                                label="Last Name"
                            >
                                <Input
                                    {...register(
                                        "last_name"
                                    )}
                                />
                            </FormField>

                            <FormField
                                label="Email"
                                error={errors.email}
                            >
                                <Input
                                    type="email"
                                    {...register(
                                        "email",
                                        {
                                            required:
                                                "Required",
                                        }
                                    )}
                                />
                            </FormField>

                            <FormField
                                label="Phone"
                            >
                                <Input
                                    {...register(
                                        "phone"
                                    )}
                                />
                            </FormField>

                            <FormField
                                label="Role"
                                error={errors.role}
                            >
                                <Select
                                    {...register(
                                        "role",
                                        {
                                            required:
                                                "Required",
                                        }
                                    )}
                                >
                                    <option value="">
                                        Select
                                    </option>
                                    <option value="ADMIN">
                                        Admin
                                    </option>
                                    <option value="DOCTOR">
                                        Doctor
                                    </option>
                                    <option value="RECEPTIONIST">
                                        Receptionist
                                    </option>
                                </Select>
                            </FormField>

                            <FormField
                                label="Department"
                            >
                                <Select
                                    {...register(
                                        "department"
                                    )}
                                >
                                    <option value="">
                                        Select
                                    </option>

                                    {departments.map(
                                        (dept) => (
                                            <option
                                                key={
                                                    dept.department_id
                                                }
                                                value={
                                                    dept.department_id
                                                }
                                            >
                                                {
                                                    dept.name
                                                }
                                            </option>
                                        )
                                    )}
                                </Select>
                            </FormField>

                            <FormField
                                label="Address"
                            >
                                <Input
                                    {...register(
                                        "address"
                                    )}
                                />
                            </FormField>

                            {serverError && (
                                <p className="text-red-500">
                                    {serverError}
                                </p>
                            )}

                            <SubmitButton
                                isLoading={
                                    isSubmitting
                                }
                                className="w-full"
                            >
                                {role === "DOCTOR"
                                    ? "Continue"
                                    : "Register"}
                            </SubmitButton>
                        </form>
                    )}

                    {step === 2 && (
                        <form
                            onSubmit={handleDoctorSubmit(
                                onSubmitDoctor
                            )}
                            className="space-y-4"
                        >
                            <FormField
                                label="License Number"
                                error={
                                    doctorErrors.license_number
                                }
                            >
                                <Input
                                    {...registerDoctor(
                                        "license_number",
                                        {
                                            required:
                                                "Required",
                                        }
                                    )}
                                />
                            </FormField>

                            <FormField
                                label="Qualification"
                            >
                                <Input
                                    {...registerDoctor(
                                        "qualification"
                                    )}
                                />
                            </FormField>

                            <FormField
                                label="Gender"
                            >
                                <Select
                                    {...registerDoctor(
                                        "gender"
                                    )}
                                >
                                    <option value="">
                                        Select
                                    </option>
                                    <option value="MALE">
                                        Male
                                    </option>
                                    <option value="FEMALE">
                                        Female
                                    </option>
                                    <option value="OTHER">
                                        Other
                                    </option>
                                </Select>
                            </FormField>

                            <FormField
                                label="Specialization"
                            >
                                <Input
                                    {...registerDoctor(
                                        "specialization"
                                    )}
                                />
                            </FormField>

                            <FormField
                                label="Experience"
                            >
                                <Input
                                    type="number"
                                    {...registerDoctor(
                                        "experience_years"
                                    )}
                                />
                            </FormField>

                            <FormField
                                label="Consultation Fee"
                            >
                                <Input
                                    type="number"
                                    {...registerDoctor(
                                        "consultation_fee"
                                    )}
                                />
                            </FormField>

                            <SubmitButton
                                isLoading={
                                    isDoctorSubmitting
                                }
                                className="w-full"
                            >
                                Create Doctor
                            </SubmitButton>
                        </form>
                    )}
                </div>
            </div>
        </div>
    );
}

export default UserRegisterPage;













// import React, { useState, useEffect } from 'react'
// import { useForm } from 'react-hook-form';
// import { registerUser } from '../api/adminApi';
// import { useNavigate } from 'react-router-dom';

// import FormField from "@/components/forms/FormField.jsx";
// import Input from "@/components/forms/Input.jsx";
// import Select from "@/components/forms/Select.jsx";
// import Textarea from "@/components/forms/Textarea.jsx";
// import SubmitButton from "@/components/forms/SubmitButton.jsx";

// import { getDepartments } from "@/features/admin/api/adminApi.js"

// function UserRegisterPage() {

//     const [ serverError, setServerError] = useState(null);
//     const navigate = useNavigate();

//     const {
//         register,
//         handleSubmit,
//         formState: { errors, isSubmitting }
//     } = useForm({
//         defaultValues: {
//             metadata: "{}"
//         }
//     });

//     const [departments, setDepartments] = useState([]);

//     useEffect(() => {
//         try {
//             const fetchDepartments = async () => {
//                 const {data: departmentsData} = await getDepartments();
//                 setDepartments(departmentsData);
//             };
//             fetchDepartments();
//         } catch (error) {
//             console.error("Error fetching departments:", error);
//         }
//     }, []);

//     const onSubmit = async (data) => {
//         try {
//             setServerError(null);
//             let metadata = {};

//             if (data.metadata) {
//                 try {
//                     metadata = JSON.parse(data.metadata);
//                 } catch (parseError) {
//                     setServerError("Metadata must be valid JSON.");
//                     return;
//                 }
//             }

//             const payload = {
//                 first_name: data.first_name,
//                 last_name: data.last_name,
//                 email: data.email,
//                 phone: data.phone,
//                 role: data.role,
//                 department_id: data.department,
//                 department: data.department,
//                 address: data.address,
//                 metadata,
//             };

//             const response = await registerUser(payload);
//             console.log(`${data.first_name} registered with user id ${response.user_id}`);
//             navigate("/");
//         } catch(err) {
//             console.error(err);
//             setServerError(
//                 err?.response?.data?.detail ||
//                 "Invalid credentials"
//             );
//         }
//     }

//   return (

//     <div className="flex min-h-5 items-center justify-center bg-slate-50">
//         <div className="w-full max-w-md rounded-lg border border-slate-200 bg-white shadow-sm">

//             <div className="mb-4text-center bg-blue-100 h-25 flex flex-col items-center justify-center rounded-t-lg p-4">
//                 <h1 className="text-3xl font-bold text-blue-700">
//                     Hospital ERP
//                 </h1>

//                 <p className="mt-2 text-gray-500">
//                     Register new user
//                 </p>
//             </div>

//             <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 p-8" >
//                 <FormField
//                     label="First Name"
//                     required
//                     error={errors.first_name}
//                 >
//                     <Input
//                         {...register("first_name", { required: "First name is required" })}
//                     />
//                 </FormField>

//                 <FormField
//                     label="Last Name"
//                     error={errors.last_name}
//                 >
//                     <Input {...register("last_name")} />
//                 </FormField>

//                 <FormField
//                     label="Email"
//                     required
//                     error={errors.email}
//                 >
//                     <Input type="email" {...register("email", { required: "Email is required" })} />
//                 </FormField>

//                 <FormField
//                     label="Phone"
//                     error={errors.phone}
//                 >
//                     <Input {...register("phone")} />
//                 </FormField>

//                 <FormField
//                     label="Role"
//                     required
//                     error={errors.role}
//                 >
//                     <Select {...register("role", { required: "Role is required" })}>
//                         <option value="">Select Role</option>
//                         <option value="SUPER_ADMIN">Super Admin</option>
//                         <option value="ADMIN">Admin</option>
//                         <option value="DOCTOR">Doctor</option>
//                         <option value="RECEPTIONIST">Receptionist</option>
//                     </Select>
//                 </FormField>

//                 <FormField
//                     label="Department"
//                     error={errors.department}
//                 >
//                     <Select {...register("department")} >
//                         <option value="">Select</option>
//                         {
//                             departments.map((dept) => (
//                                 <option key={dept.department_id} value={dept.department_id}>{dept.name}</option>
//                             ))
//                         }
//                     </Select>
//                 </FormField>

//                 {/* <FormField
//                     label="Department ID"
//                     error={errors.department_id}
//                 >
//                     <Input {...register("department_id")} />
//                 </FormField> */}

//                 <FormField
//                     label="Address"
//                     error={errors.address}
//                 >
//                     <Textarea rows={4} {...register("address")} />
//                 </FormField>

//                 <FormField
//                     label="Metadata (JSON)"
//                     error={errors.metadata}
//                 >
//                     <Textarea
//                         rows={4}
//                         placeholder='e.g. { "additionalProp1": {} }'
//                         {...register("metadata")}
//                     />
//                 </FormField>

//                 {serverError && (
//                     <div className="rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-600">
//                         {serverError}
//                     </div>
//                 )}                  

//                 <SubmitButton isLoading={isSubmitting} className="w-full">
//                     {isSubmitting ? "Registering..." : "Register"}
//                 </SubmitButton>

//             </form>
//         </div>
//     </div>
//   )
// }

// export default UserRegisterPage