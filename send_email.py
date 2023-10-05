import re
import sys

import smtplib

from email.message import EmailMessage

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from validate_email_address import validate_email

from decouple import config


class EmailRequest(BaseModel):
    """Data type class to send the request"""

    to: str = None
    subject: str = None
    message: str = None


app = FastAPI()

# Connect to smtp server
gmail_user = config('GMAIL')
gmail_password = config('PASSWORD')

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)


def check_email(email: str):
    """Check email for validity
    Args:
        email (str): mail for verification

    Returns:
        Tru if the email is valid
    """

    match = re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email)
    result = match is not None
    return result


def send_email(to: str, subject: str, text: str):
    """Send email
    Args:
        to (str): mail for sending
        subject (str): Subject os message
        text (str): Text of message

    Returns:
        Tru if the email send successfully
    """
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to
    msg.set_content(text)

    server.send_message(msg)

    return True


@app.post("/send_email")
async def root(email: EmailRequest):
    """Fastapi endpoint for sending email
    Args:
        email (EmailRequest): class of email message

    Returns:
        200:
            result: True
            message: Email send successfully!
    """
    if not check_email(email.to):
        # Check email validation
        sys.stdout.write(f'WARN:\tEmail {email.to} is not valid!\n')

        raise HTTPException(
            status_code=400,
            detail=f"Email {email.to} is not valid!",
        )

    elif validate_email(email.to, verify=True) is None:
        # check email exist, after checking for validation, as it takes longer
        sys.stdout.write(f'WARN:\tEmail {email.to} does not exist!\n')

        raise HTTPException(
            status_code=400,
            detail=f"Email {email.to} does not exist!",
        )

    # Send message
    sys.stdout.write(f'INFO:\tSend message to {email.to} with subject: "{email.subject}"\n')
    result = send_email(email.to, email.subject, email.message)

    if result:
        return {"result": result, "message": "Email send successfully!"}

    else:
        raise HTTPException(
            status_code=404,
            detail="Something went wrong",
        )

