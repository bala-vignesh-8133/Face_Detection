"""
Camera Port Scanner
Checks all camera indices (0-10) to find available cameras on your system.
"""
import cv2

def check_cameras():
    print("=" * 50)
    print("CAMERA PORT SCANNER")
    print("=" * 50)
    print("Scanning camera indices 0 to 10...\n")
    
    available_cameras = []
    
    for index in range(11):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                backend = cap.getBackendName()
                
                print(f"✅ INDEX {index}: WORKING")
                print(f"   Resolution: {width}x{height}")
                print(f"   FPS: {fps}")
                print(f"   Backend: {backend}")
                print()
                
                available_cameras.append({
                    'index': index,
                    'resolution': f"{width}x{height}",
                    'fps': fps,
                    'backend': backend
                })
            else:
                print(f"❌ INDEX {index}: Opens but cannot read frames")
            cap.release()
        else:
            print(f"❌ INDEX {index}: Not available")
    
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    if available_cameras:
        print(f"\nFound {len(available_cameras)} working camera(s):\n")
        for cam in available_cameras:
            print(f"  • Index {cam['index']}: {cam['resolution']} @ {cam['fps']} FPS ({cam['backend']})")
        
        print(f"\n💡 RECOMMENDATION: Use index {available_cameras[0]['index']} in camera_thread.py")
        print(f"   Edit line 25: self.cap = cv2.VideoCapture({available_cameras[0]['index']})")
    else:
        print("\n⚠️  No working cameras found!")
        print("    Make sure your external webcam is properly connected.")
    
    print()
    return available_cameras

if __name__ == "__main__":
    check_cameras()
