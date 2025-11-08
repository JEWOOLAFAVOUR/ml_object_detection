#!/bin/bash
# run_app.sh - Quick start script for Linux/Mac

echo "======================================"
echo "🚀 Starting SSD Object Detection App"
echo "======================================"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

echo "🔄 Starting Streamlit app..."
echo "📱 The app will open in your browser automatically"
echo "🔗 URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the app"
echo "======================================"

streamlit run app.py