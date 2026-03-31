import os
import cv2
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QFrame
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from ui.styles import Theme
from core.child_manager import ChildManager
from core.translator import Translator as T

class DatabaseView(QWidget):
    """
    Admin View: Manage Missing Children Records.
    Lists registered children with their metadata.
    Allows closing cases (deletion).
    """
    database_changed = pyqtSignal()

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.child_manager = ChildManager()
        self.init_ui()

    def showEvent(self, event):
        super().showEvent(event)
        self.refresh_list()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel(T.tr("Missing Children DB"))
        header.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {Theme.TEXT_MAIN};")
        layout.addWidget(header)
        
        sub = QLabel("View and manage missing child records active in the system.")
        sub.setStyleSheet(f"color: {Theme.TEXT_SUB}; font-size: 14px;")
        layout.addWidget(sub)
        
        layout.addSpacing(20)
        
        # List
        self.user_list = QListWidget()
        self.user_list.setStyleSheet("QListWidget::item { background: transparent; }") 
        layout.addWidget(self.user_list)
        
        # Footer / Stats
        self.stats_label = QLabel("Total Active Cases: 0")
        self.stats_label.setStyleSheet(f"color: {Theme.ACCENT}; font-weight: bold;")
        layout.addWidget(self.stats_label)
        
        self.refresh_list()

    def refresh_list(self):
        self.user_list.clear()
        
        # Refresh DB
        self.child_manager.load_db()
        
        if not os.path.exists(self.engine.known_faces_dir):
            os.makedirs(self.engine.known_faces_dir)

        # Get all children from the database instead of just active embeddings
        all_children = self.child_manager.get_all_children()
        users = sorted(all_children.keys())
        
        for name in users:
            item = QListWidgetItem(self.user_list)
            
            # Fetch Metadata
            child_data = self.child_manager.get_child(name)
            age = child_data.get("age", "Unknown Age")
            location = child_data.get("last_seen_location", "Unknown Location")
            date_missing = child_data.get("date_missing", "Unknown Date")
            aadhar = child_data.get("aadhar_number", "Not Provided")
            status = child_data.get("status", "Missing")
            
            # Create a robust container widget
            container = QFrame()
            container.setStyleSheet(f"""
                QFrame {{
                    background-color: {Theme.SURFACE}; 
                    border-radius: 8px; 
                    border: 1px solid {Theme.BORDER};
                }}
            """)
            container.setMinimumHeight(70)
            
            layout = QHBoxLayout(container)
            layout.setContentsMargins(12, 8, 12, 8)
            layout.setSpacing(15)
            
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
            
            thumb_label.setFixedSize(50, 50)
            layout.addWidget(thumb_label)
            
            # Info Block
            info_layout = QVBoxLayout()
            info_layout.setSpacing(2)
            
            name_label = QLabel(name.upper())
            name_label.setStyleSheet(f"font-weight: 800; color: {Theme.TEXT_MAIN}; font-size: 14px; border: none; background: transparent;")
            info_layout.addWidget(name_label)
            
            details = QLabel(f"Age: {age}  |  Last Seen: {location}  |  Missing Since: {date_missing}\nAadhar: {aadhar}  |  Status: {status.upper()}")
            
            if status == "Active":
                details.setStyleSheet(f"color: {Theme.PRIMARY}; font-size: 11px; font-weight: bold; border: none; background: transparent;")
            else:
                details.setStyleSheet(f"color: {Theme.WARNING}; font-size: 11px; font-weight: bold; border: none; background: transparent;")
                
            info_layout.addWidget(details)
            
            layout.addLayout(info_layout)
            layout.addStretch()
            
            # Action Buttons Layout
            action_layout = QVBoxLayout()
            
            # 1. Approve Button (Only visible if Pending and user is Police/Admin)
            role = self.window().role if hasattr(self.window(), 'role') else "Volunteer"
            if status != "Active" and role in ["Police", "Government"]:
                approve_btn = QPushButton(T.tr("Approve Case"))
                approve_btn.setFixedWidth(140)
                approve_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                approve_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {Theme.SUCCESS};
                        color: #ffffff;
                        border-radius: 4px;
                        font-weight: bold;
                        padding: 5px;
                        font-size: 11px;
                    }}
                    QPushButton:hover {{ background-color: #2fb56e; }}
                """)
                approve_btn.clicked.connect(lambda checked, n=name: self.approve_user(n))
                action_layout.addWidget(approve_btn)

            # 2. Delete button
            del_btn = QPushButton(T.tr("Close Case"))
            del_btn.setObjectName("SecondaryButton")
            del_btn.setFixedWidth(120)
            del_btn.setStyleSheet("font-size: 11px; padding: 5px;")
            del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            del_btn.clicked.connect(lambda checked, n=name: self.delete_user(n))
            action_layout.addWidget(del_btn)
            
            layout.addLayout(action_layout)
            
            # Set widget for item
            item.setSizeHint(container.sizeHint())
            self.user_list.addItem(item)
            self.user_list.setItemWidget(item, container)
            
        self.stats_label.setText(f"Total Active Cases: {len(users)}")

    def retranslate_ui(self):
        self.refresh_list()

    def approve_user(self, name):
        reply = QMessageBox.question(self, 'Confirm Approval', 
                                    f"Approve '{name}'? This will immediately activate their facial recognition on all surveillance cameras.",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # Update DB
            self.child_manager.approve_child(name)
            
            # Reload the RAM embeddings
            self.engine.reload_known_faces()
            
            self.refresh_list()
            self.database_changed.emit()
            QMessageBox.information(self, "Success", f"Case '{name}' Approved and Active!")

    def delete_user(self, name):
        reply = QMessageBox.question(self, 'Confirm Case Closure', 
                                    f"Are you sure you want to completely remove the record for '{name}'? This usually means the child has been found.",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # 1. Remove from Face Engine
            self.engine.delete_person(name)
            
            # 2. Remove from Child Database
            self.child_manager.delete_child(name)
                
            self.refresh_list()
            self.database_changed.emit()
            QMessageBox.information(self, "Success", f"Case for '{name}' closed successfully.")
