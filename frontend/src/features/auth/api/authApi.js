import api from "@/services/axios.js"

export const loginUser = async (loginData) => {
    const response = await api.post(
        "/auth/login",
        loginData
    );
    return response.data;
}

export const getCurrentUser = async () => {
    const response = await api.get(
      "/auth/me"
    );

    return response.data;
  };


export const setPassword = async (token, password) => {
    const response = await api.post(
        "/auth/set-password",
        { token, password }
    );
    return response.data;
};