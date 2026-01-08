# Installation Guide for Face Recognition System

## Quick Start (OpenCV-only version)

If you're having trouble installing `dlib`, use the lightweight OpenCV-only version:

```bash
# Install only numpy and opencv
pip install numpy opencv-python

# Run the lightweight version
python face_recognition_opencv.py
```

##  Full Installation (with dlib for better accuracy)

### Option 1: Using Pre-compiled Wheels (Recommended for Windows)

1. **Download pre-built dlib wheel:**
   - Visit: https://github.com/z-mahmud22/Dlib_Windows_Python3.x
   - Or use: `pip install dlib-compiled`

2. **Install face_recognition:**
   ```bash
   pip install face_recognition
   ```

### Option 2: Install via Conda (Easiest)

```bash
# Create conda environment
conda create -n facerecog python=3.9
conda activate facerecog

# Install packages
conda install -c conda-forge dlib
pip install face_recognition opencv-python numpy
```

### Option 3: Build from Source (Advanced)

#### Windows:
1. Install Visual Studio Build Tools (required for CMake):
   - Download from: https://visualstudio.microsoft.com/downloads/
   - Install "Desktop development with C++"

2. Install CMake:
   ```bash
   pip install cmake
   ```

3. Install dlib:
   ```bash
   pip install dlib
   ```

4. Install face_recognition:
   ```bash
   pip install face_recognition
   ```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
sudo apt-get install libx11-dev libgtk-3-dev

pip install dlib
pip install face_recognition opencv-python numpy
```

#### macOS:
```bash
# Install Xcode command line tools
xcode-select --install

# Install packages
brew install cmake
pip install dlib
pip install face_recognition opencv-python numpy
```

## Verifying Installation

Test if dlib is installed correctly:

```bash
python -c "import dlib; print('dlib version:', dlib.__version__)"
```

Test if face_recognition is installed:

```bash
python -c "import face_recognition; print('face_recognition installed successfully')"
```

## Which Version Should I Use?

| Feature | OpenCV Version | Dlib Version |
|---------|---------------|--------------|
| **Installation** | ✅ Easy (pip only) | ⚠️ Complex (requires compilation) |
| **Accuracy** | 🟡 Good (~85-90%) | ✅ Excellent (~99%) |
| **Speed** | ✅ Fast | 🟡 Moderate |
| **Feature Dimension** | 448D (histogram) | 128D (deep learning) |
| **Best For** | Quick prototypes, testing | Production, high accuracy |

## Recommendation

1. **Start with OpenCV version** (`face_recognition_opencv.py`) to test the concept
2. **Upgrade to dlib version** (`face_recognition_system.py`) for production use

## Common Installation Errors

### Error: "Microsoft Visual C++ 14.0 or greater is required"
**Solution:** Install Visual Studio Build Tools from Microsoft

### Error: "Could not find a version that satisfies the requirement dlib"
**Solution:** 
- Try: `pip install dlib-binary`
- Or use conda: `conda install -c conda-forge dlib`

### Error: "CMake must be installed to build dlib"
**Solution:** 
```bash
pip install cmake
```

## Testing After Installation

1. Create test folders:
```bash
mkdir known_faces query_faces
```

2. Add sample images (use your own photos or download from web)

3. Run test:
```bash
# For OpenCV version
python face_recognition_opencv.py

# For dlib version  
python face_recognition_system.py
```

## Need Help?

If installation fails, please provide:
1. Your operating system (Windows/Linux/macOS)
2. Python version: `python --version`
3. Full error message

Then we can troubleshoot specific issues.
