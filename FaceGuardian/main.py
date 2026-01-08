import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def get_base_path():
    """Get the correct base path whether running as script or EXE."""
    if getattr(sys, 'frozen', False):
        # Running as bundled EXE
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

def main():
    # Ensure the app uses the folder where the EXE/script is located for user data
    base_path = get_base_path()
    os.chdir(base_path)
    
    app = QApplication(sys.argv)
    app.setApplicationName("FaceGuardian")
    
    # Ensure we use absolute paths for the engine to avoid confusion
    known_faces_path = os.path.join(base_path, "known_faces")
    if not os.path.exists(known_faces_path):
        os.makedirs(known_faces_path)
        
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
