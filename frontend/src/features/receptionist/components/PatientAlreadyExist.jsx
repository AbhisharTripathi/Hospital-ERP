import InfoField from "./InfoField.jsx"

export default function PatientAlreadyExist(patient){
    return (
        <div>
            <InfoField
                label='First name'
                value={patient.first_name}
            />

            <InfoField
                label="Last name"
                value={patient.last_name}
            />

            <InfoField 
                label="Date of Birth"
                value={patient.dob}
            />

            <InfoField 
                label="Gender"
                value={patient.gender}
            />

            <InfoField
                label="Phone no"
                value={patient.phone}
            />

            <InfoField 
                label="Email"
                value={patient.email}
            />
        </div>
    )
}
