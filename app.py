# app.py - Complete Streamlit Object Detection Application
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import os

# Import your detector
from streamlit_detector import StreamlitSSDDetector

# Page configuration
st.set_page_config(
    page_title="SSD Object Detection System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e88e5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .detection-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-left: 4px solid #4caf50;
        margin: 0.5rem 0;
    }
    .stProgress .st-bo {
        background-color: #1e88e5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize detector (cache it so it only loads once)
@st.cache_resource
def load_detector():
    """Load and cache the SSD detector"""
    with st.spinner('🔄 Loading AI model... This may take a moment.'):
        detector = StreamlitSSDDetector(confidence_threshold=0.5)
        success = detector.load_model()
        if success:
            st.success("✅ AI Model loaded successfully!")
        else:
            st.error("❌ Failed to load AI model. Check your internet connection.")
        return detector, success

def create_sample_images_folder():
    """Create sample images folder with instructions"""
    sample_folder = os.path.join(os.getcwd(), "sample_images")
    if not os.path.exists(sample_folder):
        os.makedirs(sample_folder)
        
        # Create a README file
        readme_content = """
# Sample Images

Place your test images in this folder for quick access in the app.

Supported formats: JPG, JPEG, PNG

Example images to test:
- Photos with people
- Street scenes with cars
- Indoor scenes with furniture
- Photos with animals
- Food images
"""
        with open(os.path.join(sample_folder, "README.md"), "w") as f:
            f.write(readme_content)
    
    return sample_folder

def main():
    # Header
    st.markdown('<h1 class="main-header">🔍 SSD Object Detection System</h1>', unsafe_allow_html=True)
    st.markdown("### Powered by SSD MobileNet v2 - Real-time AI Object Detection")
    
    # Sidebar configuration
    st.sidebar.header("🎛️ Detection Settings")
    
    # Load detector
    detector, model_loaded = load_detector()
    
    if not model_loaded:
        st.error("❌ Cannot proceed without loading the AI model. Please check your internet connection and refresh the page.")
        return
    
    # Confidence threshold slider
    confidence_threshold = st.sidebar.slider(
        "Confidence Threshold", 
        min_value=0.1, 
        max_value=1.0, 
        value=0.5, 
        step=0.05,
        help="Lower values detect more objects but may include false positives"
    )
    detector.confidence_threshold = confidence_threshold
    
    # Advanced settings
    with st.sidebar.expander("ℹ️ About This System"):
        st.write("""
        **SSD MobileNet v2 Features:**
        - 80 COCO object classes
        - Real-time detection
        - Lightweight architecture
        - Pre-trained on COCO dataset
        
        **Common Objects Detected:**
        - People, vehicles, animals
        - Furniture, electronics
        - Food items, sports equipment
        - And much more!
        """)
    
    # Create sample images folder
    sample_folder = create_sample_images_folder()
    
    # Main interface
    tab1, tab2, tab3 = st.tabs(["📷 Image Detection", "📊 Model Info", "🧪 Test Results"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📤 Upload Image")
            
            # File uploader
            uploaded_file = st.file_uploader(
                "Choose an image file", 
                type=['jpg', 'jpeg', 'png'],
                help="Upload JPG, JPEG, or PNG images for object detection"
            )
            
            # Option to use sample images
            sample_files = []
            if os.path.exists(sample_folder):
                sample_files = [f for f in os.listdir(sample_folder) 
                              if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            if sample_files:
                st.write("Or choose from sample images:")
                selected_sample = st.selectbox("Sample Images", ["None"] + sample_files)
                if selected_sample != "None":
                    uploaded_file = os.path.join(sample_folder, selected_sample)
            
            # Display original image
            if uploaded_file is not None:
                st.subheader("🖼️ Original Image")
                
                if isinstance(uploaded_file, str):  # Sample image path
                    image = Image.open(uploaded_file)
                    image_path = uploaded_file
                else:  # Uploaded file
                    image = Image.open(uploaded_file)
                    image_path = None
                
                st.image(image, use_column_width=True)
                
                # Image info
                with st.expander("📋 Image Information"):
                    st.write(f"**Dimensions:** {image.size[0]} x {image.size[1]} pixels")
                    st.write(f"**Mode:** {image.mode}")
                    if image_path:
                        file_size = os.path.getsize(image_path) / 1024  # KB
                        st.write(f"**File Size:** {file_size:.1f} KB")
        
        with col2:
            if uploaded_file is not None:
                st.subheader("🎯 Detection Results")
                
                # Convert PIL to OpenCV format
                image_array = np.array(image)
                if len(image_array.shape) == 3:
                    image_cv = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
                else:
                    image_cv = image_array
                
                # Detection progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Perform detection
                status_text.text("🔍 Analyzing image...")
                progress_bar.progress(25)
                
                start_time = time.time()
                detections = detector.detect_objects(image_cv)
                detection_time = time.time() - start_time
                
                progress_bar.progress(75)
                status_text.text("🎨 Drawing results...")
                
                if detections:
                    # Draw detections
                    result_image = detector.draw_detections(image_cv, detections)
                    result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Detection complete!")
                    
                    # Display result
                    st.image(result_image_rgb, use_column_width=True)
                    
                    # Clear progress
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Metrics
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Objects Found", len(detections))
                    with col_b:
                        st.metric("Detection Time", f"{detection_time:.2f}s")
                    with col_c:
                        avg_confidence = sum(d['confidence'] for d in detections) / len(detections)
                        st.metric("Avg Confidence", f"{avg_confidence:.2f}")
                    
                    # Detection details
                    st.subheader("📋 Detected Objects")
                    
                    # Group by class
                    class_counts = {}
                    for detection in detections:
                        class_name = detection['class_name']
                        if class_name in class_counts:
                            class_counts[class_name] += 1
                        else:
                            class_counts[class_name] = 1
                    
                    # Summary
                    st.write("**Object Summary:**")
                    for class_name, count in sorted(class_counts.items()):
                        st.write(f"• **{class_name}:** {count} detected")
                    
                    # Detailed results
                    with st.expander("🔍 Detailed Detection Results"):
                        for i, detection in enumerate(detections):
                            bbox = detection['bbox']
                            st.markdown(f"""
                            <div class="detection-box">
                                <strong>Detection {i+1}:</strong> {detection['class_name']}<br>
                                <strong>Confidence:</strong> {detection['confidence']:.3f}<br>
                                <strong>Bounding Box:</strong> ({bbox[0]}, {bbox[1]}) → ({bbox[2]}, {bbox[3]})
                            </div>
                            """, unsafe_allow_html=True)
                
                else:
                    progress_bar.progress(100)
                    status_text.text("⚠️ No objects detected")
                    
                    st.warning(f"""
                    **No objects detected!** 
                    
                    **Suggestions:**
                    - Try lowering the confidence threshold (current: {confidence_threshold:.2f})
                    - Ensure the image has clear, recognizable objects
                    - Check if the image quality is sufficient
                    
                    **Detection Time:** {detection_time:.2f}s
                    """)
                    
                    # Clear progress after delay
                    time.sleep(1)
                    progress_bar.empty()
                    status_text.empty()
    
    with tab2:
        st.subheader("🤖 Model Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Model Architecture:**
            - SSD MobileNet v2
            - Input Size: 300x300 pixels
            - Framework: TensorFlow Hub
            - Pre-trained on COCO dataset
            
            **Performance:**
            - Real-time detection capability
            - Optimized for mobile devices
            - Good accuracy-speed tradeoff
            """)
        
        with col2:
            st.markdown("""
            **Supported Object Classes (80 total):**
            
            **Vehicles:** car, bicycle, motorcycle, airplane, bus, train, truck, boat
            
            **People & Animals:** person, bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe
            
            **Indoor Objects:** chair, couch, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard
            
            **And many more...**
            """)
    
    with tab3:
        st.subheader("🧪 System Test Results")
        
        if st.button("🔄 Run System Tests"):
            with st.spinner("Running system diagnostics..."):
                # Test 1: Model loading
                st.write("**Test 1: Model Loading**")
                if model_loaded:
                    st.success("✅ Model loaded successfully")
                else:
                    st.error("❌ Model loading failed")
                
                # Test 2: Dependencies
                st.write("**Test 2: Dependencies Check**")
                try:
                    import tensorflow as tf_test
                    import cv2 as cv2_test
                    import numpy as np_test
                    import streamlit as st_version
                    
                    st.success("✅ All dependencies available")
                    st.write(f"- TensorFlow: {tf_test.__version__}")
                    st.write(f"- OpenCV: {cv2_test.__version__}")
                    st.write(f"- NumPy: {np_test.__version__}")
                    st.write(f"- Streamlit: {st_version.__version__}")
                    
                except Exception as e:
                    st.error(f"❌ Dependency issue: {e}")
                
                # Test 3: GPU availability
                st.write("**Test 3: Hardware Acceleration**")
                if tf_test.config.list_physical_devices('GPU'):
                    st.success("✅ GPU available for acceleration")
                else:
                    st.info("ℹ️ Running on CPU (normal for most setups)")
                
                # Test 4: Internet connection
                st.write("**Test 4: Model Download Capability**")
                if model_loaded:
                    st.success("✅ Internet connection and model download working")
                else:
                    st.warning("⚠️ Check internet connection for model downloads")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🎓 <strong>Final Year Project - Object Detection System</strong></p>
        <p>Built with Streamlit • SSD MobileNet v2 • TensorFlow Hub</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()