import smtplib
import json
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import cv2

class AlertManager:
    """
    Handles sending email alerts with robust SMTP handling (SSL/TLS support).
    """
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.last_alert_time = 0
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}

    def send_alert(self, frame):
        self.load_config()
        
        if not self.config.get("alerts_enabled", False):
            return

        current_time = time.time()
        cooldown_seconds = self.config.get("alert_cooldown_minutes", 5) * 60
        
        if current_time - self.last_alert_time < cooldown_seconds:
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.get("sender_email")
            msg['To'] = self.config.get("recipient_email")
            msg['Subject'] = "🔒 SECURITY ALERT: Unauthorized Person Detected"

            body = "FaceGuardian detected an unidentified person. See attachment."
            msg.attach(MIMEText(body, 'plain'))

            _, buffer = cv2.imencode('.jpg', frame)
            image = MIMEImage(buffer.tobytes(), name="detection.jpg")
            msg.attach(image)

            # Try Port 465 (SSL) first as it's more direct
            try:
                server = smtplib.SMTP_SSL(self.config.get("smtp_server"), 465, timeout=10)
                server.login(self.config.get("sender_email"), self.config.get("sender_password"))
                server.send_message(msg)
                server.quit()
            except:
                # Fallback to Port 587 (STARTTLS)
                server = smtplib.SMTP(self.config.get("smtp_server"), 587, timeout=10)
                server.starttls()
                server.login(self.config.get("sender_email"), self.config.get("sender_password"))
                server.send_message(msg)
                server.quit()

            self.last_alert_time = current_time
            print(f"✅ Security alert sent to {self.config.get('recipient_email')}")
            
        except Exception as e:
            print(f"❌ Email Alert Failed: {e}")
