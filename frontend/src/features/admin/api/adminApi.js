import api from "@/services/axios"

export const registerUser = async (userData) => {
    const response = await api.post(
        "/users",
        userData
    );
    return response.data;
}