import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib
import os

TRAINING_DATA_PATH = "training_data.csv"
MODEL_PATH = "naive_bayes_model.pkl"

# 1. Load or create the training dataset
def load_training_data():
    if os.path.exists(TRAINING_DATA_PATH):
        return pd.read_csv(TRAINING_DATA_PATH)
    else:
        return pd.DataFrame(columns=["Description", "Category"])

# 2. Save new labeled data
def update_training_data(new_data: pd.DataFrame):
    existing_data = load_training_data()
    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    updated_data.drop_duplicates(inplace=True)  # Optional
    updated_data.to_csv(TRAINING_DATA_PATH, index=False)

# 3. Train and save the model
def train_and_save_model():
    data = load_training_data()
    if len(data) >= 2:  # Avoid training with insufficient data
        model = make_pipeline(CountVectorizer(), MultinomialNB())
        model.fit(data["Description"], data["Category"])
        joblib.dump(model, MODEL_PATH)
        return model
    return None

# 4. Load the model
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        return None

