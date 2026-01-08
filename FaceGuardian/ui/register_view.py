import cv2
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame, QMessageBox, QCheckBox, QSizePolicy, QComboBox
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from ui.styles import Theme
from core.employee_manager import EmployeeManager

class RegisterView(QWidget):
    """
    Admin View: Add New Employee.
    Captures face + Metadata (ID, Role, Dept).
    """
    user_registered = pyqtSignal()
    render_finished = pyqtSignal()

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.emp_manager = EmployeeManager()
        self.current_frame = None
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
        
        header = QLabel("Add New Employee")
        header.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Theme.TEXT_MAIN};")
        f_layout.addWidget(header)
        
        sub = QLabel("Register authorized personnel with full credentials.")
        sub.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-size: 14px;")
        sub.setWordWrap(True)
        f_layout.addWidget(sub)
        
        f_layout.addSpacing(20)
        
        # Fields
        f_layout.addWidget(self.create_label("EMPLOYEE ID"))
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("e.g. EMP-2024-001")
        f_layout.addWidget(self.id_input)
        
        f_layout.addWidget(self.create_label("FULL NAME"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Sarah Connor")
        f_layout.addWidget(self.name_input)
        
        f_layout.addWidget(self.create_label("ROLE / DESIGNATION"))
        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("e.g. Security Chief")
        f_layout.addWidget(self.role_input)
        
        f_layout.addWidget(self.create_label("DEPARTMENT"))
        self.dept_input = QComboBox()
        self.dept_input.addItems(["Security", "IT", "HR", "Management", "Operations", "Other"])
        self.dept_input.setStyleSheet(Theme.GLOBAL_STYLES)
        f_layout.addWidget(self.dept_input)
        
        f_layout.addSpacing(10)
        
        self.append_check = QCheckBox("Merge into existing profile (New Angle)")
        self.append_check.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-size: 13px;")
        f_layout.addWidget(self.append_check)
        
        f_layout.addSpacing(20)
        
        self.capture_btn = QPushButton("REGISTER EMPLOYEE")
        self.capture_btn.setObjectName("PrimaryButton")
        self.capture_btn.setFixedHeight(50)
        self.capture_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.capture_btn.clicked.connect(self.handle_registration)
        f_layout.addWidget(self.capture_btn)
        
        f_layout.addStretch()
        
        # Right: Camera Preview
        preview_container = QFrame()
        preview_container.setStyleSheet(f"background-color: black; border: 2px solid {Theme.BORDER}; border-radius: 8px;")
        p_layout = QVBoxLayout(preview_container)
        p_layout.setContentsMargins(2,2,2,2)
        
        self.preview_label = QLabel("Waiting for Secure Stream...")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("color: #64748b;")
        self.preview_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        p_layout.addWidget(self.preview_label)
        
        # Instructions Overlay
        instr = QLabel("TIP: Ensure face is clearly visible without mask/glasses.")
        instr.setStyleSheet(f"color: {Theme.ACCENT}; font-weight: bold; padding: 10px;")
        instr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        p_layout.addWidget(instr)
        
        layout.addWidget(form_container)
        layout.addWidget(preview_container, stretch=1)

    def create_label(self, text):
        return QLabel(text, styleSheet=f"color: {Theme.PRIMARY}; font-weight: bold; font-size: 11px; margin-top: 5px;")

    @pyqtSlot(np.ndarray, list)
    def update_preview(self, frame, results):
        try:
            self.current_frame = frame.copy()
            
            # Draw Face Box for Feedback
            for res in results:
                x, y, w, h = res['rect']
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            
            # Convert for preview
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            
            # Resize logic (Safe)
            target_size = self.preview_label.size()
            if target_size.width() < 100: target_size = QSize(400, 300)

            self.preview_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
                target_size, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.FastTransformation
            ))
        finally:
            self.render_finished.emit()

    def handle_registration(self):
        # Validate Inputs
        emp_id = self.id_input.text().strip()
        name = self.name_input.text().strip()
        role = self.role_input.text().strip()
        dept = self.dept_input.currentText()
        
        if not name or not emp_id or not role:
            QMessageBox.warning(self, "Validation Error", "All fields (ID, Name, Role) are required.")
            return
            
        if self.current_frame is None:
            QMessageBox.warning(self, "Hardware Error", "Webcam stream is not ready.")
            return

        is_append = self.append_check.isChecked()
        
        # AI Registration
        success = self.engine.register_new_face(name, self.current_frame, append=is_append)
        
        if success:
            # Save Metadata
            self.emp_manager.add_employee(name, emp_id, role, dept)
            
            mode = "Enhanced" if is_append else "Created"
            QMessageBox.information(self, "Success", f"Employee '{name}' (ID: {emp_id}) registered successfully.")
            
            # Clear fields
            self.id_input.clear()
            self.name_input.clear()
            self.role_input.clear()
            self.append_check.setChecked(False)
            
            self.user_registered.emit()
        else:
            QMessageBox.warning(self, "AI Error", "No clear face detected in the frame.")
