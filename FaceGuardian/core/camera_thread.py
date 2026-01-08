import cv2
import numpy as np
import time
from PyQt6.QtCore import QThread, pyqtSignal

class CameraThread(QThread):
    # frame, results
    frame_ready = pyqtSignal(np.ndarray, list)
    camera_changed = pyqtSignal(str) # Emits camera name/index

    def __init__(self, engine, camera_index=0):
        super().__init__()
        self.engine = engine
        self.camera_index = camera_index
        self.running = True
        self.cap = None
        self._render_pending = False
        self._camera_switch_pending = False
        self._new_index = 0

    def set_render_finished(self):
        self._render_pending = False

    def reset_throttle(self):
        """Force reset throttle when changing views to prevent deadlock"""
        self._render_pending = False

    def change_camera(self, source):
        """Request a source switch (integer for webcam, string for path)"""
        self._new_index = source
        self._camera_switch_pending = True
        # Proactively release to break a blocking read() if necessary
        if self.cap:
            self.cap.release()
            self.cap = None

    def run(self):
        self._open_camera()
        
        self.frame_count = 0
        self.last_results = []
        is_file = isinstance(self.camera_index, str)
        
        while self.running:
            # Handle Camera Switch
            if self._camera_switch_pending:
                self.camera_index = self._new_index
                is_file = isinstance(self.camera_index, str)
                self._open_camera()
                self._camera_switch_pending = False
                
                import os
                source_name = os.path.basename(self.camera_index) if is_file else f"Source #{self.camera_index}"
                self.camera_changed.emit(source_name)

            if not self.cap or not self.cap.isOpened():
                time.sleep(0.01) # Faster polling
                continue

            ret, frame = self.cap.read()
            if not ret:
                if is_file:
                    # Loop video file
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                else:
                    time.sleep(0.01)
                    continue

            # Drop frame if UI is still processing the previous one
            if self._render_pending:
                continue

            frame = cv2.flip(frame, 1)
            self.frame_count += 1
            
            # OPTIMIZATION: Process AI only every 3rd frame
            if self.frame_count % 3 == 0:
                try:
                    faces = self.engine.detect_faces(frame)
                except Exception as e:
                    print(f"Detection Error: {e}")
                    faces = None
                
                results = []
                if faces is not None:
                    for face in faces:
                        x, y, w, h = map(int, face[:4])
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
                results = self.last_results

            self._render_pending = True
            self.frame_ready.emit(frame, results)
            
            # Control playback speed for video files (approx 30fps)
            if is_file:
                time.sleep(0.03)
            
        if self.cap:
            self.cap.release()

    def _open_camera(self):
        if self.cap:
            self.cap.release()
        
        if isinstance(self.camera_index, int):
            # Open with DSHOW backend on Windows for faster init
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(self.camera_index)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        else:
            # Video File
            self.cap = cv2.VideoCapture(self.camera_index)

    def stop(self):
        self.running = False
        self.wait()
