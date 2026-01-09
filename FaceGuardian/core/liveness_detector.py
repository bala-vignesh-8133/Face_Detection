import cv2
import numpy as np

class LivenessDetector:
    """
    Anti-spoofing module - TEMPORARILY DISABLED
    Will be re-implemented with better algorithm
    """
    
    def __init__(self):
        self.debug = False
        
    def check_liveness(self, frame, face_box):
        """
        TEMPORARILY DISABLED - Always returns True
        
        The current implementation has too many false positives.
        Will be re-implemented with a more sophisticated approach.
        
        Args:
            frame: Full camera frame (BGR)
            face_box: (x, y, w, h) bounding box of face
            
        Returns:
            (is_live: bool, confidence: float, reason: str)
        """
        # DISABLED: Always pass liveness check
        return True, 1.0, "Liveness check disabled"
        
    def check_liveness(self, frame, face_box):
        """
        Analyze if the detected face is real or a photo/screen.
        PRIMARY FOCUS: Detect screen glare and photo artifacts.
        
        Args:
            frame: Full camera frame (BGR)
            face_box: (x, y, w, h) bounding box of face
            
        Returns:
            (is_live: bool, confidence: float, reason: str)
        """
        x, y, w, h = face_box
        
        # Extract face region with padding
        pad = 10
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(frame.shape[1], x + w + pad)
        y2 = min(frame.shape[0], y + h + pad)
        
        face_region = frame[y1:y2, x1:x2]
        
        if face_region.size == 0:
            return True, 1.0, "Live (default)"  # Default to live if can't analyze
        
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
        
        # PRIMARY TEST: Screen Reflection Detection (most reliable)
        reflection_score = self._detect_screen_reflection(face_region)
        
        # SECONDARY TESTS: Only used if reflection test is inconclusive
        texture_score = self._analyze_texture(gray)
        edge_score = self._analyze_edge_sharpness(gray)
        
        # If screen glare is detected, it's definitely a spoof
        if reflection_score < 0.4:
            is_live = False
            liveness_score = reflection_score
            reason = "Screen glare detected"
        else:
            # No obvious screen - check texture and edges
            # Be LENIENT - only reject if BOTH are very low
            if texture_score < 0.3 and edge_score < 0.3:
                is_live = False
                liveness_score = (texture_score + edge_score) / 2
                reason = "Flat photo detected"
            else:
                # Likely real face
                is_live = True
                liveness_score = max(reflection_score, texture_score, edge_score)
                reason = "Live face verified"
        
        # Debug logging
        if self.debug:
            print(f"[LIVENESS] Reflection:{reflection_score:.2f} Texture:{texture_score:.2f} Edge:{edge_score:.2f} => Live:{is_live} ({reason})")
        
        return is_live, liveness_score, reason
    
    def _detect_screen_reflection(self, face_bgr):
        """
        PRIMARY TEST: Detect screen reflections/glare.
        Phone/monitor screens have characteristic bright spots and uniform lighting.
        """
        gray = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2GRAY)
        
        # Test 1: Very bright pixels (screen glare)
        _, bright_mask = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
        bright_ratio = np.count_nonzero(bright_mask) / bright_mask.size
        
        # Test 2: Uniform brightness (screens have flat lighting)
        brightness_std = np.std(gray)
        
        # Screens have:
        # - High bright pixel ratio (>3% due to glare)
        # - Low brightness variance (<30 due to flat lighting)
        
        if bright_ratio > 0.08:
            # Definite screen glare
            return 0.1
        elif bright_ratio > 0.04 and brightness_std < 25:
            # Likely screen (bright + flat)
            return 0.3
        elif brightness_std < 20:
            # Very flat lighting (possible screen)
            return 0.5
        else:
            # Normal face lighting
            return 1.0
    
    def _analyze_texture(self, gray):
        """
        SECONDARY TEST: Texture analysis.
        Be LENIENT - only flag very flat textures.
        """
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        texture_variance = np.std(magnitude)
        
        # LENIENT thresholds:
        # Real faces: usually >15
        # Photos: usually <12
        if texture_variance > 15:
            return 1.0  # Good texture
        elif texture_variance > 10:
            return 0.6  # Acceptable
        else:
            return 0.2  # Very flat (likely photo)
    
    def _analyze_edge_sharpness(self, gray):
        """
        SECONDARY TEST: Edge analysis.
        Be LENIENT - only flag very unnatural edges.
        """
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.count_nonzero(edges) / edges.size
        
        # LENIENT thresholds:
        # Real faces: 0.04-0.18
        # Printed photos: often >0.22 (too sharp)
        # Low quality screens: <0.03 (too smooth)
        if 0.04 < edge_density < 0.20:
            return 1.0  # Normal edges
        elif edge_density > 0.22:
            return 0.3  # Too sharp (printed photo)
        elif edge_density < 0.02:
            return 0.3  # Too smooth (low quality screen)
        else:
            return 0.7  # Borderline acceptable
