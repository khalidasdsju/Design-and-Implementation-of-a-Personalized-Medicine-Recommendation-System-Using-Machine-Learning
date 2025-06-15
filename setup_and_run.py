#!/usr/bin/env python3
"""
Setup and Run Script for Personalized Medicine Recommendation System
This script will:
1. Install required dependencies
2. Train the machine learning model
3. Start the Flask web application
"""

import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"🔄 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        print(f"Return code: {e.returncode}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def check_files():
    """Check if required files exist"""
    print("\n🔍 Checking required files...")
    
    required_files = [
        'Datasets and Rename/Training.csv',
        'Datasets and Rename/description.csv',
        'Datasets and Rename/medications.csv',
        'Datasets and Rename/diets.csv',
        'Datasets and Rename/precautions.csv',
        'Datasets and Rename/workout.csv'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ Found: {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files found!")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        return False
    
    return run_command("pip install -r requirements.txt", "Installing Python packages")

def train_model():
    """Train the machine learning model"""
    print("\n🤖 Training machine learning model...")
    
    # Check if model already exists
    if os.path.exists('models/disease_prediction_model.pkl'):
        response = input("Model already exists. Retrain? (y/N): ").lower()
        if response != 'y':
            print("✅ Using existing model.")
            return True
    
    return run_command("python train_model.py", "Training machine learning model")

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting Flask application...")
    print("The application will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Start the Flask app
        subprocess.run("python app.py", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting application: {e}")
        return False
    
    return True

def main():
    """Main setup and run function"""
    print("🏥 Personalized Medicine Recommendation System")
    print("=" * 60)
    print("This script will set up and run the complete application.")
    print("=" * 60)
    
    # Step 1: Check required files
    if not check_files():
        print("\n❌ Setup failed: Missing required data files.")
        print("Please ensure all CSV files are in the 'Datasets and Rename' folder.")
        sys.exit(1)
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies.")
        sys.exit(1)
    
    # Step 3: Train model
    if not train_model():
        print("\n❌ Setup failed: Could not train machine learning model.")
        sys.exit(1)
    
    # Step 4: Start application
    print("\n✅ Setup completed successfully!")
    print("\n" + "="*60)
    print("🎉 Ready to start the application!")
    print("="*60)
    
    input("\nPress Enter to start the web application...")
    
    if not start_application():
        print("\n❌ Failed to start application.")
        sys.exit(1)

if __name__ == "__main__":
    main()
