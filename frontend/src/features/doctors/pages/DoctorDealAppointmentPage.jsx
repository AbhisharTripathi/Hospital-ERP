import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
    getAppointmentDetails,
    getPatientById,
    updateAppointmentStatus,
    createConsultation,
    createPrescription,
    searchMedicines,
} from "../api/doctorApi";

export default function DoctorDealAppointmentPage() {
    const { appointment_id } = useParams();

    const [appointment, setAppointment] = useState(null);
    const [patient, setPatient] = useState(null);

    const [status, setStatus] = useState("");
    const [isUpdating, setIsUpdating] = useState(false);
    const [loading, setLoading] = useState(true);

    const [isConsultationSubmitting, setIsConsultationSubmitting] =
        useState(false);

    const [isPrescriptionSubmitting, setIsPrescriptionSubmitting] =
        useState(false);

    // --------------------------------------------------
    // Consultation
    // --------------------------------------------------

    const [consultation, setConsultation] = useState({
        chief_complaint: "",
        history_of_present_illness: "",
        physical_examination: "",
        diagnosis: "",
        clinical_notes: "",
        advice: "",
        follow_up_date: "",
    });

    // --------------------------------------------------
    // Prescription
    // --------------------------------------------------

    const [prescription, setPrescription] = useState({
        diagnosis: "",
        advice: "",
        follow_up_date: "",
    });

    const [medicines, setMedicines] = useState([
        {
            medicine_name: "",
            dosage: "",
            frequency: "ONCE_DAILY",
            duration: "",
            timing: "BEFORE_FOOD",
            instructions: "",
        },
    ]);

    // --------------------------------------------------
    // Medicine Search
    // --------------------------------------------------

    const [medicineSearch, setMedicineSearch] = useState({});
    const [medicineSuggestions, setMedicineSuggestions] = useState({});

    // --------------------------------------------------
    // Fetch Appointment + Patient
    // --------------------------------------------------

    useEffect(() => {
        const fetchAppointmentAndPatient = async () => {
            try {
                setLoading(true);

                const appointmentDetails =
                    await getAppointmentDetails(appointment_id);

                setAppointment(appointmentDetails);
                setStatus(appointmentDetails.status);

                const patientDetails = await getPatientById(
                    appointmentDetails.patient_id
                );

                setPatient(patientDetails);
            } catch (err) {
                console.log(
                    err?.response?.data?.message ||
                    "Failed to fetch appointment details"
                );
            } finally {
                setLoading(false);
            }
        };

        fetchAppointmentAndPatient();
    }, [appointment_id]);

    // --------------------------------------------------
    // Appointment Status
    // --------------------------------------------------

    const handleStatusUpdate = async () => {
        try {
            setIsUpdating(true);

            await updateAppointmentStatus(
                appointment.appointment_id,
                status
            );

            setAppointment((prev) => ({
                ...prev,
                status,
            }));

            alert("Appointment status updated successfully!");
        } catch (err) {
            console.log(err?.response?.data?.message);

            alert("Failed to update appointment status.");
        } finally {
            setIsUpdating(false);
        }
    };

    // --------------------------------------------------
    // Consultation Handlers
    // --------------------------------------------------

    const handleConsultationChange = (e) => {
        const { name, value } = e.target;

        setConsultation((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleConsultationSubmit = async (e) => {
        e.preventDefault();

        try {
            setIsConsultationSubmitting(true);

            const data = {
                appointment_id: appointment.appointment_id,
                chief_complaint: consultation.chief_complaint,
                history_of_present_illness:
                    consultation.history_of_present_illness,
                physical_examination:
                    consultation.physical_examination,
                diagnosis: consultation.diagnosis,
                clinical_notes: consultation.clinical_notes,
                advice: consultation.advice,
                follow_up_date:
                    consultation.follow_up_date || null,
            };

            await createConsultation(data);

            alert("Consultation saved successfully!");
        } catch (err) {
            console.log(err?.response?.data);

            alert(
                err?.response?.data?.message ||
                "Failed to save consultation."
            );
        } finally {
            setIsConsultationSubmitting(false);
        }
    };

    // --------------------------------------------------
    // Prescription Handlers
    // --------------------------------------------------

    const handlePrescriptionChange = (e) => {
        const { name, value } = e.target;

        setPrescription((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleMedicineChange = (index, field, value) => {
        setMedicines((prev) =>
            prev.map((medicine, i) =>
                i === index
                    ? {
                          ...medicine,
                          [field]: value,
                      }
                    : medicine
            )
        );
    };

    // --------------------------------------------------
    // Search Medicines
    // --------------------------------------------------

    const handleMedicineSearch = async (index, value) => {
        handleMedicineChange(
            index,
            "medicine_name",
            value
        );

        setMedicineSearch((prev) => ({
            ...prev,
            [index]: value,
        }));

        if (!value.trim()) {
            setMedicineSuggestions((prev) => ({
                ...prev,
                [index]: [],
            }));

            return;
        }

        try {
            const results = await searchMedicines(value);

            setMedicineSuggestions((prev) => ({
                ...prev,
                [index]: results,
            }));
        } catch (err) {
            console.log(
                err?.response?.data ||
                "Medicine search failed"
            );

            setMedicineSuggestions((prev) => ({
                ...prev,
                [index]: [],
            }));
        }
    };

    const selectMedicine = (index, medicine) => {
        /*
         * Adjust this depending on the exact response
         * returned by your medicine API.
         *
         * For example:
         * medicine.name
         * medicine.medicine_name
         */

        const medicineName =
            medicine.medicine_name ||
            medicine.name ||
            "";

        handleMedicineChange(
            index,
            "medicine_name",
            medicineName
        );

        setMedicineSuggestions((prev) => ({
            ...prev,
            [index]: [],
        }));
    };

    // --------------------------------------------------
    // Add Medicine
    // --------------------------------------------------

    const addMedicine = () => {
        setMedicines((prev) => [
            ...prev,
            {
                medicine_name: "",
                dosage: "",
                frequency: "ONCE_DAILY",
                duration: "",
                timing: "BEFORE_FOOD",
                instructions: "",
            },
        ]);
    };

    // --------------------------------------------------
    // Remove Medicine
    // --------------------------------------------------

    const removeMedicine = (index) => {
        if (medicines.length === 1) {
            return;
        }

        setMedicines((prev) =>
            prev.filter((_, i) => i !== index)
        );
    };

    // --------------------------------------------------
    // Submit Prescription
    // --------------------------------------------------

    const handlePrescriptionSubmit = async (e) => {
        e.preventDefault();

        try {
            setIsPrescriptionSubmitting(true);

            const data = {
                appointment_id: appointment.appointment_id,

                diagnosis: prescription.diagnosis,

                advice: prescription.advice,

                follow_up_date:
                    prescription.follow_up_date || null,

                medicines: medicines,
            };

            await createPrescription(data);

            alert("Prescription saved successfully!");
        } catch (err) {
            console.log(err?.response?.data);

            alert(
                err?.response?.data?.message ||
                "Failed to save prescription."
            );
        } finally {
            setIsPrescriptionSubmitting(false);
        }
    };

    // --------------------------------------------------
    // Loading
    // --------------------------------------------------

    if (loading) {
        return (
            <div className="flex justify-center items-center h-screen">
                Loading...
            </div>
        );
    }

    // --------------------------------------------------
    // UI
    // --------------------------------------------------

    return (
        <div className="max-w-7xl mx-auto p-6">

            <h1 className="text-3xl font-bold mb-8">
                Appointment Details
            </h1>

            {/* ================================================= */}
            {/* APPOINTMENT + PATIENT */}
            {/* ================================================= */}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

                {/* Appointment Card */}

                <div className="bg-white rounded-xl shadow-md p-6">

                    <h2 className="text-2xl font-semibold mb-6">
                        Appointment Information
                    </h2>

                    <div className="space-y-3">

                        <p>
                            <strong>Appointment ID:</strong>{" "}
                            {appointment?.appointment_id}
                        </p>

                        <p>
                            <strong>Date:</strong>{" "}
                            {appointment?.appointment_date}
                        </p>

                        <p>
                            <strong>Time:</strong>{" "}
                            {appointment?.appointment_time}
                        </p>

                        <p>
                            <strong>Token Number:</strong>{" "}
                            {appointment?.token_number}
                        </p>

                        <p>
                            <strong>Appointment Type:</strong>{" "}
                            {appointment?.appointment_type}
                        </p>

                        <p>
                            <strong>Reason:</strong>{" "}
                            {appointment?.reason}
                        </p>

                        <p>
                            <strong>Notes:</strong>{" "}
                            {appointment?.notes || "N/A"}
                        </p>

                        <p>
                            <strong>Current Status:</strong>{" "}
                            <span className="font-semibold">
                                {appointment?.status}
                            </span>
                        </p>

                    </div>

                    {/* Status */}

                    <div className="mt-8">

                        <label className="block mb-2 font-medium">
                            Update Status
                        </label>

                        <select
                            value={status}
                            onChange={(e) =>
                                setStatus(e.target.value)
                            }
                            className="w-full border rounded-lg p-3"
                        >
                            <option value="BOOKED">
                                BOOKED
                            </option>

                            <option value="IN_PROGRESS">
                                IN PROGRESS
                            </option>

                            <option value="COMPLETED">
                                COMPLETED
                            </option>

                            <option value="CANCELLED">
                                CANCELLED
                            </option>

                            <option value="NO_SHOW">
                                NO SHOW
                            </option>
                        </select>

                        <button
                            onClick={handleStatusUpdate}
                            disabled={isUpdating}
                            className="mt-4 w-full bg-black text-white py-3 rounded-lg hover:opacity-90 disabled:opacity-50"
                        >
                            {isUpdating
                                ? "Updating..."
                                : "Update Status"}
                        </button>

                    </div>
                </div>

                {/* Patient Card */}

                <div className="bg-white rounded-xl shadow-md p-6">

                    <h2 className="text-2xl font-semibold mb-6">
                        Patient Information
                    </h2>

                    <div className="space-y-3">

                        <p>
                            <strong>Name:</strong>{" "}
                            {patient?.first_name}{" "}
                            {patient?.last_name}
                        </p>

                        <p>
                            <strong>Patient ID:</strong>{" "}
                            {patient?.patient_id}
                        </p>

                        <p>
                            <strong>Gender:</strong>{" "}
                            {patient?.gender}
                        </p>

                        <p>
                            <strong>Date of Birth:</strong>{" "}
                            {patient?.dob}
                        </p>

                        <p>
                            <strong>Blood Group:</strong>{" "}
                            {patient?.blood_group}
                        </p>

                        <p>
                            <strong>Phone:</strong>{" "}
                            {patient?.phone}
                        </p>

                        <p>
                            <strong>Email:</strong>{" "}
                            {patient?.email}
                        </p>

                        <p>
                            <strong>Address:</strong>{" "}
                            {patient?.address}
                        </p>

                        <p>
                            <strong>Emergency Contact:</strong>{" "}
                            {patient?.emergency_contact_name}
                        </p>

                        <p>
                            <strong>Emergency Phone:</strong>{" "}
                            {patient?.emergency_contact_phone}
                        </p>

                        <p>
                            <strong>Status:</strong>{" "}
                            {patient?.status}
                        </p>

                        <p>
                            <strong>Patient Notes:</strong>{" "}
                            {patient?.notes || "N/A"}
                        </p>

                    </div>

                </div>

            </div>

            {/* ================================================= */}
            {/* CONSULTATION */}
            {/* ================================================= */}

            <div className="bg-white rounded-xl shadow-md p-6 mt-8">

                <h2 className="text-2xl font-semibold mb-6">
                    Consultation
                </h2>

                <form
                    onSubmit={handleConsultationSubmit}
                    className="space-y-6"
                >

                    {/* Chief Complaint */}

                    <div>

                        <label className="block font-medium mb-2">
                            Chief Complaint
                        </label>

                        <textarea
                            name="chief_complaint"
                            value={
                                consultation.chief_complaint
                            }
                            onChange={
                                handleConsultationChange
                            }
                            rows={3}
                            placeholder="Enter patient's chief complaint"
                            className="w-full border rounded-lg p-3"
                            required
                        />

                    </div>

                    {/* History */}

                    <div>

                        <label className="block font-medium mb-2">
                            History of Present Illness
                        </label>

                        <textarea
                            name="history_of_present_illness"
                            value={
                                consultation
                                    .history_of_present_illness
                            }
                            onChange={
                                handleConsultationChange
                            }
                            rows={4}
                            placeholder="Describe history of present illness"
                            className="w-full border rounded-lg p-3"
                        />

                    </div>

                    {/* Physical Examination */}

                    <div>

                        <label className="block font-medium mb-2">
                            Physical Examination
                        </label>

                        <textarea
                            name="physical_examination"
                            value={
                                consultation
                                    .physical_examination
                            }
                            onChange={
                                handleConsultationChange
                            }
                            rows={4}
                            placeholder="Enter physical examination findings"
                            className="w-full border rounded-lg p-3"
                        />

                    </div>

                    {/* Diagnosis */}

                    <div>

                        <label className="block font-medium mb-2">
                            Diagnosis
                        </label>

                        <textarea
                            name="diagnosis"
                            value={
                                consultation.diagnosis
                            }
                            onChange={
                                handleConsultationChange
                            }
                            rows={3}
                            placeholder="Enter diagnosis"
                            className="w-full border rounded-lg p-3"
                            required
                        />

                    </div>

                    {/* Clinical Notes */}

                    <div>

                        <label className="block font-medium mb-2">
                            Clinical Notes
                        </label>

                        <textarea
                            name="clinical_notes"
                            value={
                                consultation.clinical_notes
                            }
                            onChange={
                                handleConsultationChange
                            }
                            rows={4}
                            placeholder="Additional clinical notes"
                            className="w-full border rounded-lg p-3"
                        />

                    </div>

                    {/* Advice */}

                    <div>

                        <label className="block font-medium mb-2">
                            Advice
                        </label>

                        <textarea
                            name="advice"
                            value={
                                consultation.advice
                            }
                            onChange={
                                handleConsultationChange
                            }
                            rows={4}
                            placeholder="Enter advice for patient"
                            className="w-full border rounded-lg p-3"
                        />

                    </div>

                    {/* Follow Up */}

                    <div>

                        <label className="block font-medium mb-2">
                            Follow-up Date
                        </label>

                        <input
                            type="date"
                            name="follow_up_date"
                            value={
                                consultation.follow_up_date
                            }
                            onChange={
                                handleConsultationChange
                            }
                            className="border rounded-lg p-3"
                        />

                    </div>

                    <button
                        type="submit"
                        disabled={
                            isConsultationSubmitting
                        }
                        className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50"
                    >
                        {isConsultationSubmitting
                            ? "Saving Consultation..."
                            : "Save Consultation"}
                    </button>

                </form>

            </div>

            {/* ================================================= */}
            {/* PRESCRIPTION */}
            {/* ================================================= */}

            <div className="bg-white rounded-xl shadow-md p-6 mt-8">

                <h2 className="text-2xl font-semibold mb-6">
                    Prescription
                </h2>

                <form
                    onSubmit={handlePrescriptionSubmit}
                    className="space-y-6"
                >

                    {/* Diagnosis */}
{/* 
                    <div>

                        <label className="block font-medium mb-2">
                            Diagnosis
                        </label>

                        <textarea
                            name="diagnosis"
                            value={
                                prescription.diagnosis
                            }
                            onChange={
                                handlePrescriptionChange
                            }
                            rows={3}
                            placeholder="Enter diagnosis"
                            className="w-full border rounded-lg p-3"
                            required
                        />

                    </div> */}

                    {/* Advice */}

                    {/* <div>

                        <label className="block font-medium mb-2">
                            Advice
                        </label>

                        <textarea
                            name="advice"
                            value={
                                prescription.advice
                            }
                            onChange={
                                handlePrescriptionChange
                            }
                            rows={3}
                            placeholder="Enter prescription advice"
                            className="w-full border rounded-lg p-3"
                        />

                    </div> */}

                    {/* Follow Up */}

                    {/* <div>

                        <label className="block font-medium mb-2">
                            Follow-up Date
                        </label>

                        <input
                            type="date"
                            name="follow_up_date"
                            value={
                                prescription.follow_up_date
                            }
                            onChange={
                                handlePrescriptionChange
                            }
                            className="border rounded-lg p-3"
                        />

                    </div> */}

                    {/* Medicines */}

                    <div>

                        <div className="flex justify-between items-center mb-4">

                            <h3 className="text-xl font-semibold">
                                Medicines
                            </h3>

                            <button
                                type="button"
                                onClick={addMedicine}
                                className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
                            >
                                + Add Medicine
                            </button>

                        </div>

                        <div className="space-y-6">

                            {medicines.map(
                                (medicine, index) => (
                                    <div
                                        key={index}
                                        className="border rounded-xl p-5 bg-gray-50"
                                    >

                                        <div className="flex justify-between items-center mb-4">

                                            <h4 className="font-semibold">
                                                Medicine{" "}
                                                {index + 1}
                                            </h4>

                                            {medicines.length >
                                                1 && (
                                                <button
                                                    type="button"
                                                    onClick={() =>
                                                        removeMedicine(
                                                            index
                                                        )
                                                    }
                                                    className="text-red-600 hover:text-red-800"
                                                >
                                                    Remove
                                                </button>
                                            )}

                                        </div>

                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

                                            {/* Medicine Name */}

                                            <div className="relative">

                                                <label className="block mb-2 font-medium">
                                                    Medicine Name
                                                </label>

                                                <input
                                                    type="text"
                                                    value={
                                                        medicine.medicine_name
                                                    }
                                                    onChange={(
                                                        e
                                                    ) =>
                                                        handleMedicineSearch(
                                                            index,
                                                            e
                                                                .target
                                                                .value
                                                        )
                                                    }
                                                    placeholder="Search medicine..."
                                                    className="w-full border rounded-lg p-3"
                                                    required
                                                />

                                                {medicineSuggestions[
                                                    index
                                                ]?.length >
                                                    0 && (
                                                    <div className="absolute z-20 bg-white border rounded-lg shadow-lg w-full mt-1 max-h-60 overflow-y-auto">

                                                        {medicineSuggestions[
                                                            index
                                                        ].map(
                                                            (
                                                                med,
                                                                medIndex
                                                            ) => (
                                                                <button
                                                                    type="button"
                                                                    key={
                                                                        medIndex
                                                                    }
                                                                    onClick={() =>
                                                                        selectMedicine(
                                                                            index,
                                                                            med
                                                                        )
                                                                    }
                                                                    className="block w-full text-left px-4 py-3 hover:bg-gray-100"
                                                                >
                                                                    {med.medicine_name ||
                                                                        med.name}
                                                                </button>
                                                            )
                                                        )}

                                                    </div>
                                                )}

                                            </div>

                                            {/* Dosage */}

                                            <div>

                                                <label className="block mb-2 font-medium">
                                                    Dosage
                                                </label>

                                                <input
                                                    type="text"
                                                    value={
                                                        medicine.dosage
                                                    }
                                                    onChange={(
                                                        e
                                                    ) =>
                                                        handleMedicineChange(
                                                            index,
                                                            "dosage",
                                                            e
                                                                .target
                                                                .value
                                                        )
                                                    }
                                                    placeholder="e.g. 500 mg"
                                                    className="w-full border rounded-lg p-3"
                                                    required
                                                />

                                            </div>

                                            {/* Frequency */}

                                            <div>

                                                <label className="block mb-2 font-medium">
                                                    Frequency
                                                </label>

                                                <select
                                                    value={
                                                        medicine.frequency
                                                    }
                                                    onChange={(
                                                        e
                                                    ) =>
                                                        handleMedicineChange(
                                                            index,
                                                            "frequency",
                                                            e
                                                                .target
                                                                .value
                                                        )
                                                    }
                                                    className="w-full border rounded-lg p-3"
                                                >

                                                    <option value="ONCE_DAILY">
                                                        Once Daily
                                                    </option>

                                                    <option value="TWICE_DAILY">
                                                        Twice Daily
                                                    </option>

                                                    <option value="THREE_TIMES_DAILY">
                                                        Three Times Daily
                                                    </option>

                                                    <option value="FOUR_TIMES_DAILY">
                                                        Four Times Daily
                                                    </option>

                                                    <option value="AS_NEEDED">
                                                        As Needed
                                                    </option>

                                                </select>

                                            </div>

                                            {/* Duration */}

                                            <div>

                                                <label className="block mb-2 font-medium">
                                                    Duration
                                                </label>

                                                <input
                                                    type="text"
                                                    value={
                                                        medicine.duration
                                                    }
                                                    onChange={(
                                                        e
                                                    ) =>
                                                        handleMedicineChange(
                                                            index,
                                                            "duration",
                                                            e
                                                                .target
                                                                .value
                                                        )
                                                    }
                                                    placeholder="e.g. 5 days"
                                                    className="w-full border rounded-lg p-3"
                                                    required
                                                />

                                            </div>

                                            {/* Timing */}

                                            <div>

                                                <label className="block mb-2 font-medium">
                                                    Timing
                                                </label>

                                                <select
                                                    value={
                                                        medicine.timing
                                                    }
                                                    onChange={(
                                                        e
                                                    ) =>
                                                        handleMedicineChange(
                                                            index,
                                                            "timing",
                                                            e
                                                                .target
                                                                .value
                                                        )
                                                    }
                                                    className="w-full border rounded-lg p-3"
                                                >

                                                    <option value="BEFORE_FOOD">
                                                        Before Food
                                                    </option>

                                                    <option value="AFTER_FOOD">
                                                        After Food
                                                    </option>

                                                    <option value="WITH_FOOD">
                                                        With Food
                                                    </option>

                                                    <option value="EMPTY_STOMACH">
                                                        Empty Stomach
                                                    </option>

                                                    <option value="ANY_TIME">
                                                        Any Time
                                                    </option>

                                                </select>

                                            </div>

                                            {/* Instructions */}

                                            <div>

                                                <label className="block mb-2 font-medium">
                                                    Instructions
                                                </label>

                                                <input
                                                    type="text"
                                                    value={
                                                        medicine.instructions
                                                    }
                                                    onChange={(
                                                        e
                                                    ) =>
                                                        handleMedicineChange(
                                                            index,
                                                            "instructions",
                                                            e
                                                                .target
                                                                .value
                                                        )
                                                    }
                                                    placeholder="e.g. Take with water"
                                                    className="w-full border rounded-lg p-3"
                                                />

                                            </div>

                                        </div>

                                    </div>
                                )
                            )}

                        </div>

                    </div>

                    <button
                        type="submit"
                        disabled={
                            isPrescriptionSubmitting
                        }
                        className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 disabled:opacity-50"
                    >
                        {isPrescriptionSubmitting
                            ? "Saving Prescription..."
                            : "Save Prescription"}
                    </button>

                </form>

            </div>

        </div>
    );
}




// import { useEffect, useState } from "react";
// import { useParams } from "react-router-dom";
// import {
//     getAppointmentDetails,
//     getPatientById,
//     updateAppointmentStatus,
// } from "../api/doctorApi";

// export default function DoctorDealAppointmentPage() {
//     const {appointment_id} = useParams();

//     const [appointment, setAppointment] = useState(null);
//     const [patient, setPatient] = useState(null);
//     const [status, setStatus] = useState("");
//     const [isUpdating, setIsUpdating] = useState(false);
//     const [loading, setLoading] = useState(true);

//     useEffect(() => {
//         const fetchAppointmentAndPatient = async () => {
//             try {
//                 setLoading(true);

//                 const appointmentDetails =
//                     await getAppointmentDetails(appointment_id);

//                 setAppointment(appointmentDetails);
//                 setStatus(appointmentDetails.status);

//                 const patientDetails = await getPatientById(
//                     appointmentDetails.patient_id
//                 );

//                 setPatient(patientDetails);
//             } catch (err) {
//                 console.log(err?.response?.data?.message);
//             } finally {
//                 setLoading(false);
//             }
//         };

//         fetchAppointmentAndPatient();
//     }, [appointment_id]);

//     const handleStatusUpdate = async () => {
//         try {
//             setIsUpdating(true);

//             await updateAppointmentStatus(
//                 appointment.appointment_id,
//                 status
//             );

//             setAppointment((prev) => ({
//                 ...prev,
//                 status,
//             }));

//             alert("Appointment status updated successfully!");
//         } catch (err) {
//             console.log(err?.response?.data?.message);
//             alert("Failed to update appointment status.");
//         } finally {
//             setIsUpdating(false);
//         }
//     };

//     if (loading) {
//         return (
//             <div className="flex justify-center items-center h-screen">
//                 Loading...
//             </div>
//         );
//     }

//     return (
//         <div className="max-w-7xl mx-auto p-6">
//             <h1 className="text-3xl font-bold mb-8">
//                 Appointment Details
//             </h1>

//             <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
//                 {/* Appointment Card */}
//                 <div className="bg-white rounded-xl shadow-md p-6">
//                     <h2 className="text-2xl font-semibold mb-6">
//                         Appointment Information
//                     </h2>

//                     <div className="space-y-3">
//                         <p>
//                             <strong>Appointment ID:</strong>{" "}
//                             {appointment?.appointment_id}
//                         </p>

//                         <p>
//                             <strong>Date:</strong>{" "}
//                             {appointment?.appointment_date}
//                         </p>

//                         <p>
//                             <strong>Time:</strong>{" "}
//                             {appointment?.appointment_time}
//                         </p>

//                         <p>
//                             <strong>Token Number:</strong>{" "}
//                             {appointment?.token_number}
//                         </p>

//                         <p>
//                             <strong>Appointment Type:</strong>{" "}
//                             {appointment?.appointment_type}
//                         </p>

//                         <p>
//                             <strong>Reason:</strong>{" "}
//                             {appointment?.reason}
//                         </p>

//                         <p>
//                             <strong>Notes:</strong>{" "}
//                             {appointment?.notes || "N/A"}
//                         </p>

//                         <p>
//                             <strong>Current Status:</strong>{" "}
//                             <span className="font-semibold">
//                                 {appointment?.status}
//                             </span>
//                         </p>
//                     </div>

//                     <div className="mt-8">
//                         <label className="block mb-2 font-medium">
//                             Update Status
//                         </label>

//                         <select
//                             value={status}
//                             onChange={(e) =>
//                                 setStatus(e.target.value)
//                             }
//                             className="w-full border rounded-lg p-3"
//                         >
//                             <option value="BOOKED">
//                                 BOOKED
//                             </option>
//                             <option value="IN_PROGRESS">
//                                 IN PROGRESS
//                             </option>
//                             <option value="COMPLETED">
//                                 COMPLETED
//                             </option>
//                             <option value="CANCELLED">
//                                 CANCELLED
//                             </option>
//                             <option value="NO_SHOW">
//                                 NO SHOW
//                             </option>
//                         </select>

//                         <button
//                             onClick={handleStatusUpdate}
//                             disabled={isUpdating}
//                             className="mt-4 w-full bg-black text-white py-3 rounded-lg hover:opacity-90 disabled:opacity-50"
//                         >
//                             {isUpdating
//                                 ? "Updating..."
//                                 : "Update Status"}
//                         </button>
//                     </div>
//                 </div>

//                 {/* Patient Card */}
//                 <div className="bg-white rounded-xl shadow-md p-6">
//                     <h2 className="text-2xl font-semibold mb-6">
//                         Patient Information
//                     </h2>

//                     <div className="space-y-3">
//                         <p>
//                             <strong>Name:</strong>{" "}
//                             {patient?.first_name}{" "}
//                             {patient?.last_name}
//                         </p>

//                         <p>
//                             <strong>Patient ID:</strong>{" "}
//                             {patient?.patient_id}
//                         </p>

//                         <p>
//                             <strong>Gender:</strong>{" "}
//                             {patient?.gender}
//                         </p>

//                         <p>
//                             <strong>Date of Birth:</strong>{" "}
//                             {patient?.dob}
//                         </p>

//                         <p>
//                             <strong>Blood Group:</strong>{" "}
//                             {patient?.blood_group}
//                         </p>

//                         <p>
//                             <strong>Phone:</strong>{" "}
//                             {patient?.phone}
//                         </p>

//                         <p>
//                             <strong>Email:</strong>{" "}
//                             {patient?.email}
//                         </p>

//                         <p>
//                             <strong>Address:</strong>{" "}
//                             {patient?.address}
//                         </p>

//                         <p>
//                             <strong>Emergency Contact:</strong>{" "}
//                             {patient?.emergency_contact_name}
//                         </p>

//                         <p>
//                             <strong>Emergency Phone:</strong>{" "}
//                             {patient?.emergency_contact_phone}
//                         </p>

//                         <p>
//                             <strong>Status:</strong>{" "}
//                             {patient?.status}
//                         </p>

//                         <p>
//                             <strong>Patient Notes:</strong>{" "}
//                             {patient?.notes || "N/A"}
//                         </p>
//                     </div>
//                 </div>
//             </div>
//         </div>
//     );
// }