import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

class EmailService:
    @staticmethod
    def send_invite(to_email: str, group_name: str, survey_link: str):
        """
        Sends an email invite to a participant with the survey link.
        """
        if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
            print("WARNING: SMTP credentials not set. Skipping email.")
            return False

        try:
            msg = MIMEMultipart()
            msg["From"] = settings.SMTP_USERNAME
            msg["To"] = to_email
            msg["Subject"] = f"PackVote Invite: Join '{group_name}' Trip Planning!"

            body = f"""
            <html>
            <body>
                <h2>You've been invited to plan a trip!</h2>
                <p>You have been added to the group <strong>{group_name}</strong>.</p>
                <p>Please fill out your preferences to help us decide where to go:</p>
                <p><a href="{survey_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Fill Survey</a></p>
                <p>Or click here: <a href="{survey_link}">{survey_link}</a></p>
                <br>
                <p>Cheers,<br>PackVote Team</p>
            </body>
            </html>
            """
            msg.attach(MIMEText(body, "html"))

            print(f"DEBUG: Connecting to SMTP {settings.SMTP_SERVER}:{settings.SMTP_PORT}...")
            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.set_debuglevel(1) # Enable library level debug
                server.starttls()
                print("DEBUG: SMTP StartTLS Success. Logging in...")
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                print(f"DEBUG: SMTP Login Success as {settings.SMTP_USERNAME}. Sending mail...")
                server.sendmail(settings.SMTP_USERNAME, to_email, msg.as_string())
            
            print(f"SUCCESS: Email sent to {to_email}")
            return True

        except Exception as e:
            print(f"ERROR: Failed to send email to {to_email}: {e}")
            return False
