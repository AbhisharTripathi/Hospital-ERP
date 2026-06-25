import api from "@/services/axios"

export const registerUser = async (userData) => {
    const response = await api.post(
        "/auth/register",
        userData
    );
    return response.data;
}