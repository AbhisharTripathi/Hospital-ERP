import { useForm } from "react-hook-form";
import { forwardRef, useImperativeHandle, useState, useEffect } from "react";

import FormField from "@/components/forms/FormField";
import Input from "@/components/forms/Input";
import Select from "@/components/forms/Select";
import Textarea from "@/components/forms/Textarea";
import FormSection from "@/components/forms/FormSection.jsx"
import {
    getDepartments,
    getDoctorsByDepartment,
} from "@/features/receptionist/api/receptionistApi.js";

function AppointmentFormSectionFunction(props, ref) {
    const {
        register,
        handleSubmit,
        reset,
        formState: {
            errors,
        },
        watch,
    } = useForm();

    useImperativeHandle(ref, () => ({
        handleSubmit,
        reset,
    }))

    const [departments, setDepartments] = useState([]);
    const [doctors, setDoctors] = useState([]);

    const selectedDepartment = watch("department_id");

    useEffect(() => {
        const fetchDepartments = async () => {
            try {
                const { data } = await getDepartments();
                setDepartments(data);
            } catch (err) {
                console.error(err);
                console.log(err?.response?.data?.message);
            }
        };
        fetchDepartments();
    }, []);

    useEffect(() => {
        if (!selectedDepartment) {
            setDoctors([]);
            return;
        }
        const fetchDoctors = async () => {
            try {
                const data = await getDoctorsByDepartment(selectedDepartment);
                setDoctors(data);
            } catch (err) {
                console.error(err);
            }
        };

        fetchDoctors();
    }, [selectedDepartment]);

    return (
        <form>
            <FormSection title="Appointment Details" >
                <FormField
                    label="Department"
                    required
                    error={
                        errors.department_id
                    }
                >
                    <Select
                        {...register(
                            "department_id",
                            {
                                required:
                                    "Department is required",
                            }
                        )}
                    >
                        <option value="">
                            Select Department
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
                    label="Doctor"
                    required
                    error={
                        errors.doctor_id
                    }
                >
                    <Select
                        {...register(
                            "doctor_id",
                            {
                                required:
                                    "Doctor is required",
                            }
                        )}
                        disabled={
                            !selectedDepartment
                        }
                    >
                        <option value="">
                            Select Doctor
                        </option>

                        {doctors.map(
                            (doctor) => (
                                <option
                                    key={
                                        doctor.doctor_id
                                    }
                                    value={
                                        doctor.doctor_id
                                    }
                                >
                                    {
                                        doctor.first_name + " " + doctor.last_name
                                    }
                                </option>
                            )
                        )}
                    </Select>
                </FormField>

                <FormField
                    label="Appointment Date"
                    required
                    error={
                        errors.appointment_date
                    }
                >
                    <Input
                        type="date"
                        {...register(
                            "appointment_date",
                            {
                                required:
                                    "Date is required",
                            }
                        )}
                    />
                </FormField>

                <FormField
                    label="Appointment Time"
                    required
                    error={
                        errors.appointment_time
                    }
                >
                    <Input
                        type="time"
                        {...register(
                            "appointment_time",
                            {
                                required:
                                    "Time is required",
                            }
                        )}
                    />
                </FormField>

                <FormField
                    label="Appointment Type"
                    required
                    error={
                        errors.appointment_type
                    }
                >
                    <Select
                        {...register(
                            "appointment_type"
                        )}
                    >
                        <option value="NEW">
                            NEW
                        </option>
                        <option value="FOLLOW_UP">
                            FOLLOW UP
                        </option>
                        <option value="EMERGENCY">
                            EMERGENCY
                        </option>
                    </Select>
                </FormField>

                <FormField label="Reason">
                    <Textarea
                        rows={1}
                        {...register(
                            "reason"
                        )}
                    />
                </FormField>

                <FormField label="Notes">
                    <Textarea
                        rows={1}
                        {...register(
                            "notes"
                        )}
                    />
                </FormField>

                {/* {serverError && (
                    <div className="rounded-md border border-red-300 bg-red-50 p-3 text-red-600">
                        {serverError}
                    </div>
                )} */}
            </FormSection>
        </form>
    )
}
const AppointmentFormSection = forwardRef(AppointmentFormSectionFunction);
AppointmentFormSection.displayName = "AppointmentFormSection";
export default AppointmentFormSection;