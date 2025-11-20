import argparse
import joblib
from pathlib import Path
import xgboost as xgb
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.preprocessing.pdf_text_extraction import extract_text_from_pdf


# Classify a single PDF as useful or not useful based on its text content.
def classify_pdf(pdf_path, model_dir="src/model/models"):
    model_path = Path(model_dir) / "pdf_classifier.json"
    vectorizer_path = Path(model_dir) / "tfidf_vectorizer.pkl"
    encoder_path = Path(model_dir) / "label_encoder.pkl"

    if not model_path.exists() or not vectorizer_path.exists() or not encoder_path.exists():
        print(f"[ERROR] Missing model, encoder, or vectorizer in {model_dir}")
        return

    # Load model, encoder, and TF-IDF vectorizer
    model = xgb.Booster()
    model.load_model(str(model_path))
    vectorizer = joblib.load(vectorizer_path)
    encoder = joblib.load(encoder_path)

    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print(f"[ERROR] No text extracted from {pdf_path}. Skipping classification.")
        return

    # Transform text into vectorized TF-IDF format
    X_vec = vectorizer.transform([text])

    # Wrap in DMatrix for XGBoost prediction
    dtest = xgb.DMatrix(X_vec)
    pred_prob = model.predict(dtest)[0]
    pred_class = 1 if pred_prob >= 0.70 else 0

    # Convert numeric class back into original label name
    pred_label = encoder.inverse_transform([pred_class])[0]

    if pred_class == 0:
        confidence = 1 - pred_prob
    else:
        confidence = pred_prob

    print("\n=== PDF Classification Result ===")
    print(f" File: {Path(pdf_path).name}")
    print(f" Prediction: {pred_label} ({confidence:.2%} confidence)")
    print("=================================\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify a PDF as useful or not useful.")
    parser.add_argument("--pdf-path", type=str, help="Path to the PDF file to classify.")
    parser.add_argument("--model_dir", type=str, default="src/model/models", help="Directory containing the trained model and TF-IDF vectorizer.")
    args = parser.parse_args()

    classify_pdf(args.pdf_path, args.model_dir)
