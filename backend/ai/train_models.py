import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

def train_models():
    # Load dataset
    dataset_path = "ai/careers_dataset.csv"
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}. Please run dataset_generator.py first.")
        return
        
    df = pd.read_csv(dataset_path)
    
    # Features and Target
    X = df.drop("target_career", axis=1)
    y = df["target_career"]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "decision_tree": DecisionTreeClassifier(random_state=42),
        "knn": KNeighborsClassifier(n_neighbors=5)
    }
    
    # Directory to save models
    os.makedirs("ml_models", exist_ok=True)
    
    print("Training models...")
    for name, model in models.items():
        # Train
        model.fit(X_train, y_train)
        
        # Evaluate
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"{name} Accuracy: {accuracy:.4f}")
        
        # Save model
        model_path = f"ml_models/{name}_model.pkl"
        joblib.dump(model, model_path)
        print(f"Saved {name} to {model_path}")

    # Also save the feature names to ensure inputs match during prediction
    joblib.dump(list(X.columns), "ml_models/feature_names.pkl")
    print("Saved feature_names.pkl")

if __name__ == "__main__":
    train_models()
