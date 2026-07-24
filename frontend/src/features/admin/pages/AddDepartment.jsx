import { useForm } from "react-hook-form"

import FormField from "@/components/forms/FormField.jsx";
import Input from "@/components/forms/Input.jsx";
import Select from "@/components/forms/Select.jsx";
import Textarea from "@/components/forms/Textarea.jsx";
import SubmitButton from "@/components/forms/SubmitButton.jsx";
import FormSection from "@/components/forms/FormSection.jsx";

export default function AddDepartment() {

    const {
        register,
        onSubmit,
        formState: {
            errors,
            isSubmitting
        }
    } = useForm();

    return (
        <form>
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