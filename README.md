# Personalized Medicine Recommendation System

An AI-powered web application that predicts diseases based on symptoms and provides personalized treatment recommendations including medications, diet, precautions, and exercise routines.

## Features

- 🤖 **AI-Powered Disease Prediction**: Uses machine learning algorithms (SVM, Random Forest, etc.) to predict diseases
- 💊 **Personalized Medication Recommendations**: Suggests appropriate medications for predicted conditions
- 🥗 **Dietary Guidance**: Provides diet recommendations to support treatment
- ⚠️ **Safety Precautions**: Lists important precautions to take
- 🏃 **Exercise Recommendations**: Suggests suitable workout routines
- 🌐 **User-Friendly Web Interface**: Modern, responsive web application
- 📱 **Mobile-Friendly**: Works on desktop, tablet, and mobile devices

## Quick Start

### Option 1: Automated Setup (Recommended)
```bash
python setup_and_run.py
```

This script will automatically:
1. Install all dependencies
2. Train the machine learning model
3. Start the web application

### Option 2: Manual Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the Model**
   ```bash
   python train_model.py
   ```

3. **Start the Application**
   ```bash
   python app.py
   ```

4. **Open in Browser**
   Navigate to `http://localhost:5000`

## Project Structure

```
├── app.py                          # Main Flask application
├── train_model.py                  # Machine learning model training
├── setup_and_run.py               # Automated setup script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Main symptom selection page
│   ├── result.html                # Results and recommendations page
│   └── error.html                 # Error page
├── models/                        # Trained models (created after training)
│   ├── disease_prediction_model.pkl
│   ├── label_encoder.pkl
│   ├── symptoms_dict.pkl
│   └── diseases_list.pkl
└── Datasets and Rename/           # Data files
    ├── Training.csv               # Training data
    ├── description.csv            # Disease descriptions
    ├── medications.csv            # Medication recommendations
    ├── diets.csv                  # Diet recommendations
    ├── precautions.csv            # Safety precautions
    └── workout.csv                # Exercise recommendations
```

## How It Works

1. **Symptom Selection**: Users select their symptoms from a comprehensive list
2. **AI Analysis**: The trained machine learning model analyzes the symptom pattern
3. **Disease Prediction**: The system predicts the most likely disease with confidence score
4. **Comprehensive Recommendations**: Provides personalized recommendations including:
   - Medications
   - Dietary advice
   - Safety precautions
   - Exercise routines

## Machine Learning Models

The system trains and compares multiple algorithms:
- Support Vector Machine (SVM)
- Random Forest
- Gradient Boosting
- K-Nearest Neighbors
- Naive Bayes
- Logistic Regression

The best-performing model is automatically selected for predictions.

## API Endpoints

- `GET /` - Main application interface
- `POST /predict` - Disease prediction from form data
- `POST /api/predict` - JSON API for predictions
- `GET /symptoms` - Get list of all symptoms

## Data Sources

The system uses medical datasets containing:
- **Training Data**: 4920 symptom-disease combinations
- **Disease Descriptions**: Detailed medical descriptions
- **Medications**: Evidence-based medication recommendations
- **Diets**: Nutritional guidance for each condition
- **Precautions**: Safety measures and lifestyle advice
- **Workouts**: Appropriate exercise recommendations

## Important Disclaimer

⚠️ **This system is for educational and informational purposes only.**

- Not a substitute for professional medical advice
- Always consult healthcare professionals for proper diagnosis
- Do not use for emergency medical situations
- Predictions are based on statistical patterns, not medical expertise

## Technical Requirements

- Python 3.7+
- Flask 2.3+
- scikit-learn 1.3+
- pandas 2.0+
- numpy 1.24+

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please ensure compliance with medical data regulations in your jurisdiction.

## Support

For issues or questions:
1. Check the troubleshooting section in the error page
2. Ensure all data files are present
3. Verify Python dependencies are installed
4. Check console output for detailed error messages

---

**Made with ❤️ for educational purposes in medical AI and machine learning.**
