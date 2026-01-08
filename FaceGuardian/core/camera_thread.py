import cv2
import numpy as np
import time
from PyQt6.QtCore import QThread, pyqtSignal

class CameraThread(QThread):
    # frame, results
    frame_ready = pyqtSignal(np.ndarray, list)

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.running = True
        self.cap = None
        self._render_pending = False

    def set_render_finished(self):
        self._render_pending = False

    def reset_throttle(self):
        """Force reset throttle when changing views to prevent deadlock"""
        self._render_pending = False

    def run(self):
        self.cap = cv2.VideoCapture(0)
        # OPTIMIZATION: Force 640x480 to prevent lag on high-res webcams
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # CRITICAL: Set buffer size to 1 to reduce latency (Subject to driver support)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        self.frame_count = 0
        self.last_results = []
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue

            # Drop frame if UI is still processing the previous one
            if self._render_pending:
                continue

            frame = cv2.flip(frame, 1)
            self.frame_count += 1
            
            # OPTIMIZATION: Process AI only every 3rd frame (Boosts FPS by 3x)
            # The video feed remains smooth, and boxes update 10 times/sec (sufficient)
            if self.frame_count % 3 == 0:
                # 1. Detection
                try:
                    faces = self.engine.detect_faces(frame)
                except Exception as e:
                    print(f"Detection Error: {e}")
                    faces = None
                
                results = []
                if faces is not None and len(faces) > 0:
                    # Deep copy needed? No, rebuilding list.
                    pass
                    
                if faces is not None:
                    for face in faces:
                        # YuNet box: x,y,w,h are at indices 0,1,2,3
                        x, y, w, h = map(int, face[:4])
                        
                        # 2. Recognition (Only runs if faces found)
                        try:
                            name, confidence = self.engine.recognize(frame, face)
                        except:
                            name, confidence = "Unknown", 0.0
                        
                        results.append({
                            'rect': (x, y, w, h),
                            'name': name,
                            'distance': confidence,
                            'authorized': name != "Unknown"
                        })
                self.last_results = results
            else:
                # Reuse last detections for smoothness
                results = self.last_results

            self._render_pending = True
            self.frame_ready.emit(frame, results)
            
        self.cap.release()

    def stop(self):
        self.running = False
        self.wait()
