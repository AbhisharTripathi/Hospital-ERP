import { useState } from "react";
import { useForm } from "react-hook-form";
import { useAuthStore } from "@/store/authStore.js";

import Input from "@/components/forms/Input";
import FormField from "@/components/forms/FormField";
import SubmitButton from "@/components/forms/SubmitButton";

import { createDoctorSchedule } from "@/features/doctors/api/doctorApi.js";

const DAYS = [
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY",
    "SATURDAY",
    "SUNDAY",
];

function DoctorSchedulePage() {
    const user = useAuthStore((state) => state.user);

    const [serverError, setServerError] = useState(null);
    const [days, setDays] = useState(
        DAYS.map((day) => ({
            day,
            enabled: false,
            start_time: "09:00",
            end_time: "17:00",
        }))
    );
    // console.log("user", user);

    const {
        register,
        handleSubmit,
        formState: { isSubmitting },
    } = useForm({
        defaultValues: {
            doctor_id: user?.employee_id || "",
            slot_duration: 15,
            max_patients: 30,
        },
    });

    const handleCheckboxChange = (index) => {
        setDays((prev) =>
            prev.map((item, i) =>
                i === index
                    ? {
                        ...item,
                        enabled: !item.enabled,
                    }
                    : item
            )
        );
    };

    const handleTimeChange = (
        index,
        field,
        value
    ) => {
        setDays((prev) =>
            prev.map((item, i) =>
                i === index
                    ? {
                        ...item,
                        [field]: value,
                    }
                    : item
            )
        );
    };

    const onSubmit = async (data) => {
        try {
            setServerError(null);

            const payload = days
                .filter(
                    (schedule) =>
                        schedule.enabled
                )
                .map((schedule) => ({
                    doctor_id: data.doctor_id,
                    day_of_week: schedule.day,
                    start_time: schedule.start_time,
                    end_time: schedule.end_time,
                    slot_duration: Number(
                            data.slot_duration
                        ),
                    max_patients: Number(
                            data.max_patients
                        ),
                }));
                console.log("payload", payload);

            if (payload.length === 0) {
                setServerError("Please select at least one day.");
                return;
            }

            await Promise.all(
                payload.map(
                    (schedule) =>
                        createDoctorSchedule(
                            schedule
                        )
                )
            );

            alert(
                "Schedule created successfully."
            );
        } catch (err) {
            console.log(err?.response?.data || err);

            setServerError(
                err?.response?.data
                    ?.detail ||
                "Failed to create schedule."
            );
        }
    };

    return (
        <div className="flex justify-center p-8">
            <div className="w-full max-w-4xl rounded-lg border bg-white shadow">
                <div className="rounded-t-lg bg-blue-100 p-6">
                    <h1 className="text-3xl font-bold text-blue-700">
                        Doctor Schedule
                    </h1>

                    <p className="mt-2 text-gray-600">
                        Configure the
                        doctor's weekly
                        schedule.
                    </p>
                </div>

                <form
                    onSubmit={handleSubmit(
                        onSubmit
                    )}
                    className="space-y-6 p-8"
                >
                    <FormField label="Doctor ID">
                        <Input
                            placeholder="USR-2026-00001"
                            disabled
                            {...register(
                                "doctor_id",
                                {
                                    required: true,
                                }
                            )}
                        />
                    </FormField>

                    <div className="grid grid-cols-1 gap-4">
                        {days.map(
                            (
                                day,
                                index
                            ) => (
                                <div
                                    key={
                                        day.day
                                    }
                                    className="grid grid-cols-4 items-center gap-4 rounded-lg border p-4"
                                >
                                    <div className="flex items-center gap-3">
                                        <input
                                            type="checkbox"
                                            checked={
                                                day.enabled
                                            }
                                            onChange={() =>
                                                handleCheckboxChange(
                                                    index
                                                )
                                            }
                                        />

                                        <span className="font-semibold">
                                            {
                                                day.day
                                            }
                                        </span>
                                    </div>

                                    <Input
                                        type="time"
                                        value={
                                            day.start_time
                                        }
                                        disabled={
                                            !day.enabled
                                        }
                                        onChange={(
                                            e
                                        ) =>
                                            handleTimeChange(
                                                index,
                                                "start_time",
                                                e
                                                    .target
                                                    .value
                                            )
                                        }
                                    />

                                    <Input
                                        type="time"
                                        value={
                                            day.end_time
                                        }
                                        disabled={
                                            !day.enabled
                                        }
                                        onChange={(
                                            e
                                        ) =>
                                            handleTimeChange(
                                                index,
                                                "end_time",
                                                e
                                                    .target
                                                    .value
                                            )
                                        }
                                    />

                                    <div className="text-sm text-gray-500">
                                        {day.enabled
                                            ? "Enabled"
                                            : "Disabled"}
                                    </div>
                                </div>
                            )
                        )}
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <FormField label="Slot Duration (Minutes)">
                            <Input
                                type="number"
                                {...register(
                                    "slot_duration",
                                    {
                                        required: true,
                                    }
                                )}
                            />
                        </FormField>

                        <FormField label="Maximum Patients">
                            <Input
                                type="number"
                                {...register(
                                    "max_patients",
                                    {
                                        required: true,
                                    }
                                )}
                            />
                        </FormField>
                    </div>

                    {serverError && (
                        <div className="rounded-md border border-red-300 bg-red-50 p-3 text-red-600">
                            {
                                serverError
                            }
                        </div>
                    )}

                    <SubmitButton
                        isLoading={
                            isSubmitting
                        }
                        className="w-full"
                    >
                        {isSubmitting
                            ? "Saving..."
                            : "Save Weekly Schedule"}
                    </SubmitButton>
                </form>
            </div>
        </div>
    );
}

export default DoctorSchedulePage;