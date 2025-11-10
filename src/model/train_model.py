"""
PDF FracFeedExtractor Classifier
-------------------------

This module uses scikit-learn to train and evaluate a text classification model
that predicts whether a PDF is useful for predator diet data analysis.

The model uses TF-IDF vectorization + Logistic Regression.
"""

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib
import json
import sys
from collections import Counter


# Load processed text files and their useful vs not useful labels.
def load_labeled_data(data_dir="data/processed-text", labels_file="data/labels.json"):
    # Load label mappings from JSON file
    data_dir = Path(data_dir)
    with open(labels_file, "r", encoding="utf-8") as f:
        labels_map = json.load(f)

    # Iterate through all .txt files in the processed-text directory
    texts, labels, filenames = [], [], []
    for txt_file in data_dir.glob("*.txt"):
        fname = txt_file.name
        # Only include files that have a corresponding label
        if fname in labels_map:
            with open(txt_file, "r", encoding="utf-8") as f:
                texts.append(f.read())
                labels.append(labels_map[fname])
                filenames.append(fname)
        else:
            print(f"[WARN] No label found for {fname}, skipping.")
    return texts, labels, filenames


# Trains and save a scikit-learn classification model.
def train_pdf_classifier(texts, labels, output_dir="src/model/models"):
    # Basic validations
    if not texts or not labels:
        print("[ERROR] No training samples found. Ensure PDFs were extracted to text before training.")
        return None

    class_counts = Counter(labels)
    if len(class_counts) < 2:
        print(f"[ERROR] Need at least 2 classes to train classifier. Found: {class_counts}")
        return None

    if any(c < 2 for c in class_counts.values()):
        print(f"[ERROR] Each class needs at least 2 samples for stratified split. Counts: {class_counts}")
        return None
    # Split the dataset into training and testing sets (stratified by label ratio)
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )
    except ValueError as e:
        print(f"[ERROR] train_test_split failed: {e}")
        return None

    # Convert text data into TF-IDF features
    vectorizer = TfidfVectorizer(max_features=10000, stop_words="english", ngram_range=(1, 3))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Initialize a logistic regression classifier
    model = LogisticRegression(max_iter=100000, solver="liblinear")
    model.fit(X_train_vec, y_train)  # Train the model

    # Evaluate model performance
    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print("\n=== Model Evaluation ===")
    print(f"Accuracy: {acc:.2f}")
    print(classification_report(y_test, y_pred, digits=2))
    print("========================\n")

    # Save model and vectorizer for future use
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    joblib.dump(model, Path(output_dir) / "pdf_classifier_model.pkl")
    joblib.dump(vectorizer, Path(output_dir) / "tfidf_vectorizer.pkl")

    return {"accuracy": acc}


if __name__ == "__main__":
    texts, labels, _ = load_labeled_data()
    result = train_pdf_classifier(texts, labels, "src/model/models")
    if result is None:
        sys.exit(1)
    print(f"Model trained successfully! Accuracy: {result['accuracy']:.2f}")
