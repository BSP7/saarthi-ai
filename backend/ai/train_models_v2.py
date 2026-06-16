import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

def train_models_v2():
    dataset_path = os.path.join(os.path.dirname(__file__), "careers_dataset_v2.csv")
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}.")
        return
        
    df = pd.read_csv(dataset_path)
    
    # Features (30 columns)
    # Exclude metadata columns to isolate features
    exclude_cols = ['soc_code', 'occupation_title', 'target_domain', 'description']
    X = df.drop(columns=[col for col in exclude_cols if col in df.columns])
    y = df["target_domain"]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Directory to save models
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_models"), exist_ok=True)
    
    print("Training Domain Classifier (V2)...")
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average='weighted', zero_division=0)
    recall = recall_score(y_test, predictions, average='weighted', zero_division=0)
    f1 = f1_score(y_test, predictions, average='weighted', zero_division=0)
    
    print(f"Random Forest Domain Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f} | Recall: {recall:.4f} | F1 Score: {f1:.4f}")
    
    # Save model
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_models", "domain_classifier_rf.pkl")
    joblib.dump(model, model_path)
    print(f"Saved model to {model_path}")

    # Also save the feature names to ensure inputs match during prediction
    joblib.dump(list(X.columns), os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml_models", "feature_names_v2.pkl"))
    print("Saved feature_names_v2.pkl")

if __name__ == "__main__":
    train_models_v2()
