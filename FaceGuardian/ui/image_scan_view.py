
import cv2
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QFileDialog, QScrollArea, QSizePolicy
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QSize
from ui.styles import Theme
from core.translator import Translator as T

class ImageScanView(QWidget):
    """
    View for scanning static images.
    Upload a photo -> AI detects & identifies faces -> Display results.
    """
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        self.header = QLabel(T.tr("Verification Scanner"))
        self.header.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Theme.TEXT_MAIN};")
        layout.addWidget(self.header)
        
        # Action Bar
        actions = QHBoxLayout()
        self.upload_btn = QPushButton(T.tr("UPLOAD PHOTO"))
        self.upload_btn.setObjectName("PrimaryButton")
        self.upload_btn.setFixedHeight(45)
        self.upload_btn.setFixedWidth(200)
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_btn.clicked.connect(self.select_image)
        actions.addWidget(self.upload_btn)
        actions.addStretch()
        layout.addLayout(actions)
        
        # Display Area
        self.display_frame = QFrame()
        self.display_frame.setStyleSheet(f"background-color: black; border: 2px solid {Theme.BORDER}; border-radius: 8px;")
        df_layout = QVBoxLayout(self.display_frame)
        df_layout.setContentsMargins(10, 10, 10, 10)
        
        self.image_label = QLabel("No Image Selected")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-size: 18px;")
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        df_layout.addWidget(self.image_label)
        
        layout.addWidget(self.display_frame, stretch=1)
        
        # Results / Info
        self.results_label = QLabel("Ready for analysis...")
        self.results_label.setStyleSheet(f"color: {Theme.ACCENT}; font-weight: bold;")
        layout.addWidget(self.results_label)

    def retranslate_ui(self):
        self.header.setText(T.tr("Verification Scanner"))
        self.upload_btn.setText(T.tr("UPLOAD PHOTO"))

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.process_image(file_path)

    def process_image(self, path):
        # 1. Load Image
        image = cv2.imread(path)
        if image is None:
            self.results_label.setText("Error: Could not load image.")
            return
            
        # 2. Run AI
        faces = self.engine.detect_faces(image)
        results_text = []
        
        if faces is not None:
            for face in faces:
                x, y, w, h = map(int, face[:4])
                name, confidence = self.engine.recognize(image, face)
                is_match = name != "Unknown"
                
                color = (0, 0, 255) if is_match else (0, 255, 0)
                # Draw Box
                cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
                # Draw Label
                lbl = f"MATCH: {name} ({int(confidence*100)}%)" if is_match else "Unknown"
                cv2.putText(image, lbl, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
                if is_match:
                    results_text.append(f"MATCH: {name} [{int(confidence*100)}%]")
        
        # 3. Display Result
        self.display_processed(image)
        
        if results_text:
            self.results_label.setText(f"Analysis Complete: Found {len(results_text)} missing child match(es) -> " + ", ".join(results_text))
            self.results_label.setStyleSheet(f"color: {Theme.DANGER}; font-weight: bold;")
            
            # --- Auto Email Trigger (Confidence > 50%) ---
            highest_conf_name = None
            max_conf = 0
            for text in results_text:
                # text format: "MATCH: Name [XX%]"
                try:
                    conf_val = int(text.split("[")[1].split("%")[0])
                    name_val = text.split("MATCH: ")[1].split(" [")[0]
                    if conf_val > max_conf:
                        max_conf = conf_val
                        highest_conf_name = name_val
                except: pass
                
            if max_conf > 50:
                print(f"[VERIFIER] Confidence {max_conf}% > 50%. Triggering Auto-Email...")
                try:
                    # Save a temp image for the email attachment
                    temp_path = "temp_scan_alert.jpg"
                    cv2.imwrite(temp_path, image)
                    
                    from core.email_notifier import EmailNotifier
                    notifier = EmailNotifier()
                    notifier.send_alert(temp_path, highest_conf_name)
                except Exception as e:
                    print(f"[VERIFIER] Failed to send auto-email: {e}")
            
        else:
            self.results_label.setText("Analysis Complete: No missing child records match.")
            self.results_label.setStyleSheet(f"color: {Theme.ACCENT}; font-weight: bold;")

    def display_processed(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        pixmap = QPixmap.fromImage(qt_image)
        target_size = self.image_label.parent().size() - QSize(20, 20)
        
        self.image_label.setPixmap(pixmap.scaled(
            target_size, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        ))
        self.image_label.setText("") # Clear placeholder text
