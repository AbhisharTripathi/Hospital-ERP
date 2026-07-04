import { createBrowserRouter, Navigate } from "react-router-dom"

import PatientCreatePage from "@/features/patients/pages/PatientCreatePage.jsx"
import PatientListPage from "@/features/patients/pages/PatientListPage.jsx"
import PatientDetailsPage from "@/features/patients/pages/PatientDetailsPage.jsx"
import PatientEditPage from "@/features/patients/pages/PatientEditPage.jsx"
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
import AdminDashboard from "../features/admin/components/AdminDashboard.jsx";
import UserRegisterPage from "../features/admin/pages/UserRegisterPage.jsx";
import { AdminLayout } from "../features/admin/layouts/AdminLayout.jsx"

import OwnerRegisterPage from "@/features/owner/pages/OwnerRegisterPage.jsx"



const router = createBrowserRouter([
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
                                        element: <AdminDashboard />
                                    },
                                    {
                                        path: "user/register",
                                        element: < UserRegisterPage />
                                    },
                                ]                                
                            },
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