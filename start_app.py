#!/usr/bin/env python3
"""
Simple startup script for the Personalized Medicine Recommendation System
"""

import subprocess
import sys
import webbrowser
import time
import os

def main():
    print("🏥 Starting Personalized Medicine Recommendation System")
    print("=" * 60)
    
    # Check if data files exist
    required_files = [
        'Datasets and Rename/Training.csv',
        'Datasets and Rename/description.csv',
        'Datasets and Rename/medications.csv',
        'Datasets and Rename/diets.csv',
        'Datasets and Rename/precautions_df.csv',
        'Datasets and Rename/workout_df.csv'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required data files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\nPlease ensure all data files are present before running the application.")
        return
    
    print("✅ All required data files found!")
    print("\n🚀 Starting the web application...")
    
    try:
        # Start the application
        process = subprocess.Popen([sys.executable, 'app.py'])
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Open browser
        print("🌐 Opening web browser...")
        webbrowser.open('http://localhost:8000')
        
        print("\n" + "=" * 60)
        print("✅ Application started successfully!")
        print("🌐 Web interface: http://localhost:8000")
        print("📋 API endpoint: http://localhost:8000/api/predict")
        print("⏹️  Press Ctrl+C to stop the application")
        print("=" * 60)
        
        # Wait for the process to complete
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user.")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")

if __name__ == "__main__":
    main()
