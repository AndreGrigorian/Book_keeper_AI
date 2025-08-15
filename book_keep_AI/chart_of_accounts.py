import numpy as np
import pandas as pd
from transformers import pipeline
from openpyxl import *
import data_cleaner
import classify_transactions
import os

from dotenv import load_dotenv
load_dotenv()  # loads OPENAI_API_KEY from .env

# Load your Excel sheet into a DataFrame
print("classifying...")
df = pd.read_excel("dummy_data.xlsx")
df["Memo"] = df["Memo"].apply(data_cleaner.janitor)
# df['Predicted Account'] = df['Memo'].apply(classify_transactions.categorize)
df["Predicted Account"] = df["Memo"].map(classify_transactions.categorize)


df.to_excel("updated_csv.xlsx", index=False)
