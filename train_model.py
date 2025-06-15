import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle
import os

def load_and_prepare_data():
    """Load and prepare the training data"""
    # Load the training dataset
    dataset_path = os.path.join('Datasets and Rename', 'Training.csv')
    dataset = pd.read_csv(dataset_path)
    
    print(f"Dataset shape: {dataset.shape}")
    print(f"Unique diseases: {len(dataset['prognosis'].unique())}")
    
    # Separate features and target
    X = dataset.drop('prognosis', axis=1)
    y = dataset['prognosis']
    
    # Encode the target variable
    le = LabelEncoder()
    le.fit(y)
    Y = le.transform(y)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=20)
    
    return X_train, X_test, y_train, y_test, le, X.columns.tolist()

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple models and compare their performance"""
    
    models = {
        'SVC': SVC(kernel='linear', probability=True),
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'KNeighbors': KNeighborsClassifier(n_neighbors=5),
        'MultinomialNB': MultinomialNB(),
        'LogisticRegression': LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000, random_state=42)
    }
    
    model_results = {}
    
    print("Training and evaluating models...")
    print("=" * 50)
    
    for model_name, model in models.items():
        # Train the model
        model.fit(X_train, y_train)
        
        # Test the model
        predictions = model.predict(X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, predictions)
        
        # Store results
        model_results[model_name] = {
            'model': model,
            'accuracy': accuracy,
            'predictions': predictions
        }
        
        print(f"{model_name} Accuracy: {accuracy:.4f}")
    
    print("=" * 50)
    
    # Find the best model
    best_model_name = max(model_results.keys(), key=lambda k: model_results[k]['accuracy'])
    best_model = model_results[best_model_name]['model']
    
    print(f"Best model: {best_model_name} with accuracy: {model_results[best_model_name]['accuracy']:.4f}")
    
    return best_model, model_results

def save_model_and_data(model, label_encoder, feature_names):
    """Save the trained model and related data"""
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save the model
    with open('models/disease_prediction_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Save the label encoder
    with open('models/label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    
    # Save feature names
    with open('models/feature_names.pkl', 'wb') as f:
        pickle.dump(feature_names, f)
    
    print("Model and related data saved successfully!")

def create_symptoms_dict(feature_names):
    """Create symptoms dictionary for the web application"""
    symptoms_dict = {symptom: idx for idx, symptom in enumerate(feature_names)}
    
    # Save symptoms dictionary
    with open('models/symptoms_dict.pkl', 'wb') as f:
        pickle.dump(symptoms_dict, f)
    
    return symptoms_dict

def main():
    """Main function to train and save the model"""
    print("Starting model training process...")
    
    # Load and prepare data
    X_train, X_test, y_train, y_test, label_encoder, feature_names = load_and_prepare_data()
    
    # Train models
    best_model, model_results = train_models(X_train, X_test, y_train, y_test)
    
    # Create symptoms dictionary
    symptoms_dict = create_symptoms_dict(feature_names)
    
    # Save model and related data
    save_model_and_data(best_model, label_encoder, feature_names)
    
    # Create diseases list mapping
    diseases_list = {idx: disease for idx, disease in enumerate(label_encoder.classes_)}
    with open('models/diseases_list.pkl', 'wb') as f:
        pickle.dump(diseases_list, f)
    
    print(f"Total symptoms: {len(symptoms_dict)}")
    print(f"Total diseases: {len(diseases_list)}")
    print("Training completed successfully!")

if __name__ == "__main__":
    main()
