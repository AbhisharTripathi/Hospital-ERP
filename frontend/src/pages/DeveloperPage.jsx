import { Link } from "react-router-dom";

const routes = [
    {
        title: "Auth",
        links: [
            { name: "Login", path: "/auth/login" },
            { name: "Owner Register", path: "/auth/register" },
            { name: "Set Password", path: "/auth/set-password" },
        ],
    },
    {
        title: "Admin",
        links: [
            { name: "Dashboard", path: "/admin" },
            { name: "Register User", path: "/admin/user/register" },
            {
                name: "Register Department",
                path: "/admin/departments/register",
            },
        ],
    },
    {
        title: "Receptionist",
        links: [
            { name: "Dashboard", path: "/receptionist" },
            {
                name: "Patient List",
                path: "/receptionist/patients",
            },
            {
                name: "Create Patient",
                path: "/receptionist/patients/create",
            },
            {
                name: "Patient Details",
                path: "/receptionist/patients/PAT-2026-00001",
            },
            {
                name: "Edit Patient",
                path: "/receptionist/patients/PAT-2026-00001/edit",
            },
            {
                name: "Create Appointment",
                path: "/receptionist/appointments/create",
            },
        ],
    },
    {
        title: "Doctor",
        links: [
            {
                name: "Dashboard",
                path: "/doctor",
            },
            {
                name: "Schedule",
                path: "/doctor/schedule"
            },
        ],
    },
];

function DeveloperPage() {
    return (
        <div className="min-h-screen bg-slate-100 p-8">
            <div className="mx-auto max-w-6xl">
                <h1 className="mb-2 text-4xl font-bold">
                    Developer Panel
                </h1>

                <p className="mb-8 text-gray-500">
                    Quick access to all pages during development.
                </p>

                <div className="grid gap-6 md:grid-cols-2">
                    {routes.map((section) => (
                        <div
                            key={section.title}
                            className="rounded-lg border bg-white p-6 shadow"
                        >
                            <h2 className="mb-4 text-2xl font-semibold">
                                {section.title}
                            </h2>

                            <div className="space-y-3">
                                {section.links.map((link) => (
                                    <Link
                                        key={link.path}
                                        to={link.path}
                                        className="block rounded-md border p-3 transition hover:bg-slate-50"
                                    >
                                        <div className="font-medium">
                                            {link.name}
                                        </div>

                                        <div className="text-sm text-gray-500">
                                            {link.path}
                                        </div>
                                    </Link>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default DeveloperPage;