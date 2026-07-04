import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { patientSchema } from "../validation/patientSchema";

import FormSection from "@/components/forms/FormSection.jsx";
import FormField from "@/components/forms/FormField.jsx";
import Input from "@/components/forms/Input.jsx";
import Select from "@/components/forms/Select.jsx";
import Textarea from "@/components/forms/Textarea.jsx";
import SubmitButton from "@/components/forms/SubmitButton.jsx";

function PatientForm({
  initialData = null,
  onSubmit,
  isLoading = false,
  submitText = "Save Patient",
  showPassword = false
}) {

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(patientSchema),
  });

  useEffect(() => {
    if(!initialData) return;
    reset({
      first_name: initialData.first_name || "",
      last_name: initialData.last_name || "",
      password: "",
      phone: initialData.phone || "",
      email: initialData.email || "",
      gender: initialData.gender || "male",
      dob: initialData.dob || "",
      blood_group: initialData.blood_group || "",
      address: initialData.address || "",
      emergency_contact_name:
        initialData.emergency_contact_name || "",
      emergency_contact_phone:
        initialData.emergency_contact_phone || "",
      notes: initialData.notes || "",
    });
  }, [initialData, reset]);

  const bloodGroups = [
    "A+",
    "A-",
    "B+",
    "B-",
    "AB+",
    "AB-",
    "O+",
    "O-"
  ];

  const genders = [
    "MALE",
    "FEMALE",
    "OTHER"
  ];

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="flex flex-col gap-6"
    >
      <FormSection title="Patient Information">
        <FormField
          label="First Name"
          required
          error={errors.first_name}
        >
          <Input {...register("first_name")} />
        </FormField>

        <FormField
          label="Last Name"
          required
          error={errors.last_name}
        >
          <Input {...register("last_name")} />
        </FormField>

        <FormField
          label="Phone"
          required
          error={errors.phone}
        >
          <Input {...register("phone")} />
        </FormField>

        <FormField
          label="Email"
          error={errors.email}
        >
          <Input type="email" {...register("email")} />
        </FormField>
        
        <FormField
          label="Gender"
          required
          >
          <Select {...register("gender")} >
            {
              genders.map((group) => (
                <option key={group} value={group}>{group}</option>
              ))
            }
          </Select>
        </FormField>

        <FormField
          label="Date of Birth"
          required
          error={errors.dob}
          >
          <Input type="date" {...register("dob")} />
        </FormField>

        {
          showPassword && (
            <FormField
              label="Password"
              error={errors.password}
            >
              <Input type="password" {...register("password")} />
            </FormField>
          )
        }
      </FormSection>

      <FormSection title="Medical Information">
        <FormField
          label="Blood Group"
        >
          <Select {...register("blood_group")} >
            <option value="">Select</option>
            {
              bloodGroups.map((group) => (
                <option key={group} value={group}>{group}</option>
              ))
            }
          </Select>
        </FormField>

        <FormField
          label="Notes"
          error={errors.notes}
        >
          <Textarea {...register("notes")} rows={1} />
        </FormField>
      </FormSection>

      <FormSection title="Contact Information">
        <FormField
          label="Emergency Contact Name"
          error={errors.emergency_contact_name}
        >
          <Input {...register("emergency_contact_name")} />
        </FormField>

        <FormField
          label="Emergency Contact Phone"
          error={errors.emergency_contact_phone}
        >
          <Input {...register("emergency_contact_phone")} />
        </FormField>
        
        <FormField
          label="Address"
          error={errors.address}
        >
          <Textarea {...register("address")} rows={3} />
        </FormField>
      </FormSection>
      
      <div className="md:col-span-2 flex justify-end">
        <SubmitButton isLoading={isLoading}>
          {submitText}
        </SubmitButton>
      </div>

    </form>
  );
}

export default PatientForm;