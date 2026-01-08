
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QProgressBar
from PyQt6.QtCore import Qt
import qtawesome as qta
from ui.styles import Theme

class DashboardView(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # 1. Stats Row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        # Count real users
        user_count = len(self.engine.known_embeddings)
        
        self.card_users = self.create_stat_card("Authorized Users", str(user_count), "fa5s.users", Theme.PRIMARY)
        self.card_alerts = self.create_stat_card("Alerts Today", "12", "fa5s.bell", Theme.DANGER)
        self.card_cameras = self.create_stat_card("Active Cameras", "1", "fa5s.video", Theme.ACCENT)
        self.card_uptime = self.create_stat_card("System Uptime", "3h 20m", "fa5s.clock", Theme.WARNING)
        
        stats_layout.addWidget(self.card_users)
        stats_layout.addWidget(self.card_alerts)
        stats_layout.addWidget(self.card_cameras)
        stats_layout.addWidget(self.card_uptime)
        
        layout.addLayout(stats_layout)
        
        # 2. Main Content (Two Columns)
        content_layout = QHBoxLayout()
        
        # Left: Activity Graph (Placeholder)
        graph_card = QFrame()
        graph_card.setObjectName("Card")
        graph_card.setSizePolicy(
            graph_card.sizePolicy().horizontalPolicy(), 
            graph_card.sizePolicy().verticalPolicy()
        )
        graph_layout = QVBoxLayout(graph_card)
        
        g_title = QLabel("Security Event Trends (7 Days)")
        g_title.setObjectName("CardTitle")
        graph_layout.addWidget(g_title)
        
        # Mock Bar Graph
        bars = QFrame()
        bars_layout = QHBoxLayout(bars)
        bars_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        for height in [40, 70, 30, 90, 50, 60, 20]:
            bar = QFrame()
            bar.setFixedWidth(40)
            bar.setFixedHeight(height * 2)
            bar.setStyleSheet(f"background-color: {Theme.SECONDARY}; border-radius: 4px;")
            bars_layout.addWidget(bar)
            
        graph_layout.addWidget(bars)
        content_layout.addWidget(graph_card, stretch=2)
        
        # Right: CPU/Memory Usage
        sys_card = QFrame()
        sys_card.setObjectName("Card")
        sys_layout = QVBoxLayout(sys_card)
        
        sys_layout.addWidget(QLabel("System Resources", objectName="CardTitle"))
        sys_layout.addSpacing(20)
        
        self.add_progress(sys_layout, "CPU Usage", 32, Theme.PRIMARY)
        self.add_progress(sys_layout, "Memory", 64, Theme.WARNING)
        self.add_progress(sys_layout, "GPU Load", 12, Theme.ACCENT)
        sys_layout.addStretch()
        
        content_layout.addWidget(sys_card, stretch=1)
        
        layout.addLayout(content_layout)
        layout.addStretch()

    def create_stat_card(self, title, value, icon_name, color):
        card = QFrame()
        card.setObjectName("Card")
        card.setStyleSheet(f"QFrame#Card {{ border-left: 4px solid {color}; }}")
        
        l = QVBoxLayout(card)
        
        # Header (Icon + Title)
        header = QHBoxLayout()
        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color=color).pixmap(24, 24))
        t_label = QLabel(title)
        t_label.setObjectName("CardTitle")
        
        header.addWidget(icon)
        header.addWidget(t_label)
        header.addStretch()
        l.addLayout(header)
        
        # Value
        v_label = QLabel(value)
        v_label.setObjectName("CardValue")
        l.addWidget(v_label)
        
        return card

    def add_progress(self, layout, label, value, color):
        lbl = QLabel(label)
        lbl.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-weight: 600;")
        layout.addWidget(lbl)
        
        prog = QProgressBar()
        prog.setValue(value)
        prog.setFixedHeight(8)
        prog.setTextVisible(False)
        prog.setStyleSheet(f"""
            QProgressBar {{
                background-color: {Theme.SURFACE_HOVER};
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(prog)
        layout.addSpacing(15)
