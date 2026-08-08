import api from "@/services/axios.js";

export const getDoctorsByDepartment = async (
    departmentId
) => {
    const response = await api.get(
        `/doctors/department/${departmentId}`
    );
    return response.data;
};

export const createAppointment = async (
    payload
) => {
    const response = await api.post(
        "/appointments",
        payload
    );
    return response.data;
};

export const getDepartments = async () => {
    const response = await api.get("/departments");
    return response.data;
}