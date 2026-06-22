import { useState } from "react";
import { useNavigate } from "react-router-dom";

import PatientForm from "../components/PatientForm.jsx";
import { createPatient } from "../api/patientApi.js";

function PatientCreatePage() {
  const navigate = useNavigate();

  const [isLoading, setIsLoading] = useState(false);

  const handleCreatePatient = async (formData) => {
    try {
      setIsLoading(true);

      const patient = await createPatient(formData);

      console.log(patient);

      navigate("/receptionist/patients");
    } catch (error) {
      console.error(error);
      alert("Failed to create patient");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="border rounded-lg bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-bold mb-6">
          Create Patient
        </h1>

        <PatientForm
          onSubmit={handleCreatePatient}
          isLoading={isLoading}
          submitText="Create Patient"
          showPassword={true}
        />
      </div>
    </div>
  );
}

export default PatientCreatePage;