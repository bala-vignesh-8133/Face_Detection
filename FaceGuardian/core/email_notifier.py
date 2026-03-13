import smtplib
import threading
import time
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import json

class EmailNotifier:
    """
    Background email notification system for unauthorized person alerts.
    Uses threading to prevent blocking the monitoring system.
    """
    
    def __init__(self, config_file="email_config.json"):
        self.config_file = config_file
        self.load_config()
        self.last_email_time = 0
        self.cooldown = 60  # 60 seconds between emails
        self.email_queue = []
        self.is_sending = False
        
    def load_config(self):
        """Load email configuration from JSON file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.sender_email = config.get('sender_email', '')
                # Remove spaces from app password (Gmail app passwords have spaces but SMTP needs them removed)
                self.sender_password = config.get('sender_password', '').replace(' ', '')
                self.receiver_email = config.get('receiver_email', '')
                self.smtp_server = config.get('smtp_server', 'smtp.gmail.com')
                self.smtp_port = config.get('smtp_port', 587)
                print(f"[EMAIL] Config loaded: {self.sender_email} -> {self.receiver_email}")
        else:
            # Default values
            self.sender_email = ''
            self.sender_password = ''
            self.receiver_email = ''
            self.smtp_server = 'smtp.gmail.com'
            self.smtp_port = 587
            
    def save_config(self, sender_email, sender_password, receiver_email):
        """Save email configuration to JSON file"""
        config = {
            'sender_email': sender_email,
            'sender_password': sender_password,
            'receiver_email': receiver_email,
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
        self.load_config()
        
    def can_send_email(self):
        """Check if cooldown period has passed"""
        current_time = time.time()
        if current_time - self.last_email_time > self.cooldown:
            return True
        return False
    
    def send_alert(self, image_path, person_name="Unknown"):
        """
        Send email alert in background thread (non-blocking).
        
        Args:
            image_path: Path to captured image
            person_name: Name of detected person
        """
        if not self.can_send_email():
            print(f"[EMAIL] Cooldown active. Skipping email.")
            return
            
        if not self.sender_email or not self.receiver_email:
            print("[EMAIL] Email not configured. Skipping.")
            return
        
        # Start background thread for email sending
        email_thread = threading.Thread(
            target=self._send_email_background,
            args=(image_path, person_name),
            daemon=True
        )
        email_thread.start()
        self.last_email_time = time.time()
        print(f"[EMAIL] Alert queued for background sending...")
        
    def _send_email_background(self, image_path, person_name):
        """
        Background thread function to send email.
        This runs asynchronously and doesn't block the main monitoring loop.
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if person_name and person_name != "Unknown":
                msg['Subject'] = f"🚨 URGENT: Missing Child Sighting - {person_name} 🚨"
                body = f"""
MISSING CHILD DETECTION SYSTEM ALERT

⚠️ POSSIBLE MATCH FOUND ⚠️

Detection Details:
- Time: {timestamp}
- Identity: {person_name}
- Location: Camera 0 (Main Entrance)
- Status: Confirmed Neural Match

Action Required:
Please review the attached image immediately and contact the authorities.

---
This is an automated alert from FaceGuardian Missing Child System.
Do not reply to this email.
                """
            else:
                msg['Subject'] = "🚨 ALERT: System Activity Detected"
                body = f"""
MISSING CHILD DETECTION SYSTEM ALERT

System Activity Details:
- Time: {timestamp}
- Location: Camera 0
- Status: System Activity Logged

---
This is an automated alert from FaceGuardian Missing Child System.
Do not reply to this email.
                """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach image
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data, name=os.path.basename(image_path))
                    msg.attach(image)
            
            # Send email via SMTP
            print(f"[EMAIL] Connecting to {self.smtp_server}:{self.smtp_port}...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                server.set_debuglevel(0)  # Set to 1 for verbose debugging
                print(f"[EMAIL] Starting TLS...")
                server.starttls()  # Secure connection
                print(f"[EMAIL] Logging in as {self.sender_email}...")
                server.login(self.sender_email, self.sender_password)
                print(f"[EMAIL] Sending message...")
                server.send_message(msg)
                
            print(f"[EMAIL] ✅ Alert sent successfully to {self.receiver_email}")
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"[EMAIL] ❌ Authentication failed: {e}")
            print(f"[EMAIL] Email: {self.sender_email}")
            print(f"[EMAIL] Password length: {len(self.sender_password)} chars")
            print(f"[EMAIL] Hint: Make sure you're using Gmail App Password, not regular password")
        except smtplib.SMTPException as e:
            print(f"[EMAIL] ❌ SMTP error: {e}")
        except Exception as e:
            print(f"[EMAIL] ❌ Failed to send email: {type(e).__name__}: {e}")
