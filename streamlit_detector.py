
import os
import numpy as np
import cv2
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import time

class StreamlitSSDDetector:
    """Simplified SSD detector for Streamlit UI"""
    
    def __init__(self, confidence_threshold=0.5):
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.model_loaded = False
        self.load_classes()
        print("🔄 Detector initialized. Call load_model() to load the AI model.")
        
    def load_model(self):
        """Load pre-trained model"""
        try:
            print("🔄 Loading SSD MobileNet model from TensorFlow Hub...")
            model_url = "https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2"
            self.model = hub.load(model_url)
            self.model_loaded = True
            print("✅ Model loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Model loading failed: {e}")
            self.model_loaded = False
            return False
    
    def load_classes(self):
        """Load COCO class names"""
        self.class_names = [
            'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
            'train', 'truck', 'boat', 'traffic light', 'fire hydrant',
            'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog',
            'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
            'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
            'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat',
            'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
            'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
            'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot',
            'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
            'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
            'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
            'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
            'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ]
        print(f"📚 Loaded {len(self.class_names)} object classes")
    
    def detect_objects(self, image):
        """Detect objects in image"""
        if not self.model_loaded:
            print("⚠️ Model not loaded. Call load_model() first.")
            return []
            
        try:
            # Preprocess image
            if isinstance(image, np.ndarray):
                if len(image.shape) == 3 and image.shape[2] == 3:
                    # Convert BGR to RGB if needed
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                else:
                    image_rgb = image
            else:
                image_rgb = np.array(image)
                
            # Resize to model input size
            image_resized = cv2.resize(image_rgb, (300, 300))
            input_tensor = tf.convert_to_tensor(np.expand_dims(image_resized, axis=0), dtype=tf.uint8)
            
            # Run detection
            detections = self.model(input_tensor)
            
            # Process results
            results = []
            boxes = detections['detection_boxes'][0].numpy()
            classes = detections['detection_classes'][0].numpy().astype(int)
            scores = detections['detection_scores'][0].numpy()
            
            height, width = image_rgb.shape[:2]
            
            for i in range(len(scores)):
                if scores[i] > self.confidence_threshold:
                    class_id = classes[i]
                    if 1 <= class_id <= len(self.class_names):
                        class_name = self.class_names[class_id - 1]
                        
                        # Convert normalized coordinates to pixel coordinates
                        y1, x1, y2, x2 = boxes[i]
                        x1 = int(max(0, min(x1 * width, width-1)))
                        y1 = int(max(0, min(y1 * height, height-1)))
                        x2 = int(max(0, min(x2 * width, width-1)))
                        y2 = int(max(0, min(y2 * height, height-1)))
                        
                        results.append({
                            'class_name': class_name,
                            'confidence': float(scores[i]),
                            'bbox': [x1, y1, x2, y2]
                        })
            
            return results
            
        except Exception as e:
            print(f"❌ Detection error: {e}")
            return []
    
    def draw_detections(self, image, detections):
        """Draw bounding boxes on image"""
        result_image = image.copy()
        
        # Generate colors for classes
        np.random.seed(42)
        colors = {}
        
        for detection in detections:
            bbox = detection['bbox']
            class_name = detection['class_name']
            confidence = detection['confidence']
            
            # Get or generate color for this class
            if class_name not in colors:
                colors[class_name] = tuple(map(int, np.random.randint(0, 255, 3)))
            color = colors[class_name]
            
            # Draw bounding box
            cv2.rectangle(result_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            
            # Draw label background
            label = f"{class_name}: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.rectangle(result_image, 
                         (bbox[0], bbox[1] - label_size[1] - 10),
                         (bbox[0] + label_size[0], bbox[1]), 
                         color, -1)
            
            # Draw label text
            cv2.putText(result_image, label, (bbox[0], bbox[1] - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        return result_image

# Test function for verification
def test_detector():
    """Test the detector with a sample"""
    print("🧪 Testing detector...")
    detector = StreamlitSSDDetector(confidence_threshold=0.3)
    
    if detector.load_model():
        print("✅ Detector is ready for export!")
        return True
    else:
        print("❌ Detector test failed!")
        return False

if __name__ == "__main__":
    test_detector()
