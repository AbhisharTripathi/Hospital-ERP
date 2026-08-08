import { useEffect, useState } from "react";
import { getAdminDashboard } from "../api/adminApi.js";
import AdminDashboard from "../components/AdminDashboard.jsx";

const AdminDashboardPage = () => {
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchDashboard();
    }, []);

    const fetchDashboard = async () => {
        try {
            const data = await getAdminDashboard();
            setDashboardData(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <h1>Loading...</h1>;
    }

    return <AdminDashboard data={dashboardData} />;
};

export default AdminDashboardPage;