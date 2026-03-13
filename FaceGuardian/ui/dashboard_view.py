from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QProgressBar, QGraphicsDropShadowEffect, QPushButton
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QColor
import qtawesome as qta
from ui.styles import Theme

class AnimatedStatCard(QFrame):
    """Premium stat card with count-up animation and glow effect"""
    
    def __init__(self, title, target_value, icon_name, color, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self.target_value = target_value
        self.current_value = 0
        self.color = color
        
        # Add glow effect
        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(20)
        glow.setColor(QColor(color))
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)
        
        # Custom styling for gradient border
        self.setStyleSheet(f"""
            QFrame#Card {{
                border-left: 4px solid {color};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        
        # Header with icon
        header = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color=color).pixmap(28, 28))
        
        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")
        
        header.addWidget(icon_label)
        header.addWidget(title_label)
        header.addStretch()
        layout.addLayout(header)
        
        # Animated value
        self.value_label = QLabel("0")
        self.value_label.setObjectName("CardValue")
        layout.addWidget(self.value_label)
        
        # Trend indicator
        trend_layout = QHBoxLayout()
        self.trend_icon = QLabel("↑")
        self.trend_icon.setStyleSheet(f"color: {Theme.ACCENT}; font-size: 18px; font-weight: bold;")
        self.trend_text = QLabel("+12% from last week")
        self.trend_text.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-size: 12px;")
        trend_layout.addWidget(self.trend_icon)
        trend_layout.addWidget(self.trend_text)
        trend_layout.addStretch()
        layout.addLayout(trend_layout)
        
        # Start count-up animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_value)
        self.timer.start(30)  # Update every 30ms
        
    def animate_value(self):
        """Animate value counting up"""
        if self.current_value < self.target_value:
            increment = max(1, (self.target_value - self.current_value) // 10)
            self.current_value = min(self.current_value + increment, self.target_value)
            self.value_label.setText(str(self.current_value))
        else:
            self.timer.stop()


class DashboardView(QWidget):
    """Advanced dashboard with premium animations and effects"""
    
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(30)
        
        # Welcome header
        welcome = QLabel("Security Command Center")
        welcome.setStyleSheet(f"font-size: 28px; font-weight: 900; color: {Theme.TEXT_MAIN}; padding-bottom: 10px;")
        layout.addWidget(welcome)
        
        # Animated stat cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(24)
        
        user_count = len(self.engine.known_embeddings)
        
        self.card_users = AnimatedStatCard("Active Missing Cases", user_count, "fa5s.search", Theme.DANGER)
        self.card_alerts = AnimatedStatCard("Reported Sightings", 23, "fa5s.bell", Theme.WARNING)
        self.card_cameras = AnimatedStatCard("Active Cameras", 1, "fa5s.video", Theme.ACCENT)
        self.card_uptime = AnimatedStatCard("System Uptime", 99, "fa5s.clock", Theme.WARNING)
        
        stats_layout.addWidget(self.card_users)
        stats_layout.addWidget(self.card_alerts)
        stats_layout.addWidget(self.card_cameras)
        stats_layout.addWidget(self.card_uptime)
        
        layout.addLayout(stats_layout)
        
        # Main content area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(24)
        
        # Left: Activity chart
        chart_card = QFrame()
        chart_card.setObjectName("Card")
        chart_layout = QVBoxLayout(chart_card)
        
        chart_title = QLabel("System Lookups & Matches - Last 7 Days")
        chart_title.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {Theme.TEXT_MAIN}; margin-bottom: 10px;")
        chart_layout.addWidget(chart_title)
        
        bars_container = QFrame()
        bars_layout = QHBoxLayout(bars_container)
        bars_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        bars_layout.setSpacing(12)
        
        heights = [60, 85, 45, 95, 70, 80, 35]
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        
        self.animations = []
        for i, (height, day) in enumerate(zip(heights, days)):
            bar_container = QVBoxLayout()
            bar = QFrame()
            bar.setFixedWidth(50)
            bar.setMinimumHeight(0)
            bar.setMaximumHeight(0)
            bar.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {Theme.PRIMARY}, stop:1 {Theme.SECONDARY}); border-radius: 8px;")
            
            # ANIMATION
            anim = QPropertyAnimation(bar, b"maximumHeight")
            anim.setDuration(1000 + i*100)
            anim.setStartValue(0)
            anim.setEndValue(height * 2)
            anim.setEasingCurve(QEasingCurve.Type.OutBounce)
            anim.start()
            self.animations.append(anim)
            
            min_anim = QPropertyAnimation(bar, b"minimumHeight")
            min_anim.setDuration(1000 + i*100)
            min_anim.setStartValue(0)
            min_anim.setEndValue(height * 2)
            min_anim.setEasingCurve(QEasingCurve.Type.OutBounce)
            min_anim.start()
            self.animations.append(min_anim)
            
            day_label = QLabel(day)
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_label.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-size: 12px; font-weight: 600;")
            
            bar_container.addWidget(bar, alignment=Qt.AlignmentFlag.AlignBottom)
            bar_container.addWidget(day_label)
            bars_layout.addLayout(bar_container)
            
        chart_layout.addWidget(bars_container)
        content_layout.addWidget(chart_card, stretch=2)
        
        # Right: System resources
        sys_card = QFrame()
        sys_card.setObjectName("Card")
        sys_layout = QVBoxLayout(sys_card)
        sys_layout.setSpacing(15)
        
        sys_title = QLabel("System Resources")
        sys_title.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {Theme.TEXT_MAIN};")
        sys_layout.addWidget(sys_title)
        
        self.add_premium_progress(sys_layout, "CPU Usage", 42, Theme.PRIMARY)
        self.add_premium_progress(sys_layout, "Memory", 68, Theme.WARNING)
        self.add_premium_progress(sys_layout, "GPU Load", 15, Theme.ACCENT)
        self.add_premium_progress(sys_layout, "Network", 28, Theme.SECONDARY)
        
        # Quick actions
        actions_title = QLabel("Quick Actions")
        actions_title.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {Theme.TEXT_SUB}; margin-top: 10px;")
        sys_layout.addWidget(actions_title)
        
        scan_btn = QPushButton(" Scan Image")
        scan_btn.setObjectName("SecondaryButton")
        scan_btn.setIcon(qta.icon('fa5s.camera', color=Theme.PRIMARY))
        sys_layout.addWidget(scan_btn)
        
        export_btn = QPushButton(" Export Report")
        export_btn.setObjectName("SecondaryButton")
        export_btn.setIcon(qta.icon('fa5s.file-export', color=Theme.PRIMARY))
        sys_layout.addWidget(export_btn)
        
        sys_layout.addStretch() # Proper placement of stretch
        
        content_layout.addWidget(sys_card, stretch=1)
        layout.addLayout(content_layout)
        layout.addStretch()
        
    def add_premium_progress(self, layout, label, value, color):
        """Add animated progress bar"""
        lbl = QLabel(label)
        lbl.setStyleSheet(f"color: {Theme.TEXT_MAIN}; font-weight: 700; font-size: 13px;")
        layout.addWidget(lbl)
        
        prog_container = QHBoxLayout()
        prog = QProgressBar()
        prog.setFixedHeight(10)
        prog.setTextVisible(False)
        prog.setStyleSheet(f"QProgressBar {{ background: rgba(100, 116, 139, 0.2); border-radius: 5px; }} QProgressBar::chunk {{ background-color: {color}; border-radius: 5px; }}")
        
        anim = QPropertyAnimation(prog, b"value")
        anim.setDuration(1000)
        anim.setStartValue(0)
        anim.setEndValue(value)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self.animations.append(anim)
        
        val_lbl = QLabel(f"{value}%")
        val_lbl.setStyleSheet(f"color: {color}; font-weight: 800; font-size: 14px;")
        val_lbl.setFixedWidth(40)
        
        prog_container.addWidget(prog)
        prog_container.addWidget(val_lbl)
        layout.addLayout(prog_container)
