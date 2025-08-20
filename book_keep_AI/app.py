import streamlit as st
import pandas as pd
from io import BytesIO
import data_cleaner  # your custom module
import classify_transactions  # your categorizer module
import bookkeeper_brain  # your model training module
import os


st.title("🤖 RoboLedger 🤖")
st.subheader("Your AI-powered financial assistant")
st.subheader("Choose a file and view the contents below")

# --- Upload Type Selection ---
upload_type = st.radio("Choose file type to upload:", ("Excel"))

# Shared preprocessing function
@st.cache_data
def preprocess_and_categorize(df_input):
    df_copy = df_input.copy()
    df_copy["Memo"] = df_copy["Memo"].apply(data_cleaner.janitor)
    if os.path.exists(bookkeeper_brain.MODEL_PATH):
        df_copy['Predicted Account'] = bookkeeper_brain.categorize_batch(df_copy['Memo'])
        mask = df_copy["Memo"].notna()
        df_copy.loc[mask, "Predicted Account"] = classify_transactions.categorize_batch(df_copy.loc[mask, "Memo"])
    else:
        df_copy['Predicted Account'] = classify_transactions.categorize_batch(df_copy['Memo'])
    return df_copy

if upload_type == "Excel":
    uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["xlsx", "xls", "csv"])

    if uploaded_file:
        # Initialize or update session state dataframe on new upload
        if "df" not in st.session_state or st.session_state.get("uploaded_file_name") != uploaded_file.name:
            try:
                if uploaded_file.name.endswith((".xlsx", ".xls")):
                    df_raw = pd.read_excel(uploaded_file)
                elif uploaded_file.name.endswith(".csv"):
                    df_raw = pd.read_csv(uploaded_file)
                else:
                    st.error("Unsupported file type.")
                    st.stop()
                processed_df = preprocess_and_categorize(df_raw)
                st.session_state.df = processed_df
                st.session_state.uploaded_file_name = uploaded_file.name
            except Exception as e:
                st.error(f"Error reading file: {e}")
                st.stop()

        df = st.session_state.df

        st.success("File uploaded and processed successfully!")
        st.write("Preview of processed data:")
        st.dataframe(df)

        # --- Row Editing ---
        if not df.empty:
            st.subheader("Edit a Row in the Data")
            default_row = int(df.index.min())
            row_index_input = st.text_input("Enter row index to edit", value=str(default_row))

            try:
                row_index = int(row_index_input)
                if row_index not in df.index:
                    st.warning(f"Row index {row_index} not found. Using default {default_row}.")
                    row_index = default_row
            except ValueError:
                st.warning("Invalid row index input. Using default.")
                row_index = default_row

            updated_values = {}
            for col in df.columns:
                original_value = df.at[row_index, col]
                if pd.api.types.is_numeric_dtype(df[col]):
                    new_val = st.number_input(f"{col}", value=float(original_value), key=f"{col}_{row_index}")
                else:
                    new_val = st.text_input(f"{col}", value=str(original_value), key=f"{col}_{row_index}")
                updated_values[col] = new_val

            if st.button("Save Changes"):
                changes_made = False
                original_row = df.loc[row_index].copy()

                for col, new_val in updated_values.items():
                    # Convert number inputs back to original dtype if needed
                    if pd.api.types.is_numeric_dtype(df[col]):
                        # Convert new_val to correct numeric type, for example float or int
                        if pd.api.types.is_integer_dtype(df[col]):
                            try:
                                new_val = int(new_val)
                            except:
                                new_val = float(new_val)
                        else:
                            new_val = float(new_val)

                    if original_row[col] != new_val:
                        df.at[row_index, col] = new_val
                        changes_made = True

                if changes_made:
                    st.session_state.df = df  # Update session state df
                    st.success("Row updated!")
                else:
                    st.warning("No changes detected.")

            st.write("### Current DataFrame")
            st.dataframe(st.session_state.df)

            # --- Save All to Training Data ---
            st.subheader("📥 Save All Processed Data to Training Set")
            st.caption("Saving the data will fine-tune the model tailored for your business. The Model will start working once teh number of transactions are greater than 100. This is done because intializing a model with little transactions forces the model to overgeneralize.")
            if st.button("Save All to Training Data"):
                if {"Memo", "Predicted Account"}.issubset(df.columns):
                    training_data = df[["Memo", "Predicted Account"]].rename(
                        columns={"Memo": "Description", "Predicted Account": "Category"}
                    )
                    bookkeeper_brain.update_training_data(training_data)
                    bookkeeper_brain.train_and_save_model()
                    st.success("All data saved and model retrained.")
                else:
                    st.error("Required columns ('Memo', 'Predicted Account') missing.")

    else:
        st.info("Please upload a file.")
else:
    st.info("The file type you have uploaded is not supported")