import os
import csv
import json
import ast
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import html

# Global variables to store data
symptoms_list = []
diseases_data = {}
description_data = {}
medications_data = {}
diets_data = {}
precautions_data = {}
workouts_data = {}

def load_csv_data():
    """Load CSV data files"""
    global symptoms_list, diseases_data, description_data, medications_data
    global diets_data, precautions_data, workouts_data

    try:
        data_path = 'Datasets and Rename'

        # Load training data to get symptoms
        with open(os.path.join(data_path, 'Training.csv'), 'r') as f:
            reader = csv.DictReader(f)
            first_row = next(reader)
            symptoms_list = [col for col in first_row.keys() if col != 'prognosis']

        # Load descriptions
        with open(os.path.join(data_path, 'description.csv'), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                description_data[row['Disease']] = row['Description']

        # Load medications
        with open(os.path.join(data_path, 'medications.csv'), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    medications_data[row['Disease']] = ast.literal_eval(row['Medication'])
                except:
                    medications_data[row['Disease']] = [row['Medication']]

        # Load diets
        with open(os.path.join(data_path, 'diets.csv'), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    diets_data[row['Disease']] = ast.literal_eval(row['Diet'])
                except:
                    diets_data[row['Disease']] = [row['Diet']]

        # Load precautions
        with open(os.path.join(data_path, 'precautions_df.csv'), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                precautions = []
                for i in range(1, 5):
                    col_name = f'Precaution_{i}'
                    if col_name in row and row[col_name]:
                        precautions.append(row[col_name])
                precautions_data[row['Disease']] = precautions

        # Load workouts
        with open(os.path.join(data_path, 'workout_df.csv'), 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    workouts_data[row['disease']] = ast.literal_eval(row['workout'])
                except:
                    workouts_data[row['disease']] = [row['workout']]

        print("All data loaded successfully!")
        return True

    except Exception as e:
        print(f"Error loading data: {e}")
        return False

def predict_disease(selected_symptoms):
    """Simple rule-based disease prediction"""
    # Simple symptom-to-disease mapping for demonstration
    disease_rules = {
        'Common Cold': ['runny_nose', 'sneezing', 'cough', 'sore_throat'],
        'Flu': ['fever', 'chills', 'muscle_aches', 'fatigue', 'headache'],
        'Gastroenteritis': ['stomach_pain', 'nausea', 'vomiting', 'diarrhoea'],
        'Migraine': ['headache', 'nausea', 'vomiting', 'sensitivity_to_light'],
        'Hypertension': ['headache', 'dizziness', 'chest_pain'],
        'Diabetes': ['increased_thirst', 'frequent_urination', 'fatigue', 'blurred_vision'],
        'Bronchial Asthma': ['cough', 'shortness_of_breath', 'wheezing'],
        'Malaria': ['fever', 'chills', 'headache', 'nausea', 'vomiting'],
        'Dengue': ['fever', 'headache', 'muscle_aches', 'nausea', 'rash'],
        'Pneumonia': ['cough', 'fever', 'shortness_of_breath', 'chest_pain']
    }

    # Calculate match scores
    best_match = None
    best_score = 0

    for disease, disease_symptoms in disease_rules.items():
        # Count matching symptoms
        matches = sum(1 for symptom in selected_symptoms if symptom in disease_symptoms)
        score = (matches / len(disease_symptoms)) * 100 if disease_symptoms else 0

        if score > best_score:
            best_score = score
            best_match = disease

    # If no good match, return a default
    if best_score < 20:
        best_match = 'Common Cold'
        best_score = 50

    return best_match, best_score

def get_disease_info(disease_name):
    """Get comprehensive information about a disease"""
    info = {
        'description': '',
        'medications': [],
        'diet': [],
        'precautions': [],
        'workouts': []
    }

    try:
        # Get description
        if disease_name in description_data:
            info['description'] = description_data[disease_name]

        # Get medications
        if disease_name in medications_data:
            info['medications'] = medications_data[disease_name]

        # Get diet recommendations
        if disease_name in diets_data:
            info['diet'] = diets_data[disease_name]

        # Get precautions
        if disease_name in precautions_data:
            info['precautions'] = precautions_data[disease_name]

        # Get workout recommendations
        if disease_name in workouts_data:
            info['workouts'] = workouts_data[disease_name]

    except Exception as e:
        print(f"Error getting disease info: {e}")

    return info

class MedicalRecommendationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/' or path == '/index.html':
            self.serve_index()
        elif path == '/symptoms':
            self.serve_symptoms_api()
        elif path.startswith('/static/'):
            self.serve_static_file(path)
        else:
            self.send_error(404)

    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/predict':
            self.handle_prediction()
        elif path == '/api/predict':
            self.handle_api_prediction()
        else:
            self.send_error(404)

    def serve_index(self):
        """Serve the main index page"""
        html_content = self.generate_index_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())

    def serve_symptoms_api(self):
        """Serve symptoms API"""
        response = {'symptoms': sorted(symptoms_list)}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def handle_prediction(self):
        """Handle form-based prediction"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(post_data)

            selected_symptoms = form_data.get('symptoms', [])

            if not selected_symptoms:
                html_content = self.generate_result_html(error="Please select at least one symptom.")
            else:
                disease, confidence = predict_disease(selected_symptoms)
                disease_info = get_disease_info(disease)
                html_content = self.generate_result_html(
                    disease=disease,
                    confidence=round(confidence, 2),
                    symptoms=selected_symptoms,
                    info=disease_info
                )

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())

        except Exception as e:
            html_content = self.generate_result_html(error=f"An error occurred: {str(e)}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())

    def handle_api_prediction(self):
        """Handle API-based prediction"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)

            selected_symptoms = data.get('symptoms', [])

            if not selected_symptoms:
                response = {'error': 'No symptoms provided'}
                self.send_response(400)
            else:
                disease, confidence = predict_disease(selected_symptoms)
                disease_info = get_disease_info(disease)
                response = {
                    'disease': disease,
                    'confidence': round(confidence, 2),
                    'symptoms': selected_symptoms,
                    'info': disease_info
                }
                self.send_response(200)

            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            response = {'error': str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

    def generate_index_html(self):
        """Generate the main index HTML page"""
        symptoms_checkboxes = ""
        for i, symptom in enumerate(sorted(symptoms_list)):
            symptom_display = symptom.replace('_', ' ').title()
            symptoms_checkboxes += f'''
            <div class="col-md-4 col-sm-6 symptom-checkbox">
                <div class="form-check">
                    <input class="form-check-input" type="checkbox"
                           name="symptoms" value="{symptom}" id="symptom_{i}">
                    <label class="form-check-label" for="symptom_{i}">
                        {symptom_display}
                    </label>
                </div>
            </div>
            '''

        return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personalized Medicine Recommendation System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .main-container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            margin: 20px auto;
            padding: 30px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }}
        .header h1 {{
            color: #667eea;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        .btn-primary {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            border-radius: 25px;
            padding: 12px 30px;
            font-weight: 600;
        }}
        .card {{
            border: none;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        }}
        .card-header {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border-radius: 15px 15px 0 0 !important;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="main-container">
            <div class="header">
                <h1><i class="fas fa-stethoscope"></i> Personalized Medicine Recommendation System</h1>
                <p>AI-powered disease prediction and personalized treatment recommendations</p>
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header">
                            <h4><i class="fas fa-clipboard-list"></i> Select Your Symptoms</h4>
                            <small>Choose all symptoms you are currently experiencing</small>
                        </div>
                        <div class="card-body">
                            <form method="POST" action="/predict">
                                <div class="row">
                                    {symptoms_checkboxes}
                                </div>
                                <div class="text-center mt-4">
                                    <button type="submit" class="btn btn-primary btn-lg">
                                        <i class="fas fa-diagnoses"></i> Get Diagnosis & Recommendations
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            <div class="footer text-center mt-4">
                <p><i class="fas fa-info-circle"></i> This system is for educational purposes only. Always consult with healthcare professionals for medical advice.</p>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
        '''

    def generate_result_html(self, disease=None, confidence=None, symptoms=None, info=None, error=None):
        """Generate the result HTML page"""
        if error:
            content = f'''
            <div class="alert alert-danger" role="alert">
                <i class="fas fa-exclamation-triangle"></i> {html.escape(error)}
            </div>
            <div class="text-center">
                <a href="/" class="btn btn-primary">
                    <i class="fas fa-arrow-left"></i> Try Again
                </a>
            </div>
            '''
        else:
            symptoms_badges = ""
            if symptoms:
                for symptom in symptoms:
                    symptom_display = symptom.replace('_', ' ').title()
                    symptoms_badges += f'<span class="badge bg-primary mb-2 me-2">{symptom_display}</span>'

            medications_list = ""
            if info and info.get('medications'):
                for med in info['medications']:
                    medications_list += f'<li class="list-group-item"><i class="fas fa-capsules text-primary me-2"></i>{html.escape(med)}</li>'

            diet_list = ""
            if info and info.get('diet'):
                for diet_item in info['diet']:
                    diet_list += f'<li class="list-group-item"><i class="fas fa-leaf text-success me-2"></i>{html.escape(diet_item)}</li>'

            precautions_list = ""
            if info and info.get('precautions'):
                for precaution in info['precautions']:
                    precautions_list += f'<li class="list-group-item"><i class="fas fa-exclamation-triangle text-warning me-2"></i>{html.escape(precaution)}</li>'

            workouts_list = ""
            if info and info.get('workouts'):
                for workout in info['workouts']:
                    workouts_list += f'<li class="list-group-item"><i class="fas fa-running text-info me-2"></i>{html.escape(workout)}</li>'

            content = f'''
            <div class="row">
                <div class="col-md-12">
                    <div class="card mb-4">
                        <div class="card-header bg-success text-white">
                            <h4><i class="fas fa-diagnoses"></i> Diagnosis Result</h4>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-8">
                                    <h3 class="text-success">{html.escape(disease or 'Unknown')}</h3>
                                    <p class="lead">Based on your symptoms, our system predicts this condition with <strong>{confidence}% confidence</strong>.</p>

                                    {f'<div class="mt-3"><h5><i class="fas fa-info-circle"></i> Description</h5><p class="text-muted">{html.escape(info.get("description", ""))}</p></div>' if info and info.get('description') else ''}
                                </div>
                                <div class="col-md-4">
                                    <div class="text-center">
                                        <div class="progress mb-3" style="height: 20px;">
                                            <div class="progress-bar bg-success" role="progressbar"
                                                 style="width: {confidence}%" aria-valuenow="{confidence}"
                                                 aria-valuemin="0" aria-valuemax="100">
                                                {confidence}%
                                            </div>
                                        </div>
                                        <small class="text-muted">Prediction Confidence</small>
                                    </div>
                                </div>
                            </div>

                            <div class="mt-4">
                                <h5><i class="fas fa-list-check"></i> Your Selected Symptoms</h5>
                                <div class="row">
                                    {symptoms_badges}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                {f'<div class="col-md-6 mb-4"><div class="card h-100"><div class="card-header"><h5><i class="fas fa-pills"></i> Recommended Medications</h5></div><div class="card-body"><ul class="list-group list-group-flush">{medications_list}</ul></div></div></div>' if medications_list else ''}

                {f'<div class="col-md-6 mb-4"><div class="card h-100"><div class="card-header"><h5><i class="fas fa-utensils"></i> Dietary Recommendations</h5></div><div class="card-body"><ul class="list-group list-group-flush">{diet_list}</ul></div></div></div>' if diet_list else ''}
            </div>

            <div class="row">
                {f'<div class="col-md-6 mb-4"><div class="card h-100"><div class="card-header"><h5><i class="fas fa-shield-alt"></i> Precautions</h5></div><div class="card-body"><ul class="list-group list-group-flush">{precautions_list}</ul></div></div></div>' if precautions_list else ''}

                {f'<div class="col-md-6 mb-4"><div class="card h-100"><div class="card-header"><h5><i class="fas fa-dumbbell"></i> Exercise Recommendations</h5></div><div class="card-body"><ul class="list-group list-group-flush">{workouts_list}</ul></div></div></div>' if workouts_list else ''}
            </div>

            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-body text-center">
                            <a href="/" class="btn btn-primary me-3">
                                <i class="fas fa-redo"></i> New Diagnosis
                            </a>
                            <button class="btn btn-success" onclick="window.print()">
                                <i class="fas fa-print"></i> Print Results
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mt-4">
                <div class="col-md-12">
                    <div class="alert alert-warning" role="alert">
                        <h5><i class="fas fa-exclamation-triangle"></i> Important Medical Disclaimer</h5>
                        <p class="mb-0">
                            This system is designed for educational and informational purposes only.
                            The predictions and recommendations provided should not replace professional medical advice,
                            diagnosis, or treatment. Always consult with qualified healthcare professionals for proper
                            medical evaluation and treatment decisions.
                        </p>
                    </div>
                </div>
            </div>
            '''

        return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diagnosis Results - Personalized Medicine System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .main-container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            margin: 20px auto;
            padding: 30px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }}
        .header h1 {{
            color: #667eea;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        .btn-primary {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            border: none;
            border-radius: 25px;
            padding: 12px 30px;
            font-weight: 600;
        }}
        .card {{
            border: none;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        }}
        .card-header {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border-radius: 15px 15px 0 0 !important;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="main-container">
            <div class="header">
                <h1><i class="fas fa-stethoscope"></i> Personalized Medicine Recommendation System</h1>
                <p>AI-powered disease prediction and personalized treatment recommendations</p>
            </div>

            {content}

            <div class="footer text-center mt-4">
                <p><i class="fas fa-info-circle"></i> This system is for educational purposes only. Always consult with healthcare professionals for medical advice.</p>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
        '''


def main():
    """Main function to start the server"""
    print("🏥 Personalized Medicine Recommendation System")
    print("=" * 60)

    # Load data
    if not load_csv_data():
        print("❌ Failed to load data files.")
        return

    print(f"✅ Loaded {len(symptoms_list)} symptoms")
    print(f"✅ Loaded data for {len(description_data)} diseases")

    # Start server
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MedicalRecommendationHandler)

    print("\n🚀 Starting server...")
    print(f"🌐 Server running at: http://localhost:8000")
    print("📱 Open this URL in your web browser")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 60)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user.")
        httpd.server_close()


if __name__ == '__main__':
    main()
