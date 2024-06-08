import random
import flet as ft
from time import sleep
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib

import app.functions.verification_dialog as ver
from app.service.files.local_files_scr import enc_data


def email_code(code, email, subject):
    email_sender = enc_data['email']
    email_password = enc_data['passcode']
    email_rec = email

    body = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verification Code</title>
</head>
<body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f7f7f7; margin: 0; padding: 0;">
    <div style="background-color: #2A2A2A; color: #ffffff; max-width: 600px; margin: 40px auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
        <div style="font-size: 26px; font-weight: bold; margin-bottom: 20px; color: #00BFFF;">
            {subject}
        </div>
        <div style="font-size: 16px; line-height: 1.6; color: #E0E0E0;">
            Hello,
            <br><br>
            Please use the following code to complete your verification process:
            <br><br>
            <div style="font-size: 20px; color: #00BFFF; background-color: #1E1E1E; padding: 15px; border-radius: 8px; text-align: center; display: inline-block; margin: 20px 0;">{code}</div>
            <br>
            This code is valid for a short period for security reasons.
            <br><br>
            If you did not request this code, please disregard this email.
            <br><br>
            <span style="color: #FF4C4C; font-weight: bold;">WARNING: Do not share this code with anyone.</span>
        </div>
    </div>
</body>
</html>"""

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = email_sender
    message["To"] = email_rec
    message.attach(MIMEText(body, "html"))

    ssl_context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl_context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_rec, message.as_string())


def verify_code_email(page: ft.Page, email, subject) -> bool:
    ver_code = str(random.randint(1000, 99999))
    print(ver_code)
    # email_code(ver_code, email, subject)

    ver.verification_dialogs(page, email, ver_code)

    while ver.verified_dialog_open:
        if ver.verified_dialog_open is False:
            break
        else:
            sleep(1)

    return ver.verified
