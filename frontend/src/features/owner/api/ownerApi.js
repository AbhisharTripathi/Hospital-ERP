import api from "@/services/axios.js";

export const registerOwner = async (data) => {
    const response = await api.post(
        "/auth/register-hospital",
        data
    );
    return response.data;
}