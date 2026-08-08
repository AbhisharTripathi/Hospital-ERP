import api from "@/services/axios"

export const registerUser = async (userData) => {
    const response = await api.post(
        "/users",
        userData
    );
    return response.data;
}

export const registerDepartment = async (departmentData) => {
    const response = await api.post(
        "/departments",
        departmentData
    );
    return response.data;
}

export const getDepartments = async () => {
    const response = await api.get("/departments");
    return response.data;
}

export const createDoctor = async (doctorData) => {
    const response = await api.post(
        "/doctors/profile",
        doctorData
    );
    return response.data;
}

export const getAdminDashboard = async () => {
    const response = await api.get("/dashboard/admin");
    return response.data;
}