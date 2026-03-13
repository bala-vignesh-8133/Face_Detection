from PyQt6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Qt, QPoint
from PyQt6.QtGui import QFont
from ui.styles import Theme

class ToastNotification(QLabel):
    """
    Modern toast notification with auto-dismiss and slide-in animation
    """
    
    def __init__(self, message, toast_type='info', parent=None, duration=3000):
        super().__init__(message, parent)
        self.duration = duration
        self.toast_type = toast_type
        
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        """Setup toast appearance"""
        # Colors based on type
        colors = {
            'success': (Theme.ACCENT, 'white'),
            'error': (Theme.DANGER, 'white'),
            'warning': (Theme.WARNING, 'white'),
            'info': (Theme.PRIMARY, 'white')
        }
        
        bg_color, text_color = colors.get(self.toast_type, colors['info'])
        
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
                border: none;
            }}
        """)
        
        self.setFont(QFont(Theme.FONT_FAMILY, 14, QFont.Weight.Bold))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumWidth(250)
        self.setMaximumWidth(400)
        self.adjustSize()
        
        # Set window flags for overlay
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
    def setup_animation(self):
        """Setup slide-in and fade animations"""
        # Opacity effect
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        # Fade in animation
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Fade out animation
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(300)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InCubic)
        self.fade_out.finished.connect(self.close)
        
    def show_toast(self, parent_widget=None):
        """Show toast with animation"""
        if parent_widget:
            # Position at top-center of parent
            parent_rect = parent_widget.rect()
            x = parent_rect.center().x() - self.width() // 2
            y = 20
            self.move(parent_widget.mapToGlobal(QPoint(x, y)))
        
        self.show()
        self.fade_in.start()
        
        # Auto-dismiss after duration
        QTimer.singleShot(self.duration, self.dismiss)
        
    def dismiss(self):
        """Dismiss toast with fade out"""
        self.fade_out.start()
        
    def mousePressEvent(self, event):
        """Click to dismiss"""
        self.dismiss()


def show_toast(message, toast_type='info', parent=None, duration=3000):
    """
    Convenience function to show toast notification
    
    Args:
        message: Text to display
        toast_type: 'success', 'error', 'warning', 'info'
        parent: Parent widget
        duration: Display duration in milliseconds
    """
    toast = ToastNotification(message, toast_type, parent, duration)
    toast.show_toast(parent)
    return toast
