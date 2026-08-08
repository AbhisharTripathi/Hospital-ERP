import { useForm } from "react-hook-form"

import FormField from "@/components/forms/FormField.jsx";
import Input from "@/components/forms/Input.jsx";
import Select from "@/components/forms/Select.jsx";
import Textarea from "@/components/forms/Textarea.jsx";
import SubmitButton from "@/components/forms/SubmitButton.jsx";
import FormSection from "@/components/forms/FormSection.jsx";

import { registerDepartment } from "../api/adminApi.js"

export default function AddDepartment() {

    const {
        register,
        handleSubmit,
        reset,
        formState: {
            errors,
            isSubmitting
        }
    } = useForm();

    const onSubmit = (data) => {
        const payload = {
            name: data.name,
            code: data.code,
            description: data.description
        };
        try {
            registerDepartment(payload);
            reset();
            alert("Department registered successfully!");
        } catch (error) {
            console.error("Error registering department:", error);
            alert("Failed to register department.");
        }
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <FormSection title="Add Department">
                <FormField label="Department Name" required error={errors.name}>
                    <Input
                        type="text"
                        {...register("name")}
                    />
                </FormField>

                <FormField label="Department Code" required error={errors.code}>
                    <Input
                        type="text"
                        {...register("code")}
                    />
                </FormField>

                <FormField label="Description" error={errors.description}>
                    <Textarea
                        {...register("description")}
                    />
                </FormField>
            </ FormSection>
            <SubmitButton isSubmitting={isSubmitting}>Add Department</SubmitButton>
        </form>
    )
}