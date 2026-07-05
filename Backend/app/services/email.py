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