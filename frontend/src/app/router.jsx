import { createBrowserRouter, Navigate } from "react-router-dom"

import PatientCreatePage from "@/features/receptionist/pages/PatientCreatePage.jsx"
import PatientListPage from "@/features/receptionist/pages/PatientListPage.jsx"
import PatientDetailsPage from "@/features/receptionist/pages/PatientDetailsPage.jsx"
import PatientEditPage from "@/features/receptionist/pages/PatientEditPage.jsx"
import AppLayout from "@/layouts/AppLayout.jsx";

import Welcome from "@/pages/Welcome.jsx"
import Unauthorized from "@/pages/Unauthorized.jsx"
import AuthLayout from "@/features/auth/layouts/AuthLayout.jsx"
import LoginPage from "@/features/auth/pages/LoginPage.jsx"
import AppAuthWrapper from "@/features/auth/pages/AppAuthWrapper.jsx"
import RoleBasedRedirect from "@/features/auth/pages/RoleBasedRedirect.jsx"
import ProtectedRoute from "@/features/auth/pages/ProtectedRoute.jsx"
import NotFound from "@/pages/NotFound.jsx"
import ReceptionistLayout from "../features/receptionist/layouts/ReceptionistLayout.jsx"
import ReceptionistDashboard from "../features/receptionist/components/ReceptionistDashboard.jsx"
import AdminDashboardPage from "../features/admin/pages/AdminDashboardPage.jsx";
import AddDepartment from "../features/admin/pages/AddDepartment.jsx";
import UserRegisterPage from "../features/admin/pages/UserRegisterPage.jsx";
import { AdminLayout } from "../features/admin/layouts/AdminLayout.jsx"

import OwnerRegisterPage from "@/features/owner/pages/OwnerRegisterPage2.jsx"
import UserSetPasswordPage from "@/features/auth/pages/UserSetPasswordPage.jsx"

import DoctorLayout from "../features/doctors/layouts/DoctorLayout.jsx";
import DoctorDashboardPage from "../features/doctors/pages/DoctorDashboardPage.jsx";
import DoctorSchedulePage from "../features/doctors/pages/DoctorSchedulePage.jsx";
import DoctorAppointmentsPage from "../features/doctors/pages/DoctorAppointmentsPage.jsx";
import DoctorDealAppointmentPage from "../features/doctors/pages/DoctorDealAppointmentPage.jsx";

import CreateAppointmentPage from "../features/receptionist/pages/CreateAppointmentPage.jsx";

import DeveloperPage from "@/pages/DeveloperPage.jsx";



const router = createBrowserRouter([
    {
        path: "/dev",
        element: <DeveloperPage />,
    },
    {
        path: "/welcome",
        element: <Welcome />,
    },
    {
        element: <AppLayout />,
        children: [
            {
                path: "/unauthorized",
                element: <Unauthorized />
            },
            {
                path: "/auth",
                element: <AuthLayout />,
                children: [
                    {
                        index: true,
                        element: <Navigate to="/auth/login" replace />
                    },
                    {
                        path: "login",
                        element: <LoginPage />
                    },
                    {
                        path: "register",
                        element: <OwnerRegisterPage />
                    },
                    {
                        path: "set-password",
                        element: <UserSetPasswordPage />
                    }
                ]
            },
            {
                path: "/",
                element: <AppAuthWrapper />,
                children: [
                    {
                        index: true,
                        element: <RoleBasedRedirect />
                    },
                    {
                        path: "receptionist",
                        element: <ProtectedRoute allowedRoles={['RECEPTIONIST']} />,
                        children: [
                            {
                                element: <ReceptionistLayout />,
                                children: [
                                    {
                                        index: true,
                                        element: <ReceptionistDashboard />
                                    },
                                    {
                                        path: "patients",
                                        element: <PatientListPage />
                                    },
                                    {
                                        path: "patients/create",
                                        element: <PatientCreatePage />,
                                    },
                                    {
                                        path: "patients/:patientId",
                                        element: <PatientDetailsPage />,
                                    },
                                    {
                                        path: "patients/:patientId/edit",
                                        element: <PatientEditPage />,
                                    },
                                    {
                                        path: "appointments/create",
                                        element: <CreateAppointmentPage />,
                                    },
                                ]
                            }
                        ]
                    },
                    {
                        path: "admin",
                        element: <ProtectedRoute allowedRoles={["ADMIN"]} />,
                        children: [
                            {
                                element: <AdminLayout />,
                                children: [
                                    {
                                        index: true,
                                        element: <AdminDashboardPage />
                                    },
                                    {
                                        path: "user/register",
                                        element: < UserRegisterPage />
                                    },
                                    {
                                        path: "departments/register",
                                        element: < AddDepartment />
                                    },
                                ]                                
                            },
                        ]
                    },
                    {
                        path: "doctor",
                        element: <ProtectedRoute allowedRoles={["DOCTOR"]} />,
                        children: [
                            {
                                element: <DoctorLayout />,
                                children: [
                                    {
                                        index: true,
                                        element: <DoctorDashboardPage />
                                    },
                                    {
                                        path: "schedule",
                                        element: <DoctorSchedulePage />
                                    },
                                    {
                                        path: "appointments",
                                        element: <DoctorAppointmentsPage />
                                    },
                                    {
                                        path: "appointments/:appointment_id",
                                        element: <DoctorDealAppointmentPage />
                                    },
                                ]
                            }
                        ]
                    },
                ]
            },
        ]
    },
    
    {
        path: "*",
        element: <NotFound />,
    },
])

export default router;