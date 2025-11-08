
# test_detector.py - Test the exported detector
from streamlit_detector import StreamlitSSDDetector

print("Testing exported detector...")
detector = StreamlitSSDDetector(confidence_threshold=0.3)

if detector.load_model():
    print("✅ Export successful! Detector is working.")
else:
    print("❌ Export failed! Check your internet connection.")
