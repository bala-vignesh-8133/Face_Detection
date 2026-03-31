import cv2
import mediapipe as mp
# Import solutions directly to avoid "no attribute 'solutions'" error on some platforms
import mediapipe.python.solutions.face_mesh as mp_face_mesh
import numpy as np
import os

# Define key landmark indices for MediaPipe
LEFT_EYE = 33
RIGHT_EYE = 263
NOSE_TIP = 1
CHIN = 152
FOREHEAD = 10 
LEFT_JAW = 234
RIGHT_JAW = 454

def get_face_landmarks_from_image(image_rgb):
    """Extracts X,Y coordinates of the 468 face landmarks from an RGB image array."""
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as face_mesh:
        results = face_mesh.process(image_rgb)
        if not results.multi_face_landmarks:
            return None
        
        # Get coordinates relative to image size
        h, w, _ = image_rgb.shape
        landmarks = []
        for lm in results.multi_face_landmarks[0].landmark:
            landmarks.append([lm.x * w, lm.y * h])
            
        return np.array(landmarks)

def calculate_age_confidence(known_image_path, query_image_rgb, assumed_years_aged=5):
    """
    Assesses how closely the known child's features match the query candidate's features
    after applying an algorithmic aging progression.
    Returns: (confidence_score (0.0 to 100.0), explanation_string)
    """
    if not os.path.exists(known_image_path):
        return 0.0, "Reference image not found."

    known_image = cv2.imread(known_image_path)
    if known_image is None:
        return 0.0, "Could not read reference image."
        
    known_image_rgb = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)
    
    child_pts = get_face_landmarks_from_image(known_image_rgb)
    candidate_pts = get_face_landmarks_from_image(query_image_rgb)
    
    if child_pts is None or candidate_pts is None:
        return 0.0, "Face landmarks not fully visible in one or both images."

    # 1. Normalize both faces using the Interpupillary Distance (IPD)
    child_ipd = np.linalg.norm((child_pts[LEFT_EYE] - child_pts[RIGHT_EYE]).astype(float))
    candidate_ipd = np.linalg.norm((candidate_pts[LEFT_EYE] - candidate_pts[RIGHT_EYE]).astype(float))
    
    if child_ipd == 0 or candidate_ipd == 0:
        return 0.0, "Eye landmarks overlapping."

    scale_factor = candidate_ipd / child_ipd
    scaled_child_pts = child_pts * scale_factor

    # 2. Extract specific ratios that change with age
    def get_aspect_ratio(pts):
        height = np.linalg.norm(pts[FOREHEAD] - pts[CHIN])
        width = np.linalg.norm(pts[LEFT_JAW] - pts[RIGHT_JAW])
        return height / width if width > 0 else 0
        
    def get_nose_ratio(pts):
        nose_len = np.linalg.norm(pts[NOSE_TIP] - ((pts[LEFT_EYE] + pts[RIGHT_EYE])/2))
        height = np.linalg.norm(pts[FOREHEAD] - pts[CHIN])
        return nose_len / height if height > 0 else 0

    child_ratio = get_aspect_ratio(scaled_child_pts)
    child_nose = get_nose_ratio(scaled_child_pts)
    
    candidate_ratio = get_aspect_ratio(candidate_pts)
    candidate_nose = get_nose_ratio(candidate_pts)
    
    # 3. Apply the "Biological Aging Math"
    # Elongation ~1.5% per year, Nose growth ~0.5% per year
    elongation_per_year = 0.015 
    predicted_ratio = child_ratio + (elongation_per_year * assumed_years_aged)
    
    nose_growth_per_year = 0.005
    predicted_nose = child_nose + (nose_growth_per_year * assumed_years_aged)

    # 4. Calculate Confidence Score
    ratio_error = abs(predicted_ratio - candidate_ratio) / (candidate_ratio + 1e-6)
    nose_error = abs(predicted_nose - candidate_nose) / (candidate_nose + 1e-6)
    
    total_error = (ratio_error * 0.6) + (nose_error * 0.4) 
    
    # Convert to a 0-100% confidence score
    confidence = max(0.0, min(100.0, 100 - (total_error * 1000)))
    
    explanation = f"Age Progressed Analysis (Est. +{assumed_years_aged} yrs) Confidence: {confidence:.1f}%"
    return confidence, explanation
