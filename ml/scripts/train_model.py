import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
from pathlib import Path


def train_model():
    print("Loading extracted features...")
    df = pd.read_csv(Path('data/processed/features_extracted.csv'))

    # 1. Convert text labels (GESTURE, DROP_ARM) into numbers (0, 1, 2, 3)
    le = LabelEncoder()
    df['label'] = le.fit_transform(df['gesture'])
    print(f"Gesture classes: {le.classes_}")

    # 2. Convert the string arrays back into real number arrays
    X = np.array([np.fromstring(features.strip('[]'), sep=' ') for features in df['features']])
    y = df['label'].values

    # 3. Split into Training Set (80%) and Testing Set (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples...")

    # 4. Build the XGBoost Brain
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric='mlogloss'
    )

    # 5. Train it!
    model.fit(X_train, y_train)

    # 6. Test it!
    y_pred = model.predict(X_test)
    print("\n--- BRAIN TEST RESULTS ---")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    # 7. Save the trained brain and the label decoder
    Path('models/v1.0.0').mkdir(exist_ok=True)
    joblib.dump(model, Path('models/v1.0.0/gesture_model.pkl'))
    joblib.dump(le, Path('models/v1.0.0/label_encoder.pkl'))
    print("\nBrain saved to models/v1.0.0/gesture_model.pkl")


if __name__ == "__main__":
    train_model()