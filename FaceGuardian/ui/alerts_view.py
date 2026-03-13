
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QHBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, pyqtSlot
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
        
        self.alerts = []
        self.row = 0
        self.col = 0
        
        scroll.setWidget(content)
        layout.addWidget(scroll)

    @pyqtSlot(str, str, str, str, str)
    def add_alert(self, title, location, time, color, name):
        # Build the card
        card = self.create_alert_card(title, location, time, color, name)
        
        # Add to top (unshift) so newest is first
        # Since QGridLayout doesn't easily support unshifting, 
        # we'll redraw or just append depending on how simple we want it.
        # Here we just insert at end for simplicity, but let's clear and redraw for "newest first" logic
        self.alerts.insert(0, (card, title, location, time, color, name))
        
        # Keep max 50 alerts in memory
        if len(self.alerts) > 50:
            self.alerts.pop()
            
        self.refresh_grid()

    def refresh_grid(self):
        # Clear current grid
        for i in reversed(range(self.grid.count())): 
            widget = self.grid.itemAt(i).widget()
            if widget is not None: 
                widget.setParent(None)
                
        row, col = 0, 0
        for data in self.alerts:
            card_widget = self.create_alert_card(data[1], data[2], data[3], data[4], data[5])
            self.grid.addWidget(card_widget, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

    def create_alert_card(self, title, location, time, color, name):
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
        l.addWidget(QLabel(f"👤 Name: {name}", styleSheet=f"color: {Theme.TEXT_MAIN}; font-weight: bold; font-size: 14px;"))
        l.addWidget(QLabel(f"📍 Area: {location}", styleSheet=f"color: {Theme.TEXT_SUB};"))
        l.addWidget(QLabel(f"🕒 {time}", styleSheet=f"color: {Theme.TEXT_SUB}; font-size: 11px;"))
        
        return card
