import cv2
import numpy as np
import os
import time
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QGridLayout, QSizePolicy
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal, QDateTime, QSize
from ui.styles import Theme
import qtawesome as qta
from core.email_notifier import EmailNotifier

class MonitorView(QWidget):
    # Signal to tell camera thread we are ready for next frame
    render_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.backend_status = "Initializing..."
        self.last_capture_time = 0
        self.alerts_dir = "alerts"
        if not os.path.exists(self.alerts_dir):
            os.makedirs(self.alerts_dir)
        
        # Initialize email notifier
        self.email_notifier = EmailNotifier()
            
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 1. Left: Video Feed
        video_wrapper = QFrame()
        video_wrapper.setStyleSheet(f"background-color: black; border: 2px solid {Theme.BORDER}; border-radius: 8px;")
        vw_layout = QVBoxLayout(video_wrapper)
        vw_layout.setContentsMargins(2, 2, 2, 2)
        
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("background-color: #000;")
        # CRITICAL FIX: Prevent label from pushing the layout size
        self.video_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        vw_layout.addWidget(self.video_label)
        
        layout.addWidget(video_wrapper, stretch=3)
        
        # 2. Right: Info Panel
        self.info_panel = QFrame()
        self.info_panel.setFixedWidth(320)
        self.info_panel.setObjectName("Card")
        ip_layout = QVBoxLayout(self.info_panel)
        ip_layout.setContentsMargins(20, 20, 20, 20)
        ip_layout.setSpacing(15)
        
        # Header
        header = QLabel("TARGET ANALYSIS")
        header.setStyleSheet(f"color: {Theme.PRIMARY}; font-weight: 900; letter-spacing: 2px; font-size: 14px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ip_layout.addWidget(header)
        
        # Profile Image Placeholder
        self.profile_img = QLabel()
        self.profile_img.setFixedSize(120, 120)
        self.profile_img.setStyleSheet(f"background-color: {Theme.SURFACE_HOVER}; border-radius: 60px; border: 2px dashed {Theme.BORDER};")
        self.profile_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        img_container = QHBoxLayout()
        img_container.addStretch()
        img_container.addWidget(self.profile_img)
        img_container.addStretch()
        ip_layout.addLayout(img_container)
        
        ip_layout.addSpacing(10)
        
        # Data Fields
        self.lbl_status = self.create_info_row(ip_layout, "STATUS", "SCANNING...", Theme.TEXT_SUB)
        self.lbl_camera = self.create_info_row(ip_layout, "SOURCE", "CAM 0", Theme.PRIMARY)
        self.lbl_name = self.create_info_row(ip_layout, "IDENTITY", "---", Theme.TEXT_MAIN)
        self.lbl_conf = self.create_info_row(ip_layout, "CONFIDENCE", "0%", Theme.TEXT_MAIN)
        self.lbl_time = self.create_info_row(ip_layout, "LAST SEEN", "---", Theme.TEXT_SUB)
        
        ip_layout.addStretch()
        
        # Manual Override Button
        btn_lock = QLabel("🔒 SECURITY LOCK ACTIVE")
        btn_lock.setStyleSheet(f"background-color: {Theme.SURFACE_HOVER}; color: {Theme.ACCENT}; padding: 10px; border-radius: 4px; font-weight: bold;")
        btn_lock.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ip_layout.addWidget(btn_lock)

        layout.addWidget(self.info_panel)

    def create_info_row(self, layout, label, value, color):
        container = QFrame()
        l = QVBoxLayout(container)
        l.setContentsMargins(0,0,0,0)
        l.setSpacing(2)
        
        lbl_title = QLabel(label)
        lbl_title.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-size: 10px; font-weight: bold;")
        
        lbl_val = QLabel(value)
        lbl_val.setStyleSheet(f"color: {color}; font-size: 16px; font-weight: 800;")
        
        l.addWidget(lbl_title)
        l.addWidget(lbl_val)
        
        layout.addWidget(container)
        return lbl_val

    def set_backend_status(self, status):
        self.backend_status = status

    @pyqtSlot(np.ndarray, list)
    def update_frame(self, frame, results):
        try:
            detected_target = False
            
            # Draw Hardware Status Overlay
            cv2.putText(frame, f"HARDWARE: {self.backend_status}", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, "MODE: LOW LATENCY", (20, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # Draw bounding boxes on frame
            for result in results:
                x, y, w, h = result['rect']
                name = result['name']
                distance = result['distance']
                authorized = result['authorized']
                
                if authorized:
                    color = (0, 255, 0)  # Green for authorized
                    display_label = f"{name} [{int(distance*100)}%]"
                    status_text = "AUTHORIZED"
                    status_color = Theme.ACCENT
                else:
                    color = (0, 0, 255)  # Red for unauthorized
                    display_label = f"{name}"
                    status_text = "UNAUTHORIZED"
                    status_color = Theme.DANGER
                
                detected_target = True

                # Draw sleek corner brackets (Cyber Style)
                length = int(w * 0.25)
                thickness = 2
                
                # Top Left
                cv2.line(frame, (x, y), (x + length, y), color, thickness)
                cv2.line(frame, (x, y), (x, y + length), color, thickness)
                
                # Top Right
                cv2.line(frame, (x + w, y), (x + w - length, y), color, thickness)
                cv2.line(frame, (x + w, y), (x + w, y + length), color, thickness)
                
                # Bottom Left
                cv2.line(frame, (x, y + h), (x + length, y + h), color, thickness)
                cv2.line(frame, (x, y + h), (x, y + h - length), color, thickness)
                
                # Bottom Right
                cv2.line(frame, (x + w, y + h), (x + w - length, y + h), color, thickness)
                cv2.line(frame, (x + w, y + h), (x + w, y + h - length), color, thickness)

                # Floating Label
                label = display_label
                
                # Label Background
                cv2.rectangle(frame, (x, y - 25), (x + int(w*0.8), y-5), color, cv2.FILLED)
                cv2.putText(frame, label, (x + 5, y - 12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1, cv2.LINE_AA)
                
                # Update info panel
                self.update_panel(name, distance, status_text, status_color)
                
                # Capture unauthorized faces with 60-second cooldown
                if not authorized:
                    current_time = time.time()
                    if current_time - self.last_capture_time > 60:  # 1 minute cooldown
                        self.capture_intruder(frame.copy(), x, y, w, h, name)
                        self.last_capture_time = current_time
            
            if not detected_target:
                self.lbl_status.setText("SCANNING...")
                self.lbl_status.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-size: 16px; font-weight: 800;")
                self.lbl_name.setText("---")

            # Convert to QImage
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            
            # Resize logic (Safe)
            target_size = self.video_label.parent().size()
            if target_size.width() < 10 or target_size.height() < 10:
                target_size = QSize(640, 480)

            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(
                target_size, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.FastTransformation
            )
            self.video_label.setPixmap(scaled_pixmap)
        finally:
            self.render_finished.emit()

    def update_panel(self, name, conf, status_text, status_color):
        """Update info panel with identity information"""
        self.lbl_name.setText(name)
        self.lbl_conf.setText(f"{int(conf*100)}%")
        self.lbl_time.setText(QDateTime.currentDateTime().toString("HH:mm:ss"))
        self.lbl_status.setText(status_text)
        self.lbl_status.setStyleSheet(f"color: {status_color}; font-size: 16px; font-weight: 800;")

    @pyqtSlot(str)
    def update_camera_info(self, name):
        self.lbl_camera.setText(name.upper())

    def capture_intruder(self, frame, x, y, w, h, name):
        """Capture unauthorized person with red bounding box drawn on image"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"intruder_{timestamp}.jpg"
        filepath = os.path.join(self.alerts_dir, filename)
        
        # Draw RED bounding box on the frame
        color = (0, 0, 255)  # Red in BGR
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
        
        # Draw label with name
        label = f"UNAUTHORIZED: {name}"
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        cv2.rectangle(frame, (x, y-30), (x + label_size[0] + 10, y), color, -1)
        cv2.putText(frame, label, (x + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Save frame with bounding box
        cv2.imwrite(filepath, frame)
        print(f"[ALERT] Intruder Captured! Saved to {filepath}")
        
        # Send email alert in background (non-blocking)
        self.email_notifier.send_alert(filepath, name)
