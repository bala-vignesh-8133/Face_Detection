
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QHBoxLayout, QGridLayout
from PyQt6.QtCore import Qt
from ui.styles import Theme
import qtawesome as qta

class AlertsView(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        h_layout = QHBoxLayout()
        title = QLabel("Security Alerts")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Theme.TEXT_MAIN};")
        
        btn_refresh = QLabel("Showing last 24 hours")
        btn_refresh.setStyleSheet(f"color: {Theme.TEXT_SUB};")
        
        h_layout.addWidget(title)
        h_layout.addStretch()
        h_layout.addWidget(btn_refresh)
        
        layout.addLayout(h_layout)
        layout.addSpacing(20)
        
        # Scroll Area for Alerts
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        content = QWidget()
        self.grid = QGridLayout(content)
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Mock Data
        alerts = [
            ("Unauthorized Access", "Camera 01", "10:42 AM", Theme.DANGER),
            ("Unknown Face", "Camera 01", "10:41 AM", Theme.WARNING),
            ("Door Forced", "Entrance", "09:15 AM", Theme.DANGER),
            ("System Boot", "Server", "08:00 AM", Theme.PRIMARY),
            ("Connection Lost", "Camera 02", "03:00 AM", Theme.ACCENT),
        ]
        
        row, col = 0, 0
        for title, loc, time, color in alerts:
            card = self.create_alert_card(title, loc, time, color)
            self.grid.addWidget(card, row, col)
            col += 1
            if col > 1: # 2 columns
                col = 0
                row += 1
                
        scroll.setWidget(content)
        layout.addWidget(scroll)

    def create_alert_card(self, title, location, time, color):
        card = QFrame()
        card.setObjectName("Card")
        card.setStyleSheet(f"border-left: 4px solid {color}; background-color: {Theme.SURFACE}; border-radius: 8px;")
        card.setMinimumHeight(100)
        
        l = QVBoxLayout(card)
        l.setSpacing(5)
        
        # Top: Title + Icon
        top = QHBoxLayout()
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {Theme.TEXT_MAIN};")
        
        icon = QLabel("⚠️")
        if color == Theme.PRIMARY: icon.setText("ℹ️")
        
        top.addWidget(t_lbl)
        top.addStretch()
        top.addWidget(icon)
        
        l.addLayout(top)
        
        # Bottom: Location + Time
        l.addWidget(QLabel(f"📍 {location}", styleSheet=f"color: {Theme.TEXT_SUB};"))
        l.addWidget(QLabel(f"🕒 {time}", styleSheet=f"color: {Theme.TEXT_SUB}; font-size: 11px;"))
        
        return card
