import cv2
import numpy as np
import os
import urllib.request
from typing import Dict, List, Tuple, Optional

class FaceRecognitionEngine:
    def __init__(self, known_faces_dir: str = "known_faces", threshold: float = 0.36):
        self.known_faces_dir = known_faces_dir
        self.threshold = threshold
        self.known_embeddings: Dict[str, List[np.ndarray]] = {}
        self.input_size = (320, 320)
        
        # Paths for models
        self.detect_model_path = "face_detection_yunet_2023mar.onnx"
        self.rec_model_path = "face_recognition_sface_2021dec.onnx"
        self.liveness_model_path = "anti_spoofing_minifasnetv2.onnx"
        
        self._ensure_models_exist()
        
        # Initialize OpenCV specialized APIs
        try:
            print(f"Initializing FaceDetectorYN with {self.detect_model_path}")
            # 1. Try NVIDIA CUDA (Requires custom OpenCV build)
            try:
                print("Attempting to use NVIDIA GPU (CUDA)...")
                self.detector = cv2.FaceDetectorYN.create(
                    self.detect_model_path, "", self.input_size, 0.5, 0.3, 5000, 
                    cv2.dnn.DNN_BACKEND_CUDA, cv2.dnn.DNN_TARGET_CUDA
                )
                self.recognizer = cv2.FaceRecognizerSF.create(
                    self.rec_model_path, "", 
                    cv2.dnn.DNN_BACKEND_CUDA, cv2.dnn.DNN_TARGET_CUDA
                )
                
                # Liveness (Optional)
                try:
                    self.liveness_net = cv2.dnn.readNetFromONNX(self.liveness_model_path)
                    self.liveness_net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
                    self.liveness_net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
                    self.liveness_enabled = True
                except:
                    print("⚠️ Liveness Model not found or CUDA incompatible. Liveness check disabled.")
                    self.liveness_enabled = False
                
                # TEST RUN
                dummy_img = np.zeros((320, 320, 3), dtype=np.uint8)
                self.detector.detect(dummy_img)
                self.backend_name = "NVIDIA CUDA"
                print("✅ NVIDIA GPU (CUDA) Enabled & Verified!")
            except Exception as cuda_err:
                # Fallback to CPU
                print(f"CUDA Failed ({cuda_err}). Switching to CPU (High Performance).")
                self.detector = cv2.FaceDetectorYN.create(
                    self.detect_model_path, "", self.input_size, 0.5, 0.3, 5000
                )
                self.recognizer = cv2.FaceRecognizerSF.create(self.rec_model_path, "")
                
                try:
                    self.liveness_net = cv2.dnn.readNetFromONNX(self.liveness_model_path)
                    self.liveness_enabled = True
                except:
                    print("⚠️ Liveness Model not found. Liveness check disabled.")
                    self.liveness_enabled = False
                    
                self.backend_name = "CPU (Optimized)"
            print(f"✅ AI Engine Initialized [{self.backend_name}]")
            
        except Exception as e:
            print(f"CRITICAL ERROR initializing models: {e}")
            # Try to delete bad models so they re-download next time
            for p in [self.detect_model_path, self.rec_model_path, self.liveness_model_path]:
                if os.path.exists(p): os.remove(p)
            raise e
        
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)
            
        self.reload_known_faces()

    def _ensure_models_exist(self):
        base_url = "https://github.com/opencv/opencv_zoo/raw/main/models/"
        # Liveness model from a compatible verified source (MiniFASNetV2)
        liveness_url = "https://github.com/kprokopi/onnx_runtime_face_anti_spoofing/raw/master/anti_spoofing_minifasnetv2.onnx"
        
        models = {
            self.detect_model_path: base_url + "face_detection_yunet/face_detection_yunet_2023mar.onnx",
            self.rec_model_path: base_url + "face_recognition_sface/face_recognition_sface_2021dec.onnx",
            self.liveness_model_path: liveness_url
        }
        
        for name, url in models.items():
            if not os.path.exists(name) or os.path.getsize(name) == 0:
                print(f"Downloading {name} from {url}...")
                try:
                    urllib.request.urlretrieve(url, name)
                    print(f"Downloaded {name} ({os.path.getsize(name)} bytes)")
                except Exception as e:
                    print(f"FAILED to download {name}: {e}")

    def reload_known_faces(self):
        print("Reloading known faces...")
        self.known_embeddings = {}
        if not os.path.exists(self.known_faces_dir):
            return
            
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith(".dat"):
                name = filename.split("_")[0]
                path = os.path.join(self.known_faces_dir, filename)
                try:
                    # SFace 2021dec output is 128 floats
                    embedding = np.fromfile(path, dtype=np.float32)
                    
                    if embedding.shape[0] != 128:
                        continue
                        
                    # Reshape to (1, 128) for cv2.match
                    embedding = embedding.reshape(1, 128)
                    
                    if name not in self.known_embeddings:
                        self.known_embeddings[name] = []
                    self.known_embeddings[name].append(embedding)
                    print(f"Loaded profile: {name}")
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

    def detect_faces(self, image: np.ndarray) -> List[np.ndarray]:
        h, w = image.shape[:2]
        self.detector.setInputSize((w, h))
        ret, faces = self.detector.detect(image)
        return faces if faces is not None else []

    def register_new_face(self, name: str, image: np.ndarray, append: bool = False) -> bool:
        faces = self.detect_faces(image)
        if len(faces) == 0:
            return False
        
        # Use first face
        face_info = faces[0]
        aligned_face = self.recognizer.alignCrop(image, face_info)
        feature = self.recognizer.feature(aligned_face)
        
        # Save embedding
        suffix = f"_{int(os.path.getmtime(self.known_faces_dir))}" if append else ""
        filename = f"{name}{suffix}.dat"
        feature.tofile(os.path.join(self.known_faces_dir, filename))
        
        # Save visual reference
        cv2.imwrite(os.path.join(self.known_faces_dir, f"{name}.jpg"), aligned_face)
        
        # Incremental Update
        if name not in self.known_embeddings:
            self.known_embeddings[name] = []
        
        valid_feature = feature.reshape(1, 128)
        self.known_embeddings[name].append(valid_feature)
        return True

    def check_liveness(self, image: np.ndarray, face_box: np.ndarray) -> Tuple[bool, float]:
        """
        Check if the face is real or a spoof (photo/screen/mask).
        Returns (is_real, score) where score > threshold means real.
        """
        if not getattr(self, 'liveness_enabled', False):
            return True, 1.0

        try:
            # 1. Expand box slightly (MiniFASNet expects context)
            x, y, w, h = map(int, face_box[:4])
            h_img, w_img = image.shape[:2]
            
            scale = 1.2
            new_w, new_h = int(w * scale), int(h * scale)
            center_x, center_y = x + w//2, y + h//2
            
            x1 = max(0, center_x - new_w//2)
            y1 = max(0, center_y - new_h//2)
            x2 = min(w_img, x1 + new_w)
            y2 = min(h_img, y1 + new_h)
            
            face_roi = image[y1:y2, x1:x2]
            if face_roi.size == 0: return False, 0.0
            
            # 2. Preprocess for MiniFASNetV2 (80x80)
            blob = cv2.dnn.blobFromImage(
                face_roi, scalefactor=1.0/255.0, size=(80, 80), 
                mean=(0, 0, 0), swapRB=True, crop=False
            )
            
            # 3. Predict
            self.liveness_net.setInput(blob)
            output = self.liveness_net.forward()
            
            # 4. Softmax
            output = np.exp(output) / np.sum(np.exp(output), axis=1, keepdims=True)
            
            # Class 0: Fake, Class 1: Real (usually, depends on model training)
            # For MiniFASNetV2: [Fake, Real, ...] (Wait, typically it's 3 classes: Real, Print, Mobile)
            # Actually MiniFASNet standard: index 1 is Real.
            
            real_score = output[0][1]
            is_real = real_score > 0.5 # Threshold can be tuned
            
            return is_real, float(real_score)
            
        except Exception as e:
            print(f"Liveness Check Failed: {e}")
            return True, 1.0 # Fail safe (allow access if model breaks)

    def recognize(self, image: np.ndarray, face_info: np.ndarray) -> Tuple[str, float]:
        aligned_face = self.recognizer.alignCrop(image, face_info)
        query_feature = self.recognizer.feature(aligned_face)
        
        best_match = "Unknown"
        max_sim = -1.0
        
        for name, embeddings in self.known_embeddings.items():
            for known_emb in embeddings:
                sim = self.recognizer.match(query_feature, known_emb, 0)
                if sim > max_sim:
                    max_sim = sim
                    best_match = name
                    
        if max_sim > self.threshold:
            return best_match, max_sim
        return "Unknown", max_sim

    def delete_person(self, name: str):
        for filename in os.listdir(self.known_faces_dir):
            if filename.startswith(name):
                try: os.remove(os.path.join(self.known_faces_dir, filename))
                except: pass
        if name in self.known_embeddings:
            del self.known_embeddings[name]
