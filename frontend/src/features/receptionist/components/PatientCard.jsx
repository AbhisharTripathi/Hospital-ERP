import { Link } from 'react-router-dom';
import { FaEye, FaEdit, FaPhoneAlt, FaEnvelope } from "react-icons/fa";

function PatientCard({
  patient_id,
  first_name,
  last_name,
  phone,
  gender,
  email,
}) {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 hover:shadow-lg transition-all duration-300">
      
      <div className="flex justify-between items-start">
        <div className="flex gap-3">
          <div className="h-12 w-12 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-semibold">
            {first_name?.[0]}
            {last_name?.[0]}
          </div>

          <div>
            <h3 className="font-semibold text-slate-800 text-lg">
              {first_name} {last_name}
            </h3>

            <p className="text-sm text-slate-500">
              Patient ID: {patient_id}
            </p>
          </div>
        </div>

        <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700">
          {gender}
        </span>
      </div>

      <div className="border-t border-slate-100 my-4"></div>

      {/* Info */}
      <div className="space-y-3">
        <div className="flex items-center gap-3">
          <FaPhoneAlt className="text-slate-400" />
          <span className="text-slate-700">{phone}</span>
        </div>

        <div className="flex items-center gap-3">
          <FaEnvelope className="text-slate-400" />
          <span className="text-slate-700 truncate">
            {email || "-"}
          </span>
        </div>
      </div>

      <div className="flex gap-3 mt-5">
        <Link
          to={`/receptionist/patients/${patient_id}`}
          className="flex-1 flex items-center justify-center gap-2 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          <FaEye />
          View
        </Link>

        <Link
          to={`/receptionist/patients/${patient_id}/edit`}
          className="flex-1 flex items-center justify-center gap-2 py-2.5 border border-slate-300 rounded-lg hover:border-blue-600 hover:text-blue-600 transition"
        >
          <FaEdit />
          Edit
        </Link>
      </div>
    </div>
  );
}

export default PatientCard;