import { useNavigate } from "react-router-dom";
function AppointmentCard({
    appointment,
}) {
    const navigate = useNavigate();
    const dealThisAppointment = () => {
        navigate(`/doctor/appointments/${appointment.appointment_id}`);
    };

    return (
        <div className="rounded-lg border bg-white p-5 shadow-sm" onClick={dealThisAppointment}>
            <div className="mb-4 flex items-center justify-between">
                <h2 className="text-lg font-semibold">
                    {
                        appointment.appointment_id
                    }
                </h2>

                <span className="rounded bg-blue-100 px-3 py-1 text-sm">
                    {
                        appointment.status
                    }
                </span>
            </div>

            <div className="space-y-2">
                <p>
                    <strong>
                        Patient:
                    </strong>{" "}
                    {
                        appointment.patient_name
                    }
                </p>

                <p>
                    <strong>
                        Token:
                    </strong>{" "}
                    {
                        appointment.token_number
                    }
                </p>

                <p>
                    <strong>
                        Date:
                    </strong>{" "}
                    {
                        appointment.appointment_date
                    }
                </p>

                <p>
                    <strong>
                        Time:
                    </strong>{" "}
                    {
                        appointment.appointment_time
                    }
                </p>

                <p>
                    <strong>
                        Type:
                    </strong>{" "}
                    {
                        appointment.appointment_type
                    }
                </p>

                {/* <p>
                    <strong>
                        Department:
                    </strong>{" "}
                    {
                        appointment.department_id
                    }
                </p> */}

                {appointment.reason && (
                    <p>
                        <strong>
                            Reason:
                        </strong>{" "}
                        {
                            appointment.reason
                        }
                    </p>
                )}

                {appointment.notes && (
                    <p>
                        <strong>
                            Notes:
                        </strong>{" "}
                        {
                            appointment.notes
                        }
                    </p>
                )}
            </div>
        </div>
    );
}

export default AppointmentCard;