import api from "@/services/axios.js";

export const createPatient = async (
  patientData
) => {
  const response = await api.post(
    "/patients",
    patientData
  );

  return response.data;
};

export const getPatients = async () => {
  const response = await api.get(
    "/patients"
  );

  return response.data;
};

export const getPatientById = async (
  patientId
) => {
  const response = await api.get(
    `/patients/${patientId}`
  );

  return response.data;
};

export const updatePatient = async (
  patientId,
  data
) => {
  const response = await api.put(
    `/patients/${patientId}`,
    data
  );

  return response.data;
};

export const deletePatient = async (
  patientId
) => {
  const response = await api.delete(
    `/patients/${patientId}`
  );

  return response.data;
};