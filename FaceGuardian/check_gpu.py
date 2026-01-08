import cv2
import sys

print(f"OpenCV Version: {cv2.__version__}")
try:
    count = cv2.cuda.getCudaEnabledDeviceCount()
    print(f"CUDA Enabled Devices: {count}")
except Exception as e:
    print(f"CUDA Check Failed: {e}")

print("\nBuild Information:")
print(cv2.getBuildInformation())
