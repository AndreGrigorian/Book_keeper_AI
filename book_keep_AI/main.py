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
        "Starbucks coffee purchase",
        "Starbucks 1245 Main St",
        "Starbucks coffee",
        "STARBUCKS AUTOPAY"
    ],
    "Amount": [100, 100, 100,100]
})

df['Memo'] = df['Memo'].str.upper() # Convert to uppercase for consistency

# Predict categories using the trained model
df['Predicted Account'] = bookkeeper_brain.categorize_batch(df['Memo'])

print("\n🧾 Categorized Data:")
print(df)

