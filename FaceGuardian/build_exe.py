import os
import subprocess
import sys

def build():
    print("--- FaceGuardian EXE Builder ---")
    
    # Check for PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Define the command
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed", # No console
        "--name", "FaceGuardian",
        "--add-data", "face_landmarker.task;.",
        # Include source folders as data if they contain non-python files (styles, etc.)
        # but here we mostly need them as packages. PyInstaller handles code imports.
        # However, we must ensure config and known_faces stay OUTSIDE.
        
        # Collect all requirements automatically
        "--collect-all", "facenet_pytorch",
        "--collect-all", "torch",
        "--collect-all", "qtawesome",
        "--collect-all", "mediapipe",
        
        # Main entry point
        "main.py"
    ]

    print(f"Running: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
        print("\n✅ Build Successful!")
        print(f"Your EXE is located in: {os.path.join(os.getcwd(), 'dist', 'FaceGuardian.exe')}")
        print("\nNote: Make sure to keep 'config.json' and 'known_faces' folder in the same folder as the EXE.")
    except Exception as e:
        print(f"\n❌ Build Failed: {e}")

if __name__ == "__main__":
    # Ensure we are in the FaceGuardian directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build()
