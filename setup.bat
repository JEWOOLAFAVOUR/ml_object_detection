@echo off
echo ====================================
echo SSD Object Detection System Setup
echo ====================================
echo.

echo 1. Installing Python dependencies...
echo This may take a few minutes...
echo.

pip install -r requirements.txt

echo.
echo 2. Testing the detector...
python test_detector.py

echo.
echo 3. Setup complete!
echo.
echo To run the Streamlit app:
echo   streamlit run app.py
echo.
echo The app will open in your browser automatically.
echo Press Ctrl+C to stop the app when done.
echo.
pause