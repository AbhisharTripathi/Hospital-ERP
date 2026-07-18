from fastapi_mail import (
    FastMail,
    MessageSchema,
    MessageType
)

from app.core.mail import conf


class EmailService:

    async def send_email(
        self,
        subject: str,
        recipients: list[str],
        body: str
    ):

        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=MessageType.html
        )

        fm = FastMail(conf)

        await fm.send_message(message)

    async def send_welcome_email(
        self,
        owner_name: str,
        hospital_name: str,
        hospital_id: str,
        user_id: str,
        email: str
    ):

        body = f"""
        <h2>🎉 Welcome to Hospital ERP</h2>

        <p>Hello <b>{owner_name}</b>,</p>

        <p>Your hospital has been registered successfully.</p>

        <hr>

        <p><b>Hospital Name:</b> {hospital_name}</p>

        <p><b>Hospital ID:</b> {hospital_id}</p>

        <p><b>User ID:</b> {user_id}</p>

        <p><b>Email:</b> {email}</p>

        <p><b>Role:</b> SUPER ADMIN</p>

        <hr>

        <p>You can now login to Hospital ERP.</p>

        <br>

        <h4>Thank you ❤️</h4>
        """

        await self.send_email(
            subject="Welcome to Hospital ERP 🎉",
            recipients=[email],
            body=body
        )
    
    
    async def send_invitation_email(
        self,
        employee_name: str,
        email: str,
        invite_token: str
    ):
        invite_link = (
            f"http://localhost:5173/set-password"
            f"?token={invite_token}"
        )

        subject = "Hospital ERP - Complete Your Account"

        body = f"""
        <h2>Welcome to Hospital ERP</h2>

        <p>Hello <b>{employee_name}</b>,</p>

        <p>Your account has been created successfully.</p>

        <p>Please click the button below to create your password.</p>

        <br>

        <a
            href="{invite_link}"
            style="
                background:#2563eb;
                color:white;
                padding:12px 20px;
                text-decoration:none;
                border-radius:6px;
            "
        >
            Create Password
        </a>

        <br><br>

        <p>This invitation link will expire in <b>24 hours</b>.</p>

        <p>If you were not expecting this email, please ignore it.</p>

        <br>

        <p>Hospital ERP Team</p>
        """

        await self.send_email(
            subject=subject,
            recipients=[email],
            body=body
        )

    async def send_doctor_profile_created_email(
        self,
        doctor_name: str,
        email: str,
        doctor_id: str,
        department_name: str,
        specialization: str
    ):

        subject = "Doctor Profile Activated - Hospital ERP"

        body = f"""
        <html>
        <body>

            <h2>Welcome Dr. {doctor_name}</h2>

            <p>
                Your Doctor Profile has been successfully created.
            </p>

            <table border="1" cellpadding="8" cellspacing="0">

                <tr>
                    <td><b>Doctor ID</b></td>
                    <td>{doctor_id}</td>
                </tr>

                <tr>
                    <td><b>Department</b></td>
                    <td>{department_name}</td>
                </tr>

                <tr>
                    <td><b>Specialization</b></td>
                    <td>{specialization}</td>
                </tr>

            </table>

            <br>

            <p>
                You can now log in to Hospital ERP and start using your doctor dashboard.
            </p>

            <br>

            <p>
                Regards,<br>
                Hospital ERP Team ❤️
            </p>

        </body>
        </html>
        """

        await self.send_email(
            
            subject=subject,
            recipients=[email],
            body=body
        )
   