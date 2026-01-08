import os
import cv2
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QFrame
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from ui.styles import Theme
from core.employee_manager import EmployeeManager

class DatabaseView(QWidget):
    """
    Admin View: Manage Employees.
    Lists registered employees with their ID/Role metadata.
    Allows revoking access (deletion).
    """
    database_changed = pyqtSignal()

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.emp_manager = EmployeeManager()
        self.init_ui()

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_list()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("Manage Employees")
        header.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Theme.TEXT_MAIN};")
        layout.addWidget(header)
        
        sub = QLabel("View and manage authorized personnel credentials.")
        sub.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-size: 14px;")
        layout.addWidget(sub)
        
        layout.addSpacing(20)
        
        # List
        self.user_list = QListWidget()
        self.user_list.setStyleSheet("QListWidget::item { background: transparent; }") 
        layout.addWidget(self.user_list)
        
        # Footer / Stats
        self.stats_label = QLabel("Total Registered: 0")
        self.stats_label.setStyleSheet(f"color: {Theme.ACCENT}; font-weight: bold;")
        layout.addWidget(self.stats_label)
        
        self.refresh_list()

    def refresh_list(self):
        self.user_list.clear()
        
        # Refresh DB
        self.emp_manager.load_db()
        
        if not os.path.exists(self.engine.known_faces_dir):
            os.makedirs(self.engine.known_faces_dir)

        # Get all users (sorted)
        users = sorted(self.engine.known_embeddings.keys())
        
        for name in users:
            item = QListWidgetItem(self.user_list)
            
            # Fetch Metadata
            emp_data = self.emp_manager.get_employee(name)
            emp_id = emp_data.get("id", "N/A")
            role = emp_data.get("role", "Unauthorized")
            dept = emp_data.get("dept", "Unknown")
            
            # Create a robust container widget
            container = QFrame()
            container.setStyleSheet(f"""
                QFrame {{
                    background-color: {Theme.SURFACE}; 
                    border-radius: 10px; 
                    border: 1px solid {Theme.BORDER};
                }}
            """)
            container.setMinimumHeight(90)
            
            layout = QHBoxLayout(container)
            layout.setContentsMargins(15, 12, 15, 12)
            layout.setSpacing(20)
            
            # Thumbnail
            thumb_label = QLabel()
            image_path = os.path.join(self.engine.known_faces_dir, f"{name}.jpg")
            if not os.path.exists(image_path):
                image_path = os.path.join(self.engine.known_faces_dir, f"{name}_0.jpg")
                
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    thumb_label.setPixmap(pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation))
                    thumb_label.setStyleSheet(f"border-radius: 30px; border: 2px solid {Theme.PRIMARY};")
            
            if thumb_label.pixmap() is None:
                thumb_label.setText("👤")
                thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                thumb_label.setStyleSheet(f"background-color: {Theme.SURFACE_HOVER}; border-radius: 30px; font-size: 24px;")
            
            thumb_label.setFixedSize(60, 60)
            layout.addWidget(thumb_label)
            
            # Info Block
            info_layout = QVBoxLayout()
            info_layout.setSpacing(2)
            
            name_label = QLabel(name.upper())
            name_label.setStyleSheet(f"font-weight: 800; color: {Theme.TEXT_MAIN}; font-size: 16px; border: none; background: transparent;")
            info_layout.addWidget(name_label)
            
            details = QLabel(f"ID: {emp_id}  |  {role}  |  {dept}")
            details.setStyleSheet(f"color: {Theme.PRIMARY}; font-size: 12px; font-weight: bold; border: none; background: transparent;")
            info_layout.addWidget(details)
            
            layout.addLayout(info_layout)
            layout.addStretch()
            
            # Delete button
            del_btn = QPushButton("Revoke Access")
            del_btn.setObjectName("DangerButton")
            del_btn.setFixedWidth(140)
            del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            del_btn.clicked.connect(lambda checked, n=name: self.delete_user(n))
            layout.addWidget(del_btn)
            
            # Set widget for item
            item.setSizeHint(container.sizeHint())
            self.user_list.addItem(item)
            self.user_list.setItemWidget(item, container)
            
        self.stats_label.setText(f"Total Registered: {len(users)}")

    def delete_user(self, name):
        reply = QMessageBox.question(self, 'Confirm Revocation', 
                                    f"Are you sure you want to PERMANENTLY remove '{name}' from the security database?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # 1. Remove from Face Engine
            self.engine.delete_person(name)
            
            # 2. Remove from Employee Database
            self.emp_manager.delete_employee(name)
                
            self.refresh_list()
            self.database_changed.emit()
            QMessageBox.information(self, "Success", f"Access for '{name}' revoked.")
