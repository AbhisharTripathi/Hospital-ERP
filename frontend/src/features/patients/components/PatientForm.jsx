import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { patientSchema } from "../validation/patientSchema";

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

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="grid grid-cols-1 md:grid-cols-2 gap-4"
    >
      <div>
        <label className="block mb-1">
          First Name *
        </label>

        <input
          {...register("first_name")}
          className="w-full border rounded-md p-2"
        />

        {errors.first_name && (
          <p className="text-red-500 text-sm">
            {errors.first_name.message}
          </p>
        )}
      </div>

      <div>
        <label className="block mb-1">
          Last Name
        </label>

        <input
          {...register("last_name")}
          className="w-full border rounded-md p-2"
        />
      </div>

      <div>
        <label className="block mb-1">
          Phone *
        </label>

        <input
          {...register("phone")}
          className="w-full border rounded-md p-2"
        />

        {errors.phone && (
          <p className="text-red-500 text-sm">
            {errors.phone.message}
          </p>
        )}
      </div>

      <div>
        <label className="block mb-1">
          Email
        </label>

        <input
          type="email"
          {...register("email")}
          className="w-full border rounded-md p-2"
        />

        {errors.email && (
          <p className="text-red-500 text-sm">
            {errors.email.message}
          </p>
        )}
      </div>

        {
          showPassword && (
            <div>
              <label className="block mb-1">
                Password
              </label>

              <input
                type="password"
                {...register("password")}
                className="w-full border rounded-md p-2"
              />
            </div>  
          
          )
        }
      

      <div>
        <label className="block mb-1">
          Gender *
        </label>

        <select
          {...register("gender")}
          className="w-full border rounded-md p-2"
        >
          <option value="MALE">Male</option>
          <option value="FEMALE">Female</option>
          <option value="OTHER">Other</option>
        </select>
      </div>

      <div>
        <label className="block mb-1">
          Date of Birth *
        </label>

        <input
          type="date"
          {...register("dob")}
          className="w-full border rounded-md p-2"
        />
      </div>

      <div>
        <label className="block mb-1">
          Blood Group
        </label>

        <select
          {...register("blood_group")}
          className="w-full border rounded-md p-2"
        >
          <option value="">Select</option>
          <option value="A+">A+</option>
          <option value="A-">A-</option>
          <option value="B+">B+</option>
          <option value="B-">B-</option>
          <option value="AB+">AB+</option>
          <option value="AB-">AB-</option>
          <option value="O+">O+</option>
          <option value="O-">O-</option>
        </select>
      </div>

      <div>
        <label className="block mb-1">
          Emergency Contact Name
        </label>

        <input
          {...register("emergency_contact_name")}
          className="w-full border rounded-md p-2"
        />
      </div>

      <div>
        <label className="block mb-1">
          Emergency Contact Phone
        </label>

        <input
          {...register("emergency_contact_phone")}
          className="w-full border rounded-md p-2"
        />
      </div>

      <div className="md:col-span-2">
        <label className="block mb-1">
          Address
        </label>

        <textarea
          rows={3}
          {...register("address")}
          className="w-full border rounded-md p-2"
        />
      </div>

      <div className="md:col-span-2">
        <label className="block mb-1">
          Notes
        </label>

        <textarea
          rows={4}
          {...register("notes")}
          className="w-full border rounded-md p-2"
        />
      </div>

      <div className="md:col-span-2 flex justify-end">
        <button
          type="submit"
          disabled={isLoading}
          className="px-6 py-2 bg-black text-white rounded-md"
        >
          {isLoading ? "Saving..." : submitText}
        </button>
      </div>
    </form>
  );
}

export default PatientForm;