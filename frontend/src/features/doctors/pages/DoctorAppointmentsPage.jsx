import { useEffect, useState } from "react";
import { useAuthStore } from "@/store/authStore.js";

import AppointmentCard from "@/components/commonFeature/AppointmentCard.jsx";
import { getDoctorAppointments } from "../api/doctorApi";

function DoctorAppointmentsPage() {
    const [appointments, setAppointments] = useState([]);

    const [page, setPage] = useState(1);
    const [total, setTotal] = useState(0);
    const [totalPages, setTotalPages] = useState(1);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);

    const user = useAuthStore(state => state.user);

    useEffect(() => {
        fetchAppointments();
    }, [page]);

    const fetchAppointments =
        async () => {
            try {
                setLoading(true);
                console.log(user);
                const data  =
                    await getDoctorAppointments(
                        user.employee_id,
                        page
                    );
                console.log("data", data);

                setAppointments(
                    data.items
                );

                setPage(data.page);

                setTotal(data.total);

                setTotalPages(
                    data.total_pages
                );
            } catch (err) {
                console.error(err);

                setError(
                    "Unable to fetch appointments."
                );
            } finally {
                setLoading(false);
            }
        };

    if (loading) {
        return (
            <div className="p-8">
                Loading...
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-8 text-red-500">
                {error}
            </div>
        );
    }

    return (
        <div className="p-8">
            <div className="mb-6 flex items-center justify-between">
                <h1 className="text-3xl font-bold">
                    Doctor Appointments
                </h1>

                <div className="rounded bg-slate-100 px-4 py-2">
                    Total: {total}
                </div>
            </div>

            <div className="grid gap-5 lg:grid-cols-2">
                {appointments.map(
                    (appointment) => (
                        <AppointmentCard
                            key={
                                appointment.appointment_id
                            }
                            appointment={
                                appointment
                            }
                        />
                    )
                )}
            </div>

            <div className="mt-8 flex items-center justify-center gap-4">
                <button
                    disabled={
                        page === 1
                    }
                    onClick={() =>
                        setPage(
                            (prev) =>
                                prev - 1
                        )
                    }
                    className="rounded border px-4 py-2 disabled:opacity-50"
                >
                    Previous
                </button>

                <span>
                    Page {page} of{" "}
                    {totalPages}
                </span>

                <button
                    disabled={
                        page ===
                        totalPages
                    }
                    onClick={() =>
                        setPage(
                            (prev) =>
                                prev + 1
                        )
                    }
                    className="rounded border px-4 py-2 disabled:opacity-50"
                >
                    Next
                </button>
            </div>
        </div>
    );
}

export default DoctorAppointmentsPage;