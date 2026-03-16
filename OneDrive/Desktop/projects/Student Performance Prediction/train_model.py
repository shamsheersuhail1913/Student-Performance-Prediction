import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data/student_data.csv")

# Load dataset
df = pd.read_csv(DATA_PATH)

FEATURE_COLUMNS = [
    "attendance",
    "study_hours",
    "assignment_score",
    "mid_exam_score",
    "previous_sem_score",
    "participation_score"
]

X = df[FEATURE_COLUMNS]
y = df["risk_level"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)

print("\nModel Evaluation")
print(classification_report(y_test, predictions))
print("Accuracy:", accuracy_score(y_test, predictions))

# Confusion Matrix
cm = confusion_matrix(y_test, predictions)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.savefig(os.path.join(BASE_DIR, "confusion_matrix.png"))

# Save model + features
joblib.dump({
    "model": model,
    "features": FEATURE_COLUMNS
}, os.path.join(BASE_DIR, "model.pkl"))

print("Model trained and saved successfully.")