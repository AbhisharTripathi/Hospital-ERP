import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
    getAppointmentDetails,
    getPatientById,
    updateAppointmentStatus,
} from "../api/doctorApi";

export default function DoctorDealAppointmentPage() {
    const {appointment_id} = useParams();

    const [appointment, setAppointment] = useState(null);
    const [patient, setPatient] = useState(null);
    const [status, setStatus] = useState("");
    const [isUpdating, setIsUpdating] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAppointmentAndPatient = async () => {
            try {
                setLoading(true);

                const appointmentDetails =
                    await getAppointmentDetails(appointment_id);

                setAppointment(appointmentDetails);
                setStatus(appointmentDetails.status);

                const patientDetails = await getPatientById(
                    appointmentDetails.patient_id
                );

                setPatient(patientDetails);
            } catch (err) {
                console.log(err?.response?.data?.message);
            } finally {
                setLoading(false);
            }
        };

        fetchAppointmentAndPatient();
    }, [appointment_id]);

    const handleStatusUpdate = async () => {
        try {
            setIsUpdating(true);

            await updateAppointmentStatus(
                appointment.appointment_id,
                status
            );

            setAppointment((prev) => ({
                ...prev,
                status,
            }));

            alert("Appointment status updated successfully!");
        } catch (err) {
            console.log(err?.response?.data?.message);
            alert("Failed to update appointment status.");
        } finally {
            setIsUpdating(false);
        }
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center h-screen">
                Loading...
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto p-6">
            <h1 className="text-3xl font-bold mb-8">
                Appointment Details
            </h1>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Appointment Card */}
                <div className="bg-white rounded-xl shadow-md p-6">
                    <h2 className="text-2xl font-semibold mb-6">
                        Appointment Information
                    </h2>

                    <div className="space-y-3">
                        <p>
                            <strong>Appointment ID:</strong>{" "}
                            {appointment?.appointment_id}
                        </p>

                        <p>
                            <strong>Date:</strong>{" "}
                            {appointment?.appointment_date}
                        </p>

                        <p>
                            <strong>Time:</strong>{" "}
                            {appointment?.appointment_time}
                        </p>

                        <p>
                            <strong>Token Number:</strong>{" "}
                            {appointment?.token_number}
                        </p>

                        <p>
                            <strong>Appointment Type:</strong>{" "}
                            {appointment?.appointment_type}
                        </p>

                        <p>
                            <strong>Reason:</strong>{" "}
                            {appointment?.reason}
                        </p>

                        <p>
                            <strong>Notes:</strong>{" "}
                            {appointment?.notes || "N/A"}
                        </p>

                        <p>
                            <strong>Current Status:</strong>{" "}
                            <span className="font-semibold">
                                {appointment?.status}
                            </span>
                        </p>
                    </div>

                    <div className="mt-8">
                        <label className="block mb-2 font-medium">
                            Update Status
                        </label>

                        <select
                            value={status}
                            onChange={(e) =>
                                setStatus(e.target.value)
                            }
                            className="w-full border rounded-lg p-3"
                        >
                            <option value="BOOKED">
                                BOOKED
                            </option>
                            <option value="IN_PROGRESS">
                                IN PROGRESS
                            </option>
                            <option value="COMPLETED">
                                COMPLETED
                            </option>
                            <option value="CANCELLED">
                                CANCELLED
                            </option>
                            <option value="NO_SHOW">
                                NO SHOW
                            </option>
                        </select>

                        <button
                            onClick={handleStatusUpdate}
                            disabled={isUpdating}
                            className="mt-4 w-full bg-black text-white py-3 rounded-lg hover:opacity-90 disabled:opacity-50"
                        >
                            {isUpdating
                                ? "Updating..."
                                : "Update Status"}
                        </button>
                    </div>
                </div>

                {/* Patient Card */}
                <div className="bg-white rounded-xl shadow-md p-6">
                    <h2 className="text-2xl font-semibold mb-6">
                        Patient Information
                    </h2>

                    <div className="space-y-3">
                        <p>
                            <strong>Name:</strong>{" "}
                            {patient?.first_name}{" "}
                            {patient?.last_name}
                        </p>

                        <p>
                            <strong>Patient ID:</strong>{" "}
                            {patient?.patient_id}
                        </p>

                        <p>
                            <strong>Gender:</strong>{" "}
                            {patient?.gender}
                        </p>

                        <p>
                            <strong>Date of Birth:</strong>{" "}
                            {patient?.dob}
                        </p>

                        <p>
                            <strong>Blood Group:</strong>{" "}
                            {patient?.blood_group}
                        </p>

                        <p>
                            <strong>Phone:</strong>{" "}
                            {patient?.phone}
                        </p>

                        <p>
                            <strong>Email:</strong>{" "}
                            {patient?.email}
                        </p>

                        <p>
                            <strong>Address:</strong>{" "}
                            {patient?.address}
                        </p>

                        <p>
                            <strong>Emergency Contact:</strong>{" "}
                            {patient?.emergency_contact_name}
                        </p>

                        <p>
                            <strong>Emergency Phone:</strong>{" "}
                            {patient?.emergency_contact_phone}
                        </p>

                        <p>
                            <strong>Status:</strong>{" "}
                            {patient?.status}
                        </p>

                        <p>
                            <strong>Patient Notes:</strong>{" "}
                            {patient?.notes || "N/A"}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}