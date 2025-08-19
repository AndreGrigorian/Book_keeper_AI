from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pandas as pd
import joblib  # for saving/loading model

# Paths to saved model and data
MODEL_PATH = "model.pkl"
TRAINING_DATA_PATH = "training_data.csv"

# Load or initialize training data
def load_training_data():
    import os
    import pandas as pd

    if not os.path.exists(TRAINING_DATA_PATH):
        return pd.DataFrame(columns=["Memo", "Category"])

    try:
        df = pd.read_csv(TRAINING_DATA_PATH)
        if df.empty:
            return pd.DataFrame(columns=["Memo", "Category"])
        return df
    except pd.errors.EmptyDataError:
        # File exists but empty
        return pd.DataFrame(columns=["Memo", "Category"])

def save_training_data(df):
    df.to_csv(TRAINING_DATA_PATH, index=False)

# Update training data with new entries
def update_training_data(new_data):
    df_existing = load_training_data()
    df_combined = pd.concat([df_existing, new_data], ignore_index=True).drop_duplicates()
    save_training_data(df_combined)


def train_and_save_model():
    df = load_training_data()
    if df.empty:
        return

    # Clean 'Memo' column: convert to string, fill NaNs, strip whitespace
    df["Memo"] = df["Memo"].fillna("").astype(str).str.strip()
    df["Category"] = df["Category"].fillna("").astype(str).str.strip()

    # Filter out rows where Memo is empty after stripping
    df = df[df["Memo"] != ""]

    # Also optionally filter out rows with empty Category
    df = df[df["Category"] != ""]

    if df.empty:
        print("No valid training data after filtering empty Memo/Category. Skipping training.")
        return

    X = df["Memo"]
    y = df["Category"]

    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(multi_class="multinomial", solver="lbfgs", max_iter=1000)),
    ])

    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)

# Load model for inference
def load_model():
    return joblib.load(MODEL_PATH)

# Predict single input
def categorize(description):
    model = load_model()
    return model.predict([description])[0]

# Predict batch input (for DataFrame .map)
def categorize_batch(descriptions):
    model = load_model()
    return model.predict(descriptions)


