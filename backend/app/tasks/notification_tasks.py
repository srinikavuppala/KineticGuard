import smtplib
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.tasks.celery_app import celery_app
from app.config import get_settings
import time


# Keep your old test task just in case
@celery_app.task(name="send_test_email_task")
def send_test_email_task(email_to: str):
    time.sleep(5)
    print(f"✅ Mailroom worker successfully sent email to: {email_to}")
    return f"Email sent to {email_to}"


# ==========================================
# THE REAL SOS EMAIL DISPATCHER
# ==========================================
@celery_app.task(name="process_sos_alert_task", bind=True, max_retries=3)
def process_sos_alert_task(self, alert_id: str, trigger_method: str, time_str: str = "Just now"):
    settings = get_settings()

    print(f"\n🚨 Connecting to SMTP server to send SOS for {alert_id}...")

    # 1. Create the WhatsApp Deep Link (Pre-fills the message automatically!)
    whatsapp_message = f"🚨 KINETIC GUARD SOS ALERT!\n\nTrigger Method: {trigger_method}\nTime: {time_str}\nAlert ID: {alert_id}\n\nImmediate action required!"
    encoded_message = urllib.parse.quote(whatsapp_message)
    whatsapp_link = f"https://wa.me/?text={encoded_message}"

    # 2. Create the email structure
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🚨 KINETIC GUARD SOS — {trigger_method} TRIGGERED"
    msg["From"] = settings.SMTP_USERNAME
    msg["To"] = settings.SMTP_USERNAME  # Sending to yourself for testing!

    # 3. Create the email body (HTML with WhatsApp Button)
    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ddd; border-radius: 5px; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #D32F2F; text-align: center;">⚠️ EMERGENCY ALERT ⚠️</h2>
        <p>An SOS alert has been triggered using the Kinetic Guard system.</p>

        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 15px 0;">
            <p><strong>Alert ID:</strong> {alert_id}</p>
            <p><strong>Trigger Method:</strong> {trigger_method}</p>
            <p><strong>Time:</strong> {time_str}</p>
        </div>

        <!-- THE NEW WHATSAPP BUTTON -->
        <div style="text-align: center; margin: 25px 0;">
            <a href="{whatsapp_link}" target="_blank" style="
                background-color: #25D366;
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
                display: inline-block;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">📱 Send to WhatsApp</a>
        </div>

        <p style="text-align: center; color: #555; font-size: 14px;">This is an automated emergency alert. Check the dashboard immediately.</p>
    </div>
    """

    msg.attach(MIMEText(html_content, "html"))

    # 4. Connect to Gmail and send
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USERNAME, settings.SMTP_USERNAME, msg.as_string())

        print(f"✅ SUCCESS! Email sent for Alert {alert_id}")
        return {"status": "email_sent", "alert_id": alert_id}

    except Exception as e:
        print(f"❌ FAILED to send email for Alert {alert_id}: {e}")
        return {"status": "email_failed", "error": str(e)}