
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from ui.styles import Theme

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Secure Admin Access")
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.init_ui()
        
    def init_ui(self):
        # Translucent background handling
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Main Card
        self.card = QFrame()
        self.card.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.SURFACE};
                border: 1px solid {Theme.BORDER};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Logo
        logo = QLabel("🛡️")
        logo.setStyleSheet("font-size: 64px; border: none; background: transparent;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)
        
        title = QLabel("ADMIN ACCESS")
        title.setStyleSheet(f"font-size: 24px; font-weight: 900; color: {Theme.TEXT_MAIN}; letter-spacing: 2px; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        status = QLabel("Restricted Area. Authorized Personnel Only.")
        status.setStyleSheet(f"color: {Theme.DANGER}; font-weight: bold; font-size: 11px; border: none;")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(status)
        
        layout.addSpacing(20)
        
        # Inputs
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Admin Username")
        self.user_input.setStyleSheet(Theme.GLOBAL_STYLES) # Re-apply input style
        layout.addWidget(self.user_input)
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.pass_input)
        
        layout.addSpacing(20)
        
        # Buttons
        self.login_btn = QPushButton("AUTHENTICATE")
        self.login_btn.setObjectName("PrimaryButton")
        self.login_btn.setFixedHeight(45)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.PRIMARY};
                color: white;
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background-color: {Theme.SECONDARY};
            }}
        """)
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)
        
        exit_btn = QPushButton("EXIT SYSTEM")
        exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        exit_btn.setStyleSheet(f"color: {Theme.TEXT_SUB}; background: transparent; border: none; font-weight: bold;")
        exit_btn.clicked.connect(self.reject)
        layout.addWidget(exit_btn)
        
        main_layout.addWidget(self.card)

    def handle_login(self):
        user = self.user_input.text()
        pwd = self.pass_input.text()
        
        # Hardcoded for now, can be moved to config later
        if user == "admin" and pwd == "admin":
            self.accept()
        else:
            QMessageBox.warning(self, "Access Denied", "Invalid Credentials.\nSecurity event has been logged.")
            self.pass_input.clear()
