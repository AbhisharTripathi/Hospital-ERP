import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import PatientCard from "../components/PatientCard.jsx";

import { getPatients } from "../api/patientApi";

function PatientListPage() {
  const [patients, setPatients] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // const {
  //   data: patients = [],
  //   isLoading,
  //   error,
  // } = useQuery({
  //   queryKey: ["patients"],
  //   queryFn: getPatients,
  // });

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    try {
      setIsLoading(true);

      const data = await getPatients();

      setPatients(data);
    } catch (err) {
      console.error(err);
      setError(
        "Failed to load patients"
      );
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="p-6">
        Loading patients...
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

  return (
    <div className="space-y-6 px-2">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">
          Patients
        </h1>

        <Link
          to="/receptionist/patients/create"
          className="py-2.5 px-5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Create Patient
        </Link>
      </div>

      {/* Table */}
      <div>
            {patients.length === 0 ? (
                <h3
                  className="text-center p-6"
                >
                  No patients found
                </h3>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                {patients.map((patient) => (
                  <PatientCard key={patient.patient_id} {...patient} />
                ))}
              </div>
            )}
      </div>
    </div>
  );
}

export default PatientListPage;