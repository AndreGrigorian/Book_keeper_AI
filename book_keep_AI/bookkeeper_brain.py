import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


# File paths
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
TRAINING_DATA_PATH = os.path.join(os.path.dirname(__file__), "training_data.csv")


# Load or initialize training data
def load_training_data():
    if not os.path.exists(TRAINING_DATA_PATH):
        return pd.DataFrame(columns=["Memo", "Category"])

    try:
        df = pd.read_csv(TRAINING_DATA_PATH)
        if df.empty:
            return pd.DataFrame(columns=["Memo", "Category"])
        return df
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["Memo", "Category"])


def save_training_data(df):
    df.to_csv(TRAINING_DATA_PATH, index=False)


def update_training_data(new_data):
    df_existing = load_training_data()
    df_combined = pd.concat([df_existing, new_data], ignore_index=True)
    save_training_data(df_combined)


def train_and_save_model():
    df = load_training_data()

    # Optional support if some files use 'Description' instead of 'Memo'
    if 'Description' in df.columns:
        df['Memo'] = df['Description']

    df["Memo"] = df["Memo"].fillna("").astype(str).str.strip()
    df["Category"] = df["Category"].fillna("").astype(str).str.strip()
    df = df[(df["Memo"] != "") & (df["Category"] != "")]

    if df.empty:
        raise ValueError("❌ No valid training data found. Cannot train model.")

    X = df["Memo"]
    y = df["Category"]

    model = Pipeline([
    ("tfidf", TfidfVectorizer(min_df=1, ngram_range=(1, 2))),
    ("clf", MultinomialNB()),
    ])

    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model trained and saved to: {MODEL_PATH}")


def load_model(model_path=None):
    if model_path is None:
        model_path = MODEL_PATH

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model file not found at: {model_path}")

    model = joblib.load(model_path)
    return model


def categorize_batch(memos, model_path=None, threshold=0.2):
    model = load_model(model_path)

    try:
        probs = model.predict_proba(memos)
        preds = model.predict(memos)
        results = [pred if max(prob) > threshold else None for pred, prob in zip(preds, probs)]
    except AttributeError:
        results = model.predict(memos)

    return results
