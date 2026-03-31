import cv2
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame, QMessageBox, QCheckBox, QSizePolicy, QComboBox, QFileDialog
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from ui.styles import Theme
from core.child_manager import ChildManager
from core.translator import Translator as T

class RegisterView(QWidget):
    """
    Reporting View: Add Missing Child Report.
    Captures face + Metadata (Age, Contact, Location).
    """
    user_registered = pyqtSignal()
    render_finished = pyqtSignal()

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.child_manager = ChildManager()
        self.current_frame = None
        self.image_path = None
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(40)
        
        # Left: Form
        form_container = QFrame()
        form_container.setFixedWidth(400)
        f_layout = QVBoxLayout(form_container)
        f_layout.setContentsMargins(0,0,0,0)
        f_layout.setSpacing(15)
        
        header = QLabel(T.tr("Report Missing Child"))
        header.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Theme.TEXT_MAIN};")
        f_layout.addWidget(header)
        
        sub = QLabel("Register a missing child with a photo and details.")
        sub.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-size: 14px;")
        sub.setWordWrap(True)
        f_layout.addWidget(sub)
        
        f_layout.addSpacing(20)
        
        # Fields
        f_layout.addWidget(self.create_label(T.tr("CHILD's FULL NAME")))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. John Doe")
        f_layout.addWidget(self.name_input)
        
        f_layout.addWidget(self.create_label(T.tr("AGE (approximate)")))
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("e.g. 5")
        f_layout.addWidget(self.age_input)
        
        f_layout.addWidget(self.create_label(T.tr("LAST SEEN LOCATION")))
        self.last_seen_input = QLineEdit()
        self.last_seen_input.setPlaceholderText("e.g. Central Park, NY")
        f_layout.addWidget(self.last_seen_input)
        
        f_layout.addWidget(self.create_label(T.tr("DATE MISSING")))
        self.date_missing_input = QLineEdit()
        self.date_missing_input.setPlaceholderText("e.g. 2026-03-12")
        f_layout.addWidget(self.date_missing_input)

        f_layout.addWidget(self.create_label(T.tr("AADHAR NUMBER")))
        self.aadhar_input = QLineEdit()
        self.aadhar_input.setPlaceholderText("e.g. 1234 5678 9012")
        f_layout.addWidget(self.aadhar_input)

        f_layout.addWidget(self.create_label(T.tr("GUARDIAN CONTACT")))
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("e.g. +1 555-0199")
        f_layout.addWidget(self.contact_input)
        
        f_layout.addSpacing(10)
        
        self.append_check = QCheckBox(T.tr("Merge into existing profile (New Angle)"))
        self.append_check.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-size: 13px;")
        f_layout.addWidget(self.append_check)
        
        f_layout.addSpacing(20)
        
        self.capture_btn = QPushButton(T.tr("REGISTER REPORT"))
        self.capture_btn.setObjectName("PrimaryButton")
        self.capture_btn.setFixedHeight(50)
        self.capture_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.capture_btn.clicked.connect(self.handle_registration)
        f_layout.addWidget(self.capture_btn)
        
        f_layout.addStretch()
        
        # Right: Image Preview & Upload
        preview_container = QFrame()
        preview_container.setStyleSheet(f"background-color: black; border: 2px solid {Theme.BORDER}; border-radius: 8px;")
        p_layout = QVBoxLayout(preview_container)
        p_layout.setContentsMargins(10,10,10,10)
        
        self.preview_label = QLabel("No Photo Selected")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("color: #64748b; font-size: 16px;")
        self.preview_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        p_layout.addWidget(self.preview_label, stretch=1)
        
        self.upload_btn = QPushButton(T.tr("Select Photo"))
        self.upload_btn.setObjectName("SecondaryButton")
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_btn.clicked.connect(self.select_image)
        p_layout.addWidget(self.upload_btn)
        
        # Instructions Overlay
        instr = QLabel("TIP: Ensure face is clearly visible without mask/glasses.")
        instr.setStyleSheet(f"color: {Theme.ACCENT}; font-weight: bold; padding: 10px;")
        instr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        p_layout.addWidget(instr)
        
        layout.addWidget(form_container)
        layout.addWidget(preview_container, stretch=1)

    def retranslate_ui(self):
        # This is a bit tricky for dynamically created labels, but let's update common once
        self.capture_btn.setText(T.tr("REGISTER REPORT"))
        self.upload_btn.setText(T.tr("Select Photo"))
        self.append_check.setText(T.tr("Merge into existing profile (New Angle)"))
        # Re-creating form with current logic is better but for now we'll just do this
        # In a real app we'd store refs to all labels.

    def create_label(self, text):
        return QLabel(text, styleSheet=f"color: {Theme.PRIMARY}; font-weight: bold; font-size: 11px; margin-top: 5px;")

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.image_path = file_path
            self.current_frame = cv2.imread(file_path)
            
            # Display image
            pixmap = QPixmap(file_path)
            target_size = self.preview_label.size()
            if target_size.width() < 100: target_size = QSize(400, 300)
            
            self.preview_label.setPixmap(pixmap.scaled(
                target_size, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            ))

    def handle_registration(self):
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()
        last_seen = self.last_seen_input.text().strip()
        date_missing = self.date_missing_input.text().strip()
        contact = self.contact_input.text().strip()
        aadhar = self.aadhar_input.text().strip()
        
        if not name or not age or not contact or not aadhar:
            QMessageBox.warning(self, "Validation Error", "Name, Age, Contact, and Aadhar Number are required.")
            return
            
        if self.current_frame is None:
            QMessageBox.warning(self, "Validation Error", "Please upload a photo of the child.")
            return

        is_append = self.append_check.isChecked()
        role = self.window().role 

        # We need to tell the engine if it should cache this face in RAM immediately
        # Volunteers cannot make faces instantly active on cameras; they require Police approval.
        is_active = role in ["Police", "Government"]
        
        # AI Registration
        success = self.engine.register_new_face(name, self.current_frame, append=is_append, activate=is_active)
        
        if success:
            # Save Metadata
            status = "Active" if is_active else "Pending Approval"
            self.child_manager.add_child(name, age, last_seen, date_missing, contact, aadhar, status)
            
            if is_active:
                QMessageBox.information(self, "Success", f"Missing child '{name}' reported successfully. The face is now active on the network.")
            else:
                QMessageBox.information(self, "Success", f"Missing child '{name}' reported successfully. The case is now awaiting Police Approval.")
            
            # Clear fields
            self.name_input.clear()
            self.age_input.clear()
            self.last_seen_input.clear()
            self.date_missing_input.clear()
            self.contact_input.clear()
            self.aadhar_input.clear()
            self.append_check.setChecked(False)
            self.current_frame = None
            self.image_path = None
            self.preview_label.setText("No Photo Selected")
            self.preview_label.setPixmap(QPixmap())
            
            self.user_registered.emit()
        else:
            QMessageBox.warning(self, "AI Error", "No clear face detected in the frame.")
