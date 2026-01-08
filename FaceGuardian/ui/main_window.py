import cv2
import sys
import qtawesome as qta
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
    QStackedWidget, QLabel, QFrame, QDialog
)
from PyQt6.QtCore import Qt, QTimer, QSize, QDateTime
from PyQt6.QtGui import QIcon

from core.recognition import FaceRecognitionEngine
from core.camera_thread import CameraThread
from ui.monitor_view import MonitorView
from ui.register_view import RegisterView
from ui.database_view import DatabaseView
from ui.dashboard_view import DashboardView
from ui.alerts_view import AlertsView
from ui.login_dialog import LoginDialog
from ui.settings_view import SettingsView
from ui.styles import Theme

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 0. AUTHENTICATION (Strict Admin Only)
        login = LoginDialog()
        if login.exec() != QDialog.DialogCode.Accepted:
            sys.exit(0)
            
        self.setWindowTitle("FaceGuardian Pro | Admin Security Console")
        self.resize(1280, 800)
        
        # Apply Global Theme
        self.setStyleSheet(Theme.GLOBAL_STYLES)
        
        # Initialize Core Systems
        self.engine = FaceRecognitionEngine()
        self.camera_thread = CameraThread(self.engine)
        self.camera_thread.start()
        
        self.init_ui()
        
    def init_ui(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        # Main Layout: [Sidebar] [ContentArea]
        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 1. Sidebar
        self.create_sidebar()
        
        # 2. Right Side (TopBar + Stack)
        self.right_container = QWidget()
        self.right_layout = QVBoxLayout(self.right_container)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)
        
        self.create_topbar()
        
        # 3. Content Area
        self.content_area = QStackedWidget()
        self.right_layout.addWidget(self.content_area)
        
        self.main_layout.addWidget(self.right_container)
        
        # Initialize Views
        self.monitor_view = MonitorView()
        self.monitor_view.set_backend_status(self.engine.backend_name)
        
        self.register_view = RegisterView(self.engine) # Will be renamed in UI to "Add Employee"
        self.database_view = DatabaseView(self.engine) # Will be renamed in UI to "Manage Employees"
        self.dashboard_view = DashboardView(self.engine)
        self.alerts_view = AlertsView(self.engine)
        self.settings_view = SettingsView(self.camera_thread)
        
        # Add to stack 
        # 0: Dashboard (Real)
        self.content_area.addWidget(self.dashboard_view)
        # 1: Monitor
        self.content_area.addWidget(self.monitor_view)
        # 2: Add Employee
        self.content_area.addWidget(self.register_view)
        # 3: Manage Employees
        self.content_area.addWidget(self.database_view)
        # 4: Alerts (Real)
        self.content_area.addWidget(self.alerts_view)
        # 5: Settings
        self.content_area.addWidget(self.settings_view)
        
        # --- Connections ---
        self.monitor_view.render_finished.connect(self.camera_thread.set_render_finished)
        self.register_view.render_finished.connect(self.camera_thread.set_render_finished)
        self.camera_thread.camera_changed.connect(self.monitor_view.update_camera_info)
        
        self.register_view.user_registered.connect(self.database_view.refresh_list)
        self.database_view.database_changed.connect(self.engine.reload_known_faces)
        
        # Start at Dashboard
        self.switch_view(0)

    def create_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(260)
        
        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Logo Area
        logo_box = QFrame()
        logo_box.setFixedHeight(80)
        logo_box.setStyleSheet(f"background-color: {Theme.SURFACE}; border-bottom: 1px solid {Theme.BORDER};")
        logo_layout = QHBoxLayout(logo_box)
        
        logo = QLabel("SECURITY\nCONSOLE")
        logo.setStyleSheet(f"font-weight: 900; font-size: 20px; color: {Theme.TEXT_MAIN};")
        icon = QLabel("🛡️")
        icon.setStyleSheet("font-size: 32px; background: transparent;")
        
        logo_layout.addWidget(icon)
        logo_layout.addWidget(logo)
        logo_layout.addStretch()
        
        layout.addWidget(logo_box)
        layout.addSpacing(20)
        
        # Navigation
        self.nav_buttons = []
        # (Text, IconName, StackIndex)
        items = [
            ("Dashboard", "fa5s.chart-line", 0),
            ("Live Monitor", "fa5s.video", 1),
            ("Add Employee", "fa5s.user-plus", 2),
            ("Manage Employees", "fa5s.users", 3),
            ("Security Alerts", "fa5s.bell", 4),
            ("System Settings", "fa5s.cog", 5),
        ]
        
        for text, icon, idx in items:
            btn = self.create_nav_btn(text, icon, idx)
            layout.addWidget(btn)
            
        layout.addStretch()
        
        # Bottom Info
        version = QLabel("Admin Access Only")
        version.setStyleSheet(f"color: {Theme.DANGER}; padding: 20px; font-size: 11px; font-weight: bold;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)

        self.main_layout.addWidget(self.sidebar)

    def create_nav_btn(self, text, icon_name, index):
        btn = QPushButton(f"  {text}")
        btn.setIcon(qta.icon(icon_name, color=Theme.TEXT_SUB))
        btn.setIconSize(QSize(20, 20))
        btn.setObjectName("NavButton")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Store index and connect
        btn.clicked.connect(lambda checked, idx=index: self.switch_view(idx))
        
        btn.target_index = index
        self.nav_buttons.append(btn)
        return btn

    def create_topbar(self):
        self.topbar = QFrame()
        self.topbar.setObjectName("TopBar")
        self.topbar.setFixedHeight(60)
        
        layout = QHBoxLayout(self.topbar)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Left: Breadcrumb/Page Title
        self.page_title = QLabel("Dashboard")
        self.page_title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {Theme.TEXT_MAIN};")
        layout.addWidget(self.page_title)
        
        layout.addStretch()
        
        # Right: Status Indicators
        status_box = QFrame()
        status_box.setStyleSheet(f"background-color: {Theme.SURFACE_HOVER}; border-radius: 15px; padding: 5px 15px;")
        sb_layout = QHBoxLayout(status_box)
        sb_layout.setContentsMargins(0,0,0,0)
        
        dot = QLabel("●")
        dot.setStyleSheet(f"color: {Theme.ACCENT}; font-size: 12px;")
        status = QLabel(" SYSTEM ACTIVE")
        status.setObjectName("SystemStatus")
        
        sb_layout.addWidget(dot)
        sb_layout.addWidget(status)
        layout.addWidget(status_box)
        
        layout.addSpacing(20)
        
        # Time
        self.time_label = QLabel()
        self.time_label.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-weight: 600;")
        layout.addWidget(self.time_label)
        
        # Admin Icon
        admin = QLabel("👤 Admin")
        admin.setStyleSheet(f"font-weight: bold; padding-left: 20px; border-left: 1px solid {Theme.BORDER};")
        layout.addWidget(admin)
        
        self.right_layout.addWidget(self.topbar)
        
        # Timer for clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        now = QDateTime.currentDateTime()
        self.time_label.setText(now.toString("yyyy-MM-dd HH:mm:ss"))

    def switch_view(self, index):
        self.content_area.setCurrentIndex(index)
        
        # Update Titles
        titles = ["Security Dashboard", "Live Surveillance", "Biometric Registration", "Authorized Personnel", "System Alerts"]
        if index < len(titles):
            self.page_title.setText(titles[index])
        
        # Active State Styling
        for btn in self.nav_buttons:
            isActive = (btn.target_index == index)
            btn.setProperty("active", isActive)
            
            # Update Icon Color
            icon_name = "fa5s.chart-line" # Default
            # Ideally we re-set icon here to change color, but skipping for perf.
            # CSS handles text color and border.
            
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            
        # DYNAMIC SIGNAL MANAGEMENT (Deadlock Fix)
        # Only connected the active view to the camera stream.
        try:
            self.camera_thread.frame_ready.disconnect()
        except TypeError:
            pass # Was not connected

        if index == 1: # Monitor
            self.camera_thread.frame_ready.connect(self.monitor_view.update_frame)
        elif index == 2: # Register
            self.camera_thread.frame_ready.connect(self.register_view.update_preview)

        # UNBLOCK: Reset the throttle flag
        self.camera_thread.reset_throttle()

    def closeEvent(self, event):
        self.camera_thread.stop()
        event.accept()
