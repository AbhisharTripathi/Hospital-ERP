import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

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
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">
          Patients
        </h1>

        <Link
          to="/receptionist/patients/create"
          className="px-4 py-2 bg-black text-white rounded-md"
        >
          Create Patient
        </Link>
      </div>

      {/* Table */}
      <div className="overflow-hidden border rounded-lg">
        <table className="w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="text-left p-3">
                Patient ID
              </th>

              <th className="text-left p-3">
                Name
              </th>

              <th className="text-left p-3">
                Phone
              </th>

              <th className="text-left p-3">
                Gender
              </th>

              <th className="text-left p-3">
                Email
              </th>

              <th className="text-left p-3">
                Actions
              </th>
            </tr>
          </thead>

          <tbody>
            {patients.length === 0 ? (
              <tr>
                <td
                  colSpan="6"
                  className="text-center p-6"
                >
                  No patients found
                </td>
              </tr>
            ) : (
              patients.map((patient) => (
                <tr
                  key={patient._id}
                  className="border-t"
                >
                  <td className="p-3">
                    {patient.patient_id}
                  </td>

                  <td className="p-3">
                    {patient.first_name}{" "}
                    {patient.last_name}
                  </td>

                  <td className="p-3">
                    {patient.phone}
                  </td>

                  <td className="p-3 capitalize">
                    {patient.gender}
                  </td>

                  <td className="p-3">
                    {patient.email || "-"}
                  </td>

                  <td className="p-3">
                    <div className="flex gap-2">
                      <Link
                        to={`/receptionist/patients/${patient.patient_id}`}
                        className="px-3 py-1 border rounded"
                      >
                        View
                      </Link>

                      <Link
                        to={`/receptionist/patients/${patient.patient_id}/edit`}
                        className="px-3 py-1 border rounded"
                      >
                        Edit
                      </Link>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PatientListPage;