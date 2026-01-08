# One-Shot Face Recognition System bala

A face recognition system using the **Matrix/Vector Distance method** with 128-dimensional embedding vectors and Euclidean distance calculations.

## 📋 Overview

This system implements face recognition using:
- **Feature Extraction**: Converting W×H×3 pixel matrices into 1×128 vectors using a pre-trained deep learning model
- **Distance Calculation**: Computing d = ||v_known - v_query|| (L2 norm / Euclidean Distance)
- **Thresholding**: Boolean matching with `is_match = distance < 0.6`

## 🎯 Technical Details

| Operation | Technical Detail |
|-----------|-----------------|
| **Feature Extraction** | W×H×3 pixel matrix → 1×128 embedding vector |
| **Distance Calculation** | d = \|\|v_known - v_query\|\| (Euclidean Distance) |
| **Thresholding** | is_match = distance < 0.6 |

## 📁 Project Structure

```
face/
├── known_faces/          # Reference photos (training set)
│   ├── person1.jpg
│   ├── person2.jpg
│   └── ...
├── query_faces/          # Images to be identified (test set)
│   ├── test1.jpg
│   ├── test2.jpg
│   └── ...
├── face_recognition_system.py  # Main recognition system
├── test_run.py                 # Test script with logging
├── recognition_log.txt         # Auto-generated log file
└── README.md
```

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- CMake (required for dlib compilation)

### Install Dependencies

Run the following command to install required packages for the lightweight version (working immediately):

```bash
pip install numpy opencv-contrib-python
```

**Note**: Installing `dlib` may take several minutes as it requires compilation. Ensure you have a C++ compiler installed on your system.

### Package Details
- `cmake`: Build system for dlib
- `dlib`: Machine learning toolkit with face detection
- `face_recognition`: High-level face recognition library built on dlib
- `numpy`: Numerical computing for vector operations
- `opencv-python`: Computer vision library for image processing

## 💡 Usage

### Step 1: Prepare Known Faces (Done automatically in demo)

We have already generated sample images for "Alice" and "Bob" in the `known_faces/` directory.

You can add more:
- Use clear, front-facing photos
- One face per image
- Filename (without extension) will be used as the person's name
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`

Example:
```
known_faces/
├── john_doe.jpg
├── jane_smith.jpg
└── alice_brown.jpg
```

### Step 2: Prepare Query Images

Add images to identify to the `query_faces/` directory:
- Same format requirements as known faces
- Can contain unknown people

Example:
```
query_faces/
├── test_photo1.jpg
├── test_photo2.jpg
└── unknown_person.jpg
```

### Step 3: Run Recognition

#### Option A: Run Test Script (Recommended)
```bash
python test_run.py
```

This will:
- Load all known faces
- Process all query images
- Calculate and display distance matrices  
- Log all results to `recognition_log.txt`
- Print a comprehensive summary

#### Option B: Run Main System
```bash
python face_recognition_system.py
```

This will process all query images and display results in the console.

#### Option C: Use as a Module

```python
from face_recognition_system import FaceRecognitionSystem

# Initialize system
system = FaceRecognitionSystem(known_faces_dir="known_faces", threshold=0.6)

# Recognize a face
name, distance = system.recognize_face("query_faces/test.jpg", log_distances=True)
print(f"Identified: {name} (distance: {distance:.4f})")

# Recognize and create annotated image
system.recognize_and_annotate("query_faces/test.jpg", output_path="result.jpg")
```

## 🔬 How It Works

### 1. Feature Extraction
Each face image is converted into a 128-dimensional vector:
```python
# Input: W×H×3 RGB image
image = face_recognition.load_image_file("person.jpg")

# Output: 1×128 embedding vector
encoding = face_recognition.face_encodings(image)[0]
```

### 2. Distance Calculation
The Euclidean distance between vectors is calculated:
```python
def calculate_euclidean_distance(v1, v2):
    # L2 norm: d = sqrt(Σ(v1[i] - v2[i])²)
    return np.linalg.norm(v1 - v2)
```

### 3. Matching Decision
A face is recognized if the distance is below the threshold:
```python
is_match = distance < 0.6  # Threshold: 0.6
result = best_match_name if is_match else "Unknown"
```

## 📊 Understanding the Output

### Console Output Example
```
==============================================================
🔍 Recognizing Face from: test1.jpg
==============================================================

📸 Processing: test1.jpg
✅ Vector extracted (shape: (128,))

📊 Distance Matrix Calculations:
--------------------------------------------------------------
  d(query, john_doe      ) = 0.3542
  d(query, jane_smith    ) = 0.7821
  d(query, alice_brown   ) = 0.9134
--------------------------------------------------------------

🎯 Best Match: john_doe
📏 Distance: 0.3542
🎚️  Threshold: 0.6
✅ Match Status: RECOGNIZED
==============================================================
```

### Log File Format
The `recognition_log.txt` file contains:
- Timestamp of test run
- List of loaded known faces
- Distance calculations for each query
- Final results and summary statistics

## 🎛️ Configuration

### Adjusting the Threshold

The default threshold is `0.6`. You can adjust it based on your needs:

```python
# More strict (fewer false positives, more false negatives)
system = FaceRecognitionSystem(threshold=0.4)

# More lenient (more false positives, fewer false negatives)
system = FaceRecognitionSystem(threshold=0.7)
```

**Recommended values:**
- `0.4` - Very strict, use for high-security applications
- `0.6` - Balanced (default), good for most use cases
- `0.8` - Lenient, use when you want to minimize "Unknown" results

## 🧪 Testing

To test the system:

1. Add at least 2-3 photos to `known_faces/`
2. Add test photos to `query_faces/` (some matching, some not)
3. Run: `python test_run.py`
4. Check `recognition_log.txt` for detailed results

## 📝 Example Workflow

```bash
# 1. Install dependencies
pip install cmake dlib face_recognition numpy opencv-python

# 2. Add reference photos
# Copy photos to known_faces/

# 3. Add test photos
# Copy photos to query_faces/

# 4. Run the test
python test_run.py

# 5. Check results
# View console output and recognition_log.txt
```

## 🔍 Troubleshooting

### "No face detected in image"
- Ensure the photo has a clear, visible face
- Face should be front-facing
- Image should have good lighting
- Try a different photo

### "Multiple faces detected"
- The system uses the first detected face
- For best results, use images with only one face

### CMake/dlib installation fails
- **Windows**: Install Visual Studio Build Tools
- **Mac**: Install Xcode Command Line Tools: `xcode-select --install`
- **Linux**: Install build essentials: `sudo apt-get install build-essential cmake`

### High distances for known people
- Check photo quality (resolution, lighting)
- Ensure photos are front-facing
- Try adjusting the threshold
- Use multiple photos of the same person

## 📚 Mathematical Background

### Embedding Vector
The 128D vector represents facial features in a high-dimensional space where:
- Similar faces are close together
- Different faces are far apart

### Euclidean Distance (L2 Norm)
$$d = \sqrt{\sum_{i=1}^{128} (v_{known}[i] - v_{query}[i])^2}$$

Or equivalently:
$$d = \| \mathbf{v}_{known} - \mathbf{v}_{query} \|_2$$

### Decision Boundary
The threshold creates a hypersphere in 128D space:
- Inside sphere (d < 0.6): Same person
- Outside sphere (d ≥ 0.6): Different person

## 🎓 Credits

This system uses:
- **dlib**: Pre-trained face recognition model (ResNet-based)
- **face_recognition**: Simplified API for face recognition
- **Distance metric**: Euclidean distance in 128D embedding space

## 📄 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Feel free to improve the system by:
- Adding multiple face support
- Implementing different distance metrics (cosine similarity, etc.)
- Adding real-time video recognition
- Creating a GUI interface

---

**Note**: The accuracy of this system depends on the quality of the input images and the appropriateness of the threshold value for your specific use case.
