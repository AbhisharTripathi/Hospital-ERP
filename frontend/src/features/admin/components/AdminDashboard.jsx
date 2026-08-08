import {
    FaHospital,
    FaUserInjured,
    FaUserMd,
    FaBuilding,
    FaCalendarCheck,
    FaMoneyBillWave,
} from "react-icons/fa";

const AdminDashboard = ({ data }) => {
    const { hospital, stats, recent_appointments, appointment_status_summary } =
        data;

    const statCards = [
        {
            title: "Total Patients",
            value: stats.total_patients,
            icon: <FaUserInjured size={24} />,
        },
        {
            title: "Active Patients",
            value: stats.active_patients,
            icon: <FaUserInjured size={24} />,
        },
        {
            title: "Total Doctors",
            value: stats.total_doctors,
            icon: <FaUserMd size={24} />,
        },
        {
            title: "Active Doctors",
            value: stats.active_doctors,
            icon: <FaUserMd size={24} />,
        },
        {
            title: "Departments",
            value: stats.total_departments,
            icon: <FaBuilding size={24} />,
        },
        {
            title: "Today's Appointments",
            value: stats.today_appointments,
            icon: <FaCalendarCheck size={24} />,
        },
        {
            title: "Completed Today",
            value: stats.completed_today,
            icon: <FaCalendarCheck size={24} />,
        },
        {
            title: "Revenue Today",
            value: `₹${stats.today_revenue}`,
            icon: <FaMoneyBillWave size={24} />,
        },
    ];

    return (
        <div className="space-y-6 p-6">
            {/* Header */}
            <div className="rounded-xl bg-white p-6 shadow">
                <div className="flex items-center gap-4">
                    <FaHospital size={32} />
                    <div>
                        <h1 className="text-3xl font-bold">
                            {hospital.hospital_name}
                        </h1>
                        <p className="text-gray-500">
                            Hospital ID: {hospital.hospital_id}
                        </p>
                    </div>
                </div>
            </div>

            {/* Stats */}
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                {statCards.map((card) => (
                    <div
                        key={card.title}
                        className="rounded-xl bg-white p-5 shadow"
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-gray-500">
                                    {card.title}
                                </p>
                                <h2 className="mt-2 text-2xl font-bold">
                                    {card.value}
                                </h2>
                            </div>

                            <div className="rounded-full bg-blue-100 p-3 text-blue-600">
                                {card.icon}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Appointment Status */}
            <div className="rounded-xl bg-white p-6 shadow">
                <h2 className="mb-4 text-xl font-semibold">
                    Appointment Status Summary
                </h2>

                <div className="grid gap-4 md:grid-cols-4">
                    {Object.entries(appointment_status_summary).map(
                        ([key, value]) => (
                            <div
                                key={key}
                                className="rounded-lg border p-4"
                            >
                                <p className="capitalize text-gray-500">
                                    {key.replace("_", " ")}
                                </p>
                                <p className="text-2xl font-bold">{value}</p>
                            </div>
                        )
                    )}
                </div>
            </div>

            {/* Recent Appointments */}
            <div className="rounded-xl bg-white p-6 shadow">
                <h2 className="mb-4 text-xl font-semibold">
                    Recent Appointments
                </h2>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr className="border-b">
                                <th className="p-3 text-left">Token</th>
                                <th className="p-3 text-left">Patient</th>
                                <th className="p-3 text-left">Doctor</th>
                                <th className="p-3 text-left">Time</th>
                                <th className="p-3 text-left">Status</th>
                            </tr>
                        </thead>

                        <tbody>
                            {recent_appointments.map((appointment) => (
                                <tr
                                    key={appointment.appointment_id}
                                    className="border-b"
                                >
                                    <td className="p-3">
                                        {appointment.token_number}
                                    </td>

                                    <td className="p-3">
                                        {appointment.patient_name}
                                    </td>

                                    <td className="p-3">
                                        {appointment.doctor_name}
                                    </td>

                                    <td className="p-3">
                                        {appointment.appointment_time}
                                    </td>

                                    <td className="p-3">
                                        <span className="rounded-full bg-green-100 px-3 py-1 text-sm text-green-700">
                                            {appointment.status}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                    {recent_appointments.length === 0 && (
                        <p className="py-5 text-center text-gray-500">
                            No recent appointments.
                        </p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;