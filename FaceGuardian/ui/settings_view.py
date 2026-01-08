
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QFrame, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from ui.styles import Theme

class SettingsView(QWidget):
    def __init__(self, camera_thread, parent=None):
        super().__init__(parent)
        self.camera_thread = camera_thread
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("System Settings")
        header.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Theme.TEXT_MAIN};")
        layout.addWidget(header)
        
        sub = QLabel("Configure hardware and security parameters.")
        sub.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-size: 14px;")
        layout.addWidget(sub)
        
        layout.addSpacing(20)
        
        # Camera Settings Card
        cam_card = QFrame()
        cam_card.setObjectName("Card")
        cc_layout = QVBoxLayout(cam_card)
        cc_layout.setContentsMargins(20, 20, 20, 20)
        cc_layout.setSpacing(15)
        
        cc_layout.addWidget(QLabel("PRIMARY CAMERA SOURCE", styleSheet=f"color: {Theme.PRIMARY}; font-weight: bold; font-size: 12px;"))
        
        self.cam_select = QComboBox()
        self.cam_select.addItems([
            "Integrated Webcam (Index 0)",
            "External USB Camera (Index 1)",
            "External USB Camera (Index 2)",
            "External USB Camera (Index 3)"
        ])
        # Set current index based on thread
        self.cam_select.setCurrentIndex(self.camera_thread.camera_index)
        cc_layout.addWidget(self.cam_select)
        
        self.current_cam_lbl = QLabel(f"Currently Active: Source #{self.camera_thread.camera_index}")
        self.current_cam_lbl.setStyleSheet(f"color: {Theme.ACCENT}; font-weight: bold; font-size: 11px;")
        cc_layout.addWidget(self.current_cam_lbl)
        
        help_text = QLabel("Note: On Windows, switching uses High-Speed DSHOW for minimum delay.")
        help_text.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-size: 11px; font-style: italic;")
        cc_layout.addWidget(help_text)
        
        layout.addWidget(cam_card)
        
        # Save Button
        self.save_btn = QPushButton("APPLY HARDWARE CHANGES")
        self.save_btn.setObjectName("PrimaryButton")
        self.save_btn.setFixedHeight(45)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.clicked.connect(self.apply_settings)
        layout.addWidget(self.save_btn)
        
        layout.addStretch()

    def apply_settings(self):
        new_index = self.cam_select.currentIndex()
        self.save_btn.setText("SWITCHING HARDWARE...")
        self.save_btn.setEnabled(False)
        
        self.camera_thread.change_camera(new_index)
        self.current_cam_lbl.setText(f"Currently Active: Source #{new_index}")
        
        # Short delay to allow hardware to init before re-enabling
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1500, lambda: self.reset_btn())

    def reset_btn(self):
        self.save_btn.setText("APPLY HARDWARE CHANGES")
        self.save_btn.setEnabled(True)
