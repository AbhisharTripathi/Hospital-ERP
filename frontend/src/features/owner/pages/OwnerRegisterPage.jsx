import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom';

import FormField from "@/components/forms/FormField.jsx";
import Input from "@/components/forms/Input.jsx";
import Select from "@/components/forms/Select.jsx";
import SubmitButton from "@/components/forms/SubmitButton.jsx";

import { zodResolver } from "@hookform/resolvers/zod";

import { registerOwner } from '../api/ownerApi.js';
import { ownerRegisterSchema } from '../validation/ownerSchema.js';

function OwnerRegisterPage() {

    const [serverError, setServerError] = useState();
    const navigate = useNavigate();

    const {
        register,
        handleSubmit,
        formState: {
            isSubmitting,
            errors
        }
    } = useForm({
        resolver: zodResolver(ownerRegisterSchema),
    });

    const onSubmit = async (data) => {
        try {
            setServerError(null);
            await registerOwner(data);
            navigate("/auth/login");
        } catch (err) {
            alert("Error registering owner: " + err.message);
            console.log(err);
            setServerError(err.message);
        }
    };

    return (
        <div className="flex justify-center items-center">
            <div className="max-w-7xl">
                <div className="border border-slate-200 rounded-2xl bg-white shadow-sm">

                    <h1 className="text-2xl font-bold mb-1 flex items-center justify-center bg-blue-100 h-20 text-center rounded-t-2xl text-blue-700">
                        Register Hospital
                    </h1>

                    <div className="p-6">
                        <form onSubmit={handleSubmit(onSubmit)}
                            className="flex flex-col gap-6 w-sm"
                        >
                            <FormField
                                label="Hospital Name"
                                required
                                error={errors.hospital_name}
                            >
                                <Input {...register("hospital_name")} placeholder="Enter hospital name" />
                            </FormField>

                            <FormField
                                label="First Name"
                                required
                                error={errors.owner_first_name}
                            >
                                <Input {...register("owner_first_name")} placeholder="Enter your first name" />
                            </FormField>

                            <FormField
                                label="Last Name"
                                error={errors.owner_last_name}
                            >
                                <Input {...register("owner_last_name")} placeholder="Enter your last name" />
                            </FormField>

                            <FormField
                                label="Enter your Email"
                                required
                                error={errors.owner_email}
                            >
                                <Input {...register("owner_email")} placeholder="Enter your email" type="email" />
                            </FormField>

                            <FormField
                                label="Enter your Phone Number"
                                error={errors.owner_phone}
                            >
                                <Input {...register("owner_phone")} placeholder="Enter your phone number" />
                            </FormField>

                            <FormField
                                label="Enter your Password"
                                required
                                error={errors.owner_password}
                            >
                                <Input {...register("owner_password")} placeholder="Enter your password" type="password" />
                            </FormField>

                            <FormField
                                label="Confirm your Password"
                                required
                                error={errors.owner_password_confirm}
                            >
                                <Input {...register("owner_password_confirm")} placeholder="Confirm your password" type="password" />
                            </FormField>

                            {/* <FormField
                                label="Subscription"
                                required
                                error={errors.subscription_plan}
                            >
                                <Select {...register("subscription_plan")} >
                                    <option value="" >Choose a plan</option>
                                    <option value="PREMIUM">Premium</option>
                                    <option value="BASIC">Basic</option>
                                </Select>
                            </FormField> */}

                            <div>
                                <SubmitButton
                                    isLoading={isSubmitting}
                                    className="w-full"
                                >
                                    Submit Details
                                </SubmitButton>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default OwnerRegisterPage