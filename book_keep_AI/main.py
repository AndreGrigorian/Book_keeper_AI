import os
import pandas as pd
import bookkeeper_brain

# Optional: auto-train if model is missing
if not os.path.exists("model.pkl"):
    print("⚠️ model.pkl not found — training model...")
    bookkeeper_brain.train_and_save_model()

# Sample data to categorize
df = pd.DataFrame({
    "Memo": [
        "PARKMOBILE ZONE #9913 - STREET PARKING",
        "PARKMOBILE ZONE #9913",
        "PARKMOBILE ZONE #12354",
        "STARBUCKS AUTOPAY",
        "WALMART SUPERCENTER 1728",
        "STARBUCKS AUTOPAY",
    ],
    "Amount": [100, 100, 100,100, 100,100]
})

df['Memo'] = df['Memo'].str.upper() # Convert to uppercase for consistency

# Predict categories using the trained model
df['Predicted Account'] = bookkeeper_brain.categorize_batch(df['Memo'])

# Normalize memos to ensure exact matching
df['Normalized Memo'] = df['Memo'].astype(str).str.strip().str.lower()

# Use the normalized memos for scoring
memos = df['Normalized Memo'].tolist()

# Get scores
scores_dict = bookkeeper_brain.get_scores(memos)

# Map scores back using normalized memo
df['scores'] = df['Normalized Memo'].map(scores_dict)

print("\n🧾 Categorized Data:")
print(df)

