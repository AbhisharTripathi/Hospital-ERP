import { createBrowserRouter, Navigate } from "react-router-dom"
import AppLayout from "@/layouts/AppLayout.jsx"
import AuthLayout from "@/layouts/AuthLayout.jsx"
import NotFound from "@/pages/NotFound.jsx"
import Welcome from "@/pages/Welcome.jsx"
import LoginPage from "@/features/auth/pages/LoginPage.jsx"
import ProtectedRoute from "@/features/auth/pages/ProtectedRoute.jsx"
import PatientCreatePage from "@/features/patients/pages/PatientCreatePage.jsx"
import PatientListPage from "@/features/patients/pages/PatientListPage.jsx"
import PatientDetailsPage from "@/features/patients/pages/PatientDetailsPage.jsx"
import PatientEditPage from "@/features/patients/pages/PatientEditPage.jsx"

const router = createBrowserRouter([
    {
        path: "/",
        element: <Welcome />,
        // element: <Navigate to="/dashboard" replace />,
    },
    {
        path: "/auth",
        element: <AuthLayout />,
        errorElement: <NotFound />,
        children: [
            {
                index: true,
                path: "login",
                element: <LoginPage />
            },
            // {
            //     path: "dashboard",
            //     element: <Dashboard />,
            //     // loader: dashboardLoader,
            // }
        ]
    },
    {
        element: (
            <ProtectedRoute>
                <AppLayout/>
            </ProtectedRoute>
        ),
        children: [
            // {
            //     path: "/dashboard",
            //     element: <DashboardPage />

            // },
            {
                path: "/patients",
                children: [
                    {
                        index: true,
                        element: <PatientListPage />,
                    },
                    {
                        path: "create",
                        element: <PatientCreatePage />,
                    },
                    {
                        path: ":patientId",
                        element: <PatientDetailsPage />,
                    },
                    {
                        path: ":patientId/edit",
                        element: <PatientEditPage />,
                    },
                ],
            },
        ]
    },
    {
        path: "*",
        element: <NotFound />,
    },
])

export default router;