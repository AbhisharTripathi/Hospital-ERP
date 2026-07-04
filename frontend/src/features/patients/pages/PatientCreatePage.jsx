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
      <div className="border border-slate-200 rounded-2xl bg-white shadow-sm">

        <h1 className="text-2xl font-bold mb-1 flex items-center justify-center bg-blue-100 h-20 text-center rounded-t-2xl text-blue-700">
          Create Patient
        </h1>
        
        <div className="p-6">
          <PatientForm
            onSubmit={handleCreatePatient}
            isLoading={isLoading}
            submitText="Add Patient"
            showPassword={true}
          />
        </div>
      </div>
    </div>
  );
}

export default PatientCreatePage;