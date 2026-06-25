import { useEffect, useState } from "react";
import {
  useNavigate,
  useParams,
} from "react-router-dom";

import PatientForm from "../components/PatientForm";

import {
  getPatientById,
  updatePatient,
} from "../api/patientApi";

function PatientEditPage() {
  const { patientId } = useParams();

  const navigate = useNavigate();

  const [patient, setPatient] = useState(null);

  const [isLoading, setIsLoading] = useState(true);

  const [isSaving, setIsSaving] = useState(false);

  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPatient();
  }, [patientId]);

  const fetchPatient = async () => {
    try {
      setIsLoading(true);

      const data = await getPatientById(patientId);

      setPatient(data);
    } catch (err) {
      console.error(err);

      setError(
        "Failed to load patient"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdatePatient =
    async (formData) => {
      try {
        setIsSaving(true);

        await updatePatient(
          patientId,
          formData
        );

        navigate(
          `/receptionist/patients/${patientId}`
        );
      } catch (err) {
        console.error(err);

        alert(
          "Failed to update patient"
        );
      } finally {
        setIsSaving(false);
      }
    };

  if (isLoading) {
    return (
      <div className="p-6">
        Loading patient...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-red-500">
        {error}
      </div>
    );
  }

  if (!patient) {
    return (
      <div className="p-6">
        Patient not found
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="border rounded-lg bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-bold mb-6">
          Edit Patient
        </h1>

        <PatientForm
          initialData={patient}
          onSubmit={
            handleUpdatePatient
          }
          isLoading={isSaving}
          submitText="Update Patient"
        />
      </div>
    </div>
  );
}

export default PatientEditPage;