import { z } from "zod";

export const patientSchema = z.object({
  first_name: z
    .string()
    .min(2, "First name must be at least 2 characters")
    .max(50, "First name must be less than 50 characters"),

  last_name: z.string().optional(),

  password: z
    .string()
    .min(6, "Password must be at least 6 characters")
    .optional()
    .or(z.literal("")),

  phone: z
    .string()
    .min(10, "Phone number is required")
    .max(15, "Phone number is too long"),

  email: z
    .string()
    .email("Invalid email")
    .optional()
    .or(z.literal("")),

  gender: z.enum(["MALE", "FEMALE", "OTHER"]),

  dob: z.string(),

  blood_group: z.string().optional(),

  address: z.string().optional(),

  emergency_contact_name: z.string().optional(),

  emergency_contact_phone: z.string().optional(),

  notes: z.string().optional(),
});