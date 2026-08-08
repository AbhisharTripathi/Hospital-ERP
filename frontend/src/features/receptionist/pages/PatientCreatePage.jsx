import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import PatientForm from "../components/PatientForm.jsx";
import { createPatient } from "../api/patientApi.js";
import { createAppointment } from "../api/receptionistApi.js";

import AppointmentFormSection from "../components/AppointmentFormSection.jsx";

function PatientCreatePage() {
  const navigate = useNavigate();
  const patientFormRef = useRef(null);
  const appointmentSectionRef = useRef(null);

  const [isLoading, setIsLoading] = useState(false);

  const handlePatientAndAppointmentCreate = async () => {
    try {
      setIsLoading(true);

      const patient = await new Promise((resolve, reject) => {
        patientFormRef.current.handleSubmit(async (formData) => {
          try {
            const patient = await createPatient(formData);
            patientFormRef.current.reset();
            resolve(patient);
          } catch (err) {
            reject(err);
          }
        })();
      });

      appointmentSectionRef.current.handleSubmit(async (data) => {
        const payload = {
          patient_id: patient.patient_id,
          doctor_id: data.doctor_id,
          department_id:
            data.department_id,
          appointment_date:
            data.appointment_date,
          appointment_time:
            data.appointment_time,
          appointment_type:
            data.appointment_type,
          reason: data.reason,
          notes: data.notes,
        };
        await createAppointment(
          payload
        );
        appointmentSectionRef.current.reset();
        alert("Appointment created successfully.");

      })();

    } catch (error) {
      console.log(error?.response?.data?.message);
      alert("Failed to create patient and book appointment.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="border border-slate-200 rounded-2xl bg-white shadow-sm">

        <h1 className="text-2xl font-bold mb-1 flex items-center justify-center bg-blue-100 h-20 text-center rounded-t-2xl text-blue-700">
          Create Patient
        </h1>

        <div className="p-6">
          <PatientForm
            onSubmit={() => {console.log("handled in Patient Create page.")}}
            isLoading={isLoading}
            submitText="Add Patient"
            showPassword={true}
            createNewPatient
            ref={patientFormRef}
          />
        </div>

        <div className="px-6 pb-6">
          <AppointmentFormSection ref={appointmentSectionRef} />
        </div>
        <div className="grid justify-items-end">
          <button
            onClick={handlePatientAndAppointmentCreate}
            disabled={isLoading}
            className={
              `px-6
              py-3
              mr-7
              mb-7
              rounded-lg
              bg-blue-600
              text-white
              font-medium
              hover:bg-blue-700
              disabled:opacity-60`
            }
          >Book Appointment</button>
        </div>
      </div>
    </div>
  );
}

export default PatientCreatePage;