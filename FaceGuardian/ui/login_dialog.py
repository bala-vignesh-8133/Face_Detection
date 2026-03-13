from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFrame, QGraphicsDropShadowEffect, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


# ===== Custom Dark Message Box =====
class DarkMessageBox(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setStyleSheet("""
            background-color: #11121a;
            color: #ff4d4d;
            border: 2px solid #ff4d4d;
            border-radius: 12px;
        """)
        self.setFixedSize(300, 120)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        msg_label = QLabel(message)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setStyleSheet("font-size: 13px; font-weight: 700;")
        layout.addWidget(msg_label)

        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(30)
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4d4d;
                color: #ffffff;
                border-radius: 6px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn, alignment=Qt.AlignmentFlag.AlignCenter)


# ===== Login Dialog =====
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Secure Access Terminal")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()
        self.setStyleSheet("background-color: #05070d;")
        
        self.role = None  # To store the authenticated role
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== Glass Card =====
        self.card = QFrame()
        self.card.setFixedSize(460, 580)
        self.card.setObjectName("LoginCard")
        self.card.setStyleSheet("""
            QFrame#LoginCard {
                background: rgba(18, 22, 35, 0.96);
                border: 1px solid #00f6ff;
                border-radius: 18px;
            }
        """)

        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(45)
        glow.setXOffset(0)
        glow.setYOffset(0)
        glow.setColor(QColor(0, 246, 255, 140))
        self.card.setGraphicsEffect(glow)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(18)

        # ===== Premium Logo Badge (Plain) =====
        logo_label = QLabel("🛡️")  # plain shield
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("""
            QLabel {
                font-size: 56px;
                color: #00f6ff;
                background: transparent;
            }
        """)

        logo_glow = QGraphicsDropShadowEffect()
        logo_glow.setBlurRadius(30)
        logo_glow.setXOffset(0)
        logo_glow.setYOffset(0)
        logo_glow.setColor(QColor(0, 246, 255, 180))
        logo_label.setGraphicsEffect(logo_glow)

        layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # ===== Title Badge =====
        title = QLabel("Missing Child Detection System")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 rgba(0, 246, 255, 0.08),
                                            stop:0.5 rgba(0, 246, 255, 0.18),
                                            stop:1 rgba(0, 246, 255, 0.08));
                border: 1px solid rgba(0, 246, 255, 0.7);
                border-radius: 8px;
                padding: 12px 18px;
                color: #eaffff;
                font-size: 18px;
                font-weight: 800;
                letter-spacing: 2px;
            }
        """)

        title_glow = QGraphicsDropShadowEffect()
        title_glow.setBlurRadius(25)
        title_glow.setXOffset(0)
        title_glow.setYOffset(0)
        title_glow.setColor(QColor(0, 246, 255, 160))
        title.setGraphicsEffect(title_glow)

        layout.addWidget(title)

        # ===== Subtitle =====
        subtitle = QLabel("AUTHORIZED PERSONNEL ONLY")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                background: rgba(255, 0, 0, 0.08);
                border: 1px solid rgba(255, 60, 60, 0.6);
                border-radius: 6px;
                padding: 6px 14px;
                color: #ff4d4d;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1.5px;
            }
        """)
        layout.addWidget(subtitle)

        layout.addSpacing(25)

        # ===== Role Selection =====
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Volunteer", "Police Officer", "Government Admin"])
        self.role_combo.setFixedHeight(46)
        self.role_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(10, 14, 25, 0.85);
                border: 1px solid #1f3b4d;
                border-radius: 12px;
                padding-left: 14px;
                font-size: 13px;
                color: #e5f9ff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #0a0e19;
                color: #e5f9ff;
                selection-background-color: rgba(0, 246, 255, 0.2);
                selection-color: #00f6ff;
                border: 1px solid #1f3b4d;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                min-height: 35px;
                padding-left: 10px;
            }
        """)
        layout.addWidget(self.role_combo)

        # ===== Username =====
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Agent/User ID")
        self.user_input.setFixedHeight(46)
        self.user_input.setStyleSheet(self.input_style())
        layout.addWidget(self.user_input)

        # ===== Password =====
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Access Key")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setFixedHeight(46)
        self.pass_input.setStyleSheet(self.input_style())
        self.pass_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.pass_input)

        layout.addSpacing(30)

        # ===== Login Button =====
        self.login_btn = QPushButton("AUTHENTICATE")
        self.login_btn.setFixedHeight(48)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #00f6ff;
                color: #00f6ff;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 1.5px;
            }
            QPushButton:hover {
                background-color: rgba(0, 246, 255, 0.12);
            }
            QPushButton:pressed {
                background-color: rgba(0, 246, 255, 0.22);
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)

        # ===== Exit =====
        exit_btn = QPushButton("EXIT SYSTEM")
        exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        exit_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #7aa7b3;
                font-size: 11px;
                letter-spacing: 1.2px;
            }
            QPushButton:hover {
                color: #ffffff;
            }
        """)
        exit_btn.clicked.connect(self.reject)
        layout.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(self.card)

    def input_style(self):
        return """
            QLineEdit {
                background-color: rgba(10, 14, 25, 0.85);
                border: 1px solid #1f3b4d;
                border-radius: 12px;
                padding-left: 14px;
                font-size: 13px;
                color: #e5f9ff;
            }
            QLineEdit:focus {
                border: 1px solid #00f6ff;
                background-color: rgba(10, 14, 25, 1);
            }
            QLineEdit::placeholder {
                color: #6b9aaa;
            }
        """

    def handle_login(self):
        user = self.user_input.text()
        pwd = self.pass_input.text()
        selected_role = self.role_combo.currentText()

        # Simple Hardcoded RBAC Authentication
        authenticated = False
        
        if selected_role == "Volunteer" and user == "volunteer" and pwd == "volunteer":
            self.role = "Volunteer"
            authenticated = True
        elif selected_role == "Police Officer" and user == "police" and pwd == "police":
            self.role = "Police"
            authenticated = True
        elif selected_role == "Government Admin" and (user == "gov" or user == "admin") and (pwd == "gov" or pwd == "admin"):
            self.role = "Government"
            authenticated = True

        if authenticated:
            self.accept()
        else:
            dlg = DarkMessageBox("ACCESS DENIED", "Invalid credentials for selected role.", self)
            dlg.exec()
