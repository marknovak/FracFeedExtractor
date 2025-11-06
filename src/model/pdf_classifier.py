import argparse
import joblib
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.preprocessing.pdf_text_extraction import extract_text_from_pdf

DIET_TERMS = ["stomach contents", "prey composition", "percent occurrence", "feeding habits", "gut content", "dietary analysis", "trophic", "predator-prey", "fish species", "diet analysis"]


# Classify a single PDF as useful or not useful based on its text content.
def classify_pdf(pdf_path, model_dir="src/model/model-config"):
    model_path = Path(model_dir) / "pdf_classifier_model.pkl"
    vectorizer_path = Path(model_dir) / "tfidf_vectorizer.pkl"

    # Load model and TF-IDF vectorizer
    if not model_path.exists() or not vectorizer_path.exists():
        print(f"[ERROR] Missing model or vectorizer in {model_dir}")
        return

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print(f"[ERROR] No text extracted from {pdf_path}. Skipping classification.")
        return

    # Transform and classify
    X_vec = vectorizer.transform([text])
    prediction = model.predict(X_vec)[0]

    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(X_vec)[0]
        confidence = max(prob)
        print("\n=== PDF Classification Result ===")
        print(f" File:        {Path(pdf_path).name}")
        print(f" Prediction:  {prediction.capitalize()} ({confidence:.2%} confidence)")
        print("=================================\n")
    else:
        print("\n=== PDF Classification Result ===")
        print(f" File:        {Path(pdf_path).name}")
        print(f" Prediction:  {prediction.capitalize()}")
        print("=================================\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify a PDF as useful or not useful.")
    parser.add_argument("--pdf-path", type=str, help="Path to the PDF file to classify.")
    parser.add_argument("--model_dir", type=str, default="src/model/model-config", help="Directory containing the trained model and TF-IDF vectorizer.")
    args = parser.parse_args()

    classify_pdf(args.pdf_path, args.model_dir)
