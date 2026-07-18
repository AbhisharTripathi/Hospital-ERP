import { useNavigate, useSearchParams } from "react-router-dom";
import { useForm } from "react-hook-form";
import { setPaswordSchema } from "../validation/setPasswordSchema";
import { zodResolver } from "@hookform/resolvers/zod";

import FormField from "@/components/forms/FormField.jsx";
import Input from "@/components/forms/Input.jsx";
import Select from "@/components/forms/Select.jsx";
import Textarea from "@/components/forms/Textarea.jsx";
import SubmitButton from "@/components/forms/SubmitButton.jsx";

import { setPassword } from "../api/authApi";

export default function UserSetPasswordPage() {
    const [searchParams] = useSearchParams();
    const token = searchParams.get("token");
    const navigate = useNavigate();

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting }
    } = useForm({
        resolver: zodResolver(setPaswordSchema),
    });

    const onSubmit = async (data) => {
        if (data.password !== data.confirmPassword) {
            alert("Passwords do not match");
            return;
        }
        try {

            await setPassword(token, data.password);
            alert("Password set successfully");
            navigate("/auth/login");
        } catch (error) {
            console.error("Error setting password:", error);
            alert("Failed to set password");
        }
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <div className="w-full max-w-md p-8 bg-white rounded shadow-md">
                <h2 className="text-2xl font-bold mb-6 text-center">Set Your Password</h2>
                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    <FormField
                        label="New Password"
                        required
                        error={errors.password}
                    >
                        <Input
                            type="password"
                            {...register("password")}
                        />
                    </FormField>

                    <FormField
                        label="Confirm Password"
                        required
                        error={errors.confirmPassword}
                    >
                        <Input
                            type="password"
                            {...register("confirmPassword")}
                        />
                    </FormField>

                    <SubmitButton isLoading={isSubmitting} className="w-full">
                        {isSubmitting ? "Setting Password..." : "Set Password"}
                    </SubmitButton>
            </form>
        </div>
        </div >
    );
}