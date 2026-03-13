from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import QTimer, QPropertyAnimation, QRect, Qt
from PyQt6.QtGui import QPainter, QColor, QPen
from ui.styles import Theme

class LoadingSpinner(QWidget):
    """
    Animated loading spinner
    """
    
    def __init__(self, size=40, color=None, parent=None):
        super().__init__(parent)
        self.size = size
        self.color = QColor(color if color else Theme.PRIMARY)
        self.angle = 0
        
        self.setFixedSize(size, size)
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.setInterval(50)  # 20 FPS
        
    def start(self):
        """Start spinning animation"""
        self.timer.start()
        self.show()
        
    def stop(self):
        """Stop spinning animation"""
        self.timer.stop()
        self.hide()
        
    def rotate(self):
        """Rotate the spinner"""
        self.angle = (self.angle + 10) % 360
        self.update()
        
    def paintEvent(self, event):
        """Draw the spinner"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw arc
        pen = QPen(self.color, 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        rect = QRect(4, 4, self.size - 8, self.size - 8)
        painter.drawArc(rect, self.angle * 16, 120 * 16)


class LoadingOverlay(QWidget):
    """
    Full-screen loading overlay with spinner
    """
    
    def __init__(self, parent=None, message="Loading..."):
        super().__init__(parent)
        self.message = message
        
        # Semi-transparent background
        self.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(15, 23, 42, 0.8);
            }}
        """)
        
        # Spinner
        self.spinner = LoadingSpinner(60, Theme.PRIMARY, self)
        
        # Message label
        self.label = QLabel(message, self)
        self.label.setStyleSheet(f"""
            QLabel {{
                color: {Theme.TEXT_MAIN};
                font-size: 16px;
                font-weight: 600;
                background: transparent;
            }}
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Hide by default
        self.hide()
        
    def showEvent(self, event):
        """Center spinner and label when shown"""
        if self.parent():
            self.setGeometry(self.parent().rect())
            
        # Center spinner
        spinner_x = (self.width() - self.spinner.width()) // 2
        spinner_y = (self.height() - self.spinner.height()) // 2 - 30
        self.spinner.move(spinner_x, spinner_y)
        
        # Center label below spinner
        self.label.setGeometry(0, spinner_y + 80, self.width(), 30)
        
        self.spinner.start()
        super().showEvent(event)
        
    def hideEvent(self, event):
        """Stop spinner when hidden"""
        self.spinner.stop()
        super().hideEvent(event)
