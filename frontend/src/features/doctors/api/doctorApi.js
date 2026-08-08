import api from "@/services/axios.js";

export const createDoctorSchedule = async (data) => {
    const response = await api.post("/doctor-schedules", data);
    return response.data;
};

export const getDoctorAppointments = async (doctor_id, page=1, limit=20) => {
    const response = await api.get(
        `/appointments?doctor_id=${doctor_id}&page=${page}&limit=${limit}&sort_by=appointment_date&sort_order=-1`
    );
    return response.data;
};

export const getAppointmentDetails = async (appointment_id) => {
    const response = await api.get(
        `/appointments/${appointment_id}`
    );
    return response.data;
}

export const getPatientById = async (patient_id) => {
    const response = await api.get(
        `/patients/${patient_id}`
    );
    return response.data;
}

export const updateAppointmentStatus = async (appointment_id, status) => {
    const response = await api.patch(
        `/appointments/${appointment_id}/status`,
        {
            "status": status,
        }
    );
    return response.data;
}