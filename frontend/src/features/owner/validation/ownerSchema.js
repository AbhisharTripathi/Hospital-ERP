import { z } from "zod";

export const ownerRegisterSchema = z.object({
    hospital_name: z
        .string()
        .min(2, "Hospital Name must be at least two characters long.")
        .max(50, "Hospital Name can not be more than 50 char long."),

    owner_first_name: z
        .string()
        .min(2, "First Name must be at least two characters long.")
        .max(30, "First Name can not be more than 30 char long."),

    owner_last_name: z
        .string()
        .optional(),

    owner_email: z
        .email("Invalid Email"),

    owner_phone_number: z
        .string()
        .min(2, "Not valid")
        .max(15, "Not valid")
        .optional(),

    owner_password: z
        .string()
        .min(6, "Password's length too small"),
        
    owner_password_confirm: z
        .string(),

    // subscription_plan: z
    //     .string()
    //     .min(1, "Please select a subscription plan")
})
.refine((data) => data.owner_password === data.owner_password_confirm, {
    message: "Passwords don't match",
    path: ["owner_password_confirm"],
})
.transform(({ owner_password_confirm, ...rest}) => {
    return Object.fromEntries(
        Object.entries(rest).filter(([key, value]) => value !== "")
    );
});