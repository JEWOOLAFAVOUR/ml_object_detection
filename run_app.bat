@echo off
title SSD Object Detection System

echo ======================================
echo 🚀 SSD Object Detection System
echo ======================================
echo.

echo 🔄 Starting Streamlit app...
echo 📱 The app will open automatically in your browser
echo 🔗 URL: http://localhost:8501
echo.
echo ⚠️  If browser doesn't open, manually go to:
echo    http://localhost:8501
echo.
echo 🛑 Press Ctrl+C to stop the app
echo ======================================
echo.

streamlit run app.py

echo.
echo ✅ App stopped successfully
pause