import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { getPatientById } from "../api/patientApi";

function PatientDetailsPage() {
  const { patientId } = useParams();

  const [patient, setPatient] = useState(null);
  const [isLoading, setIsLoading] =
    useState(true);
  const [error, setError] =
    useState(null);

  useEffect(() => {
    fetchPatient();
  }, [patientId]);

  const fetchPatient = async () => {
    try {
      setIsLoading(true);

      const data =
        await getPatientById(patientId);

      setPatient(data);
    } catch (err) {
      console.error(err);

      setError(
        "Failed to fetch patient details"
      );
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="p-6">
        Loading patient details...
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
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">
            Patient Details
          </h1>

          <p className="text-gray-500">
            {patient.patient_id}
          </p>
        </div>

        <Link
          to={`/receptionist/patients/${patientId}/edit`}
          className="px-4 py-2 bg-black text-white rounded-md"
        >
          Edit Patient
        </Link>
      </div>

      {/* Card */}
      <div className="border rounded-lg bg-white p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          <InfoField
            label="First Name"
            value={patient.first_name}
          />

          <InfoField
            label="Last Name"
            value={patient.last_name}
          />

          <InfoField
            label="Phone"
            value={patient.phone}
          />

          <InfoField
            label="Email"
            value={patient.email}
          />

          <InfoField
            label="Gender"
            value={patient.gender}
          />

          <InfoField
            label="Date of Birth"
            value={patient.dob}
          />

          <InfoField
            label="Blood Group"
            value={patient.blood_group}
          />

          <InfoField
            label="Emergency Contact Name"
            value={
              patient.emergency_contact_name
            }
          />

          <InfoField
            label="Emergency Contact Phone"
            value={
              patient.emergency_contact_phone
            }
          />

          <div className="md:col-span-2">
            <p className="text-sm text-gray-500">
              Address
            </p>

            <p className="mt-1">
              {patient.address || "-"}
            </p>
          </div>

          <div className="md:col-span-2">
            <p className="text-sm text-gray-500">
              Notes
            </p>

            <p className="mt-1">
              {patient.notes || "-"}
            </p>
          </div>

        </div>
      </div>
    </div>
  );
}

function InfoField({ label, value }) {
  return (
    <div>
      <p className="text-sm text-gray-500">
        {label}
      </p>

      <p className="font-medium mt-1">
        {value || "-"}
      </p>
    </div>
  );
}

export default PatientDetailsPage;