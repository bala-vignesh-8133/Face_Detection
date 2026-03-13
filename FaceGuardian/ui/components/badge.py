from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt
from PyQt6.QtGui import QFont
from ui.styles import Theme

class StatusBadge(QLabel):
    """
    Status badge with optional pulse animation
    """
    
    def __init__(self, text, badge_type='success', pulse=False, parent=None):
        super().__init__(text, parent)
        self.badge_type = badge_type
        self.pulse_enabled = pulse
        
        self.setup_ui()
        if pulse:
            self.setup_pulse()
            
    def setup_ui(self):
        """Setup badge appearance"""
        # Colors based on type
        colors = {
            'success': Theme.ACCENT,
            'danger': Theme.DANGER,
            'warning': Theme.WARNING,
            'info': Theme.PRIMARY,
            'default': Theme.TEXT_SUB
        }
        
        bg_color = colors.get(self.badge_type, colors['default'])
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: white;
                border-radius: 10px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
            }}
        """)
        
        self.setFont(QFont(Theme.FONT_FAMILY, 11, QFont.Weight.Bold))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.adjustSize()
        
    def setup_pulse(self):
        """Setup pulse animation"""
        self.pulse_animation = QPropertyAnimation(self, b"minimumSize")
        self.pulse_animation.setDuration(1000)
        self.pulse_animation.setStartValue(self.size())
        self.pulse_animation.setEndValue(QSize(self.width() + 4, self.height() + 2))
        self.pulse_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.pulse_animation.setLoopCount(-1)  # Infinite loop
        self.pulse_animation.start()


class NotificationBadge(QLabel):
    """
    Small circular notification badge (for counts)
    """
    
    def __init__(self, count=0, parent=None):
        super().__init__(str(count) if count > 0 else "", parent)
        self.count = count
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {Theme.DANGER};
                color: white;
                border-radius: 10px;
                font-size: 10px;
                font-weight: 800;
                min-width: 20px;
                min-height: 20px;
                max-width: 20px;
                max-height: 20px;
            }}
        """)
        
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setVisible(count > 0)
        
    def set_count(self, count):
        """Update badge count"""
        self.count = count
        if count > 0:
            display_text = str(count) if count < 100 else "99+"
            self.setText(display_text)
            self.setVisible(True)
        else:
            self.setText("")
            self.setVisible(False)
