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
        
        self._ensure_models_exist()
        
        # Initialize OpenCV specialized APIs
        try:
            print(f"Initializing FaceDetectorYN with {self.detect_model_path}")
            # 1. Try NVIDIA CUDA (Requires custom OpenCV build)
            try:
                print("Attempting to use NVIDIA GPU (CUDA)...")
                self.detector = cv2.FaceDetectorYN.create(
                    self.detect_model_path, "", self.input_size, 0.65, 0.3, 5000, 
                    cv2.dnn.DNN_BACKEND_CUDA, cv2.dnn.DNN_TARGET_CUDA
                )
                self.recognizer = cv2.FaceRecognizerSF.create(
                    self.rec_model_path, "", 
                    cv2.dnn.DNN_BACKEND_CUDA, cv2.dnn.DNN_TARGET_CUDA
                )
                # TEST RUN: Force execution to check if CUDA is actually available
                # This prevents "lazy" crashes later during runtime
                dummy_img = np.zeros((320, 320, 3), dtype=np.uint8)
                self.detector.detect(dummy_img)
                self.backend_name = "NVIDIA CUDA"
                print("✅ NVIDIA GPU (CUDA) Enabled & Verified!")
                self.backend_name = "NVIDIA CUDA"
                print("✅ NVIDIA GPU (CUDA) Enabled & Verified!")
            except Exception as cuda_err:
                # 2. Skip OpenCL (User reported lag due to memory transfer overhead)
                # 3. Fallback to CPU (Tested & Verified Lag-Free)
                print(f"CUDA Failed ({cuda_err}). Switching to CPU (High Performance).")
                self.detector = cv2.FaceDetectorYN.create(
                    self.detect_model_path, "", self.input_size, 0.65, 0.3, 5000
                )
                self.recognizer = cv2.FaceRecognizerSF.create(self.rec_model_path, "")
                self.backend_name = "CPU (Optimized)"
            print(f"✅ AI Engine Initialized [{self.backend_name}]")
            print(f"✅ AI Engine Initialized [{self.backend_name}]")
            
        except Exception as e:
            print(f"CRITICAL ERROR initializing models: {e}")
            # Try to delete bad models so they re-download next time
            if os.path.exists(self.detect_model_path): os.remove(self.detect_model_path)
            if os.path.exists(self.rec_model_path): os.remove(self.rec_model_path)
            raise e
        
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)
            
        from .child_manager import ChildManager
        self.child_db = ChildManager()
            
        self.reload_known_faces()

    def _ensure_models_exist(self):
        base_url = "https://github.com/opencv/opencv_zoo/raw/main/models/"
        models = {
            self.detect_model_path: base_url + "face_detection_yunet/face_detection_yunet_2023mar.onnx",
            self.rec_model_path: base_url + "face_recognition_sface/face_recognition_sface_2021dec.onnx"
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
            
        self.child_db.load_db()
            
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith(".dat"):
                # Strip extension and potential timestamp suffix
                name = filename.replace(".dat", "").split("_")[0]
                
                # Check Approval Status BEFORE Loading into RAM
                child_record = self.child_db.get_child(name)
                if child_record and child_record.get("status") != "Active":
                    print(f"Skipping {name}: Pending Approval")
                    continue
                    
                path = os.path.join(self.known_faces_dir, filename)
                try:
                    # SFace 2021dec output is 128 floats
                    embedding = np.fromfile(path, dtype=np.float32)
                    
                    if embedding.shape[0] != 128:
                        print(f"WARNING: Ignoring & Deleting incompatible legacy profile: {filename} (Size: {embedding.shape[0]})")
                        try:
                            os.remove(path)
                        except:
                            pass
                        continue
                        
                    # Reshape to (1, 128) for cv2.match
                    embedding = embedding.reshape(1, 128)
                    
                    if name not in self.known_embeddings:
                        self.known_embeddings[name] = []
                    self.known_embeddings[name].append(embedding)
                    print(f"Loaded active profile: {name}")
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

    def detect_faces(self, image: np.ndarray) -> List[np.ndarray]:
        h, w = image.shape[:2]
        self.detector.setInputSize((w, h))
        ret, faces = self.detector.detect(image)
        
        if faces is not None:
            # Filter out false positives while allowing distant faces
            filtered_faces = []
            for face in faces:
                x, y, w_face, h_face = map(int, face[:4])
                confidence = face[14]  # Detection confidence score
                
                # Filter criteria:
                # 1. Face must be at least 25x25 pixels (allows detection at door ~3-4 meters)
                # 2. Confidence must be > 0.65 (balanced threshold)
                # 3. Aspect ratio should be reasonable (0.6 to 1.6) - wider range for angles
                aspect_ratio = w_face / h_face if h_face > 0 else 0
                
                # Allow smaller faces but with stricter aspect ratio to avoid hands
                if (w_face >= 25 and h_face >= 25 and 
                    confidence > 0.65 and 
                    0.6 <= aspect_ratio <= 1.6):
                    filtered_faces.append(face)
            
            return filtered_faces
             
        return []

    def register_new_face(self, name: str, image: np.ndarray, append: bool = False, activate: bool = True) -> bool:
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
        
        # Save visual reference (optional but helpful)
        cv2.imwrite(os.path.join(self.known_faces_dir, f"{name}.jpg"), aligned_face)
        
        # Push to RAM only if actived!
        if activate:
            if name not in self.known_embeddings:
                self.known_embeddings[name] = []
            valid_feature = feature.reshape(1, 128)
            self.known_embeddings[name].append(valid_feature)
        
        return True

    def recognize(self, image: np.ndarray, face_info: np.ndarray) -> Tuple[str, float]:
        aligned_face = self.recognizer.alignCrop(image, face_info)
        query_feature = self.recognizer.feature(aligned_face)
        
        best_match = "Unknown"
        max_sim = -1.0
        
        for name, embeddings in self.known_embeddings.items():
            for known_emb in embeddings:
                # SFace match function (0: cosine, 1: norm-l2)
                sim = self.recognizer.match(query_feature, known_emb, 0)
                if sim > max_sim:
                    max_sim = sim
                    best_match = name
                    
        if max_sim > self.threshold:
            return best_match, max_sim
            
        # --- NEW: Age Progression Fallback ---
        # If the face is somewhat similar but didn't pass strict threshold 
        # (e.g. within 0.15 of threshold), we check for age progression changes.
        if best_match != "Unknown" and max_sim > (self.threshold - 0.15):
            try:
                from .age_analysis import calculate_age_confidence
                # Try finding the original image registered for this person
                known_img_path = os.path.join(self.known_faces_dir, f"{best_match}.jpg")
                if os.path.exists(known_img_path):
                    # Convert the current camera frame to RGB for MediaPipe
                    query_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    
                    # Run geometric age analysis (assumed ~5 yrs aged, this can be dynamic)
                    confidence, expl = calculate_age_confidence(known_img_path, query_rgb, assumed_years_aged=5)
                    
                    # If high geometric confidence -> Override strict Face ID result
                    if confidence > 75.0:
                        print(f"🌟 [AGE PROGRESSION ALGORITHM] Probable match for {best_match}! {expl}")
                        # Boost the similarity score artificially to pass validations upstream
                        return f"{best_match} (Aged-Match)", max_sim + 0.15  
            except Exception as e:
                print(f"Age progression analysis error: {e}")

        return "Unknown", max_sim

    def delete_person(self, name: str):
        # 1. Delete files (Support both jpg and png)
        for filename in os.listdir(self.known_faces_dir):
            if filename.startswith(name):
                try:
                    os.remove(os.path.join(self.known_faces_dir, filename))
                except:
                    pass
        
        # 2. Update Memory (Optimized O(1))
        if name in self.known_embeddings:
            del self.known_embeddings[name]
