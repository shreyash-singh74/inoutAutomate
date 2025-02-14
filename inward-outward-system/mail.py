from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from config import EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_FROM
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

mail_config = ConnectionConfig(
    MAIL_USERNAME=EMAIL_USERNAME or "",
    MAIL_PASSWORD=EMAIL_PASSWORD,  # type: ignore
    MAIL_FROM=EMAIL_USERNAME,  # type: ignore
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME=EMAIL_FROM,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

mail = FastMail(config=mail_config)

async def create_message(recipients: list[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )
    await mail.send_message(message=message)