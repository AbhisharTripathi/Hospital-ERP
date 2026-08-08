import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { FaSearch } from "react-icons/fa";
import { useSearchParams, useNavigate } from "react-router-dom";

import {
    getDepartments,
    getDoctorsByDepartment,
    createAppointment,
} from "@/features/receptionist/api/receptionistApi.js";

import {
    getPatientByMobileNo,
    getPatientById,
} from "@/features/receptionist/api/patientApi.js"

import FormField from "@/components/forms/FormField";
import Input from "@/components/forms/Input";
import Select from "@/components/forms/Select";
import Textarea from "@/components/forms/Textarea";
import SubmitButton from "@/components/forms/SubmitButton";
import FormSection from "@/components/forms/FormSection.jsx"


function CreateAppointmentPage() {
    const navigate = useNavigate();
    const [departments, setDepartments] = useState([]);
    const [doctors, setDoctors] = useState([]);
    const [serverError, setServerError] = useState(null);

    const [searchParam, setSearchParam] = useState("patient_id");
    const [searchId, setSearchId] = useState("");
    const [patient, setPatient] = useState(null);

    const fetchPatient = async () => {
        if (!searchId) return;
        try {
            let response;
            if (searchParam === "mobile_no") {
                response = await getPatientByMobileNo(searchId);
            } else if (searchParam === "patient_id") {
                response = await getPatientById(searchId);
            }
            setPatient(response);
        } catch (err) {
            console.error(err);
            console.log(err?.response?.data?.message);
        }
    }

    const [queryParams] = useSearchParams();
    useEffect(() => {
        const patientId = queryParams.get("patient_id");

        if (!patientId) return;

        setSearchParam("patient_id");
        setSearchId(patientId);
    }, [queryParams]);

    useEffect(() => {
        setPatient(null);
        const id = setTimeout(fetchPatient, 3000);

        return () => clearTimeout(id);
    }, [searchId]);

    const {
        register,
        handleSubmit,
        watch,
        formState: {
            errors,
            isSubmitting,
        },
    } = useForm({
        defaultValues: {
            appointment_type: "NEW",
        },
    });

    const selectedDepartment = watch("department_id");

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

    useEffect(() => {
        if (!selectedDepartment) {
            setDoctors([]);
            return;
        }

        const fetchDoctors = async () => {
            try {
                const data = await getDoctorsByDepartment(selectedDepartment);
                console.log("Doctors data:", data);
                setDoctors(data);
            } catch (err) {
                console.error(err);
            }
        };

        fetchDoctors();
    }, [selectedDepartment]);

    const onSubmit = async (data) => {
        try {
            setServerError(null);

            const payload = {
                patient_id: patient.patient_id,
                doctor_id: data.doctor_id,
                department_id:
                    data.department_id,
                appointment_date:
                    data.appointment_date,
                appointment_time:
                    data.appointment_time,
                appointment_type:
                    data.appointment_type,
                reason: data.reason,
                notes: data.notes,
            };

            await createAppointment(
                payload
            );

            alert(
                "Appointment created successfully."
            );
            navigate("/receptionist/patients/create");
        } catch (err) {
            console.log(err?.response?.data || err);
            setServerError(
                err?.response?.data?.message ||
                "Unable to create appointment."
            );
        }
    };


    return (
        <div className="flex justify-center p-8">
            <div className="w-full max-w-2xl rounded-lg border bg-white shadow">
                <div className="rounded-t-lg bg-blue-100 p-5">
                    <h1 className="text-2xl font-bold text-blue-700">
                        Create Appointment
                    </h1>
                </div>

                <form
                    onSubmit={handleSubmit(
                        onSubmit
                    )}
                    className="space-y-4 p-8"
                >
                    <FormSection title="Patient Details">
                        <FormField
                            label="Search Patient by :-"
                            required
                        >
                            <Select
                                disabled={queryParams.get("patient_id")}
                                value={searchParam}
                                onChange={(e) => setSearchParam(e.target.value)}
                            >
                                <option value="patient_id">Patient ID</option>
                                <option value="mobile_no">Mobile no.</option>

                            </Select>
                        </FormField>
                        <FormField
                            label={searchParam === "patient_id" ? "Patient ID" : "Mobile no."}
                            required
                        >
                            <div className="flex relative items-center">
                                <Input
                                    disabled={queryParams.get("patient_id")}
                                    placeholder={searchParam === "patient_id" ? "PAT-2026-00001" : "9912345678"}
                                    value={searchId}
                                    onChange={(e) => setSearchId(e.target.value)}
                                />
                                <button
                                    type="button"
                                    disabled={queryParams.get("patient_id")}
                                    className="rounded-full h-8 w-8 absolute right-1 bg-blue-600 text-white hover:bg-blue-700 flex items-center justify-center"
                                    onClick={fetchPatient}
                                ><FaSearch /></button>
                            </div>
                        </FormField>

                        <FormField
                            label="Patient Full Name"
                        >
                            <Input
                                disabled
                                value={patient ? patient.first_name + " " + patient.last_name : ""}
                            />
                        </FormField>

                        <FormField
                            label="Patient's DOB"
                        >
                            <Input
                                disabled
                                value={patient ? patient.dob : ""}
                            />
                        </FormField>
                    </FormSection>
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

                        {serverError && (
                            <div className="rounded-md border border-red-300 bg-red-50 p-3 text-red-600">
                                {serverError}
                            </div>
                        )}
                    </FormSection>
                    <SubmitButton
                        isLoading={
                            isSubmitting
                        }
                        className="w-full"
                    >
                        {isSubmitting
                            ? "Creating..."
                            : "Create Appointment"}
                    </SubmitButton>
                </form>
            </div>
        </div>
    );
}

export default CreateAppointmentPage;