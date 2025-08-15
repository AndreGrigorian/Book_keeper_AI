import streamlit as st
import pandas as pd
import bookkeeper_brain
import classify_transactions
import data_cleaner

st.title("🫨 RoboLedger 🫨")
st.subheader("Your AI-powered financial assistant")
st.subheader("Choose a file and view the contents below")

# --- Upload Type Selection ---
upload_type = st.radio("Choose file type to upload:", ("PDF", "Excel"))

# --- PDF Upload ---
if upload_type == "PDF":
    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")

    if pdf_file:
        st.success("PDF uploaded successfully!")
        st.write("File name:", pdf_file.name)
        # Optional: Add PDF processing logic here
    else:
        st.info("Please upload a PDF file.")

# --- Excel Upload ---
elif upload_type == "Excel":
    excel_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls", "csv"])

    if excel_file:
        try:
            df_raw = pd.read_excel(excel_file)

            # --- Cached cleaning & categorization ---
            @st.cache_data
            def preprocess_and_categorize(df_input):
                df_copy = df_input.copy()
                df_copy["Memo"] = df_copy["Memo"].apply(data_cleaner.janitor)
                df_copy["Predicted Account"] = df_copy["Memo"].map(classify_transactions.categorize)
                return df_copy

            df = preprocess_and_categorize(df_raw)

            st.success("Excel uploaded and processed successfully!")
            st.write("Preview of processed data:")
            st.dataframe(df)

            if not df.empty:
                st.subheader("Edit a Row in the Excel File")

                # User input: row index
                row_index = int(st.text_input("Enter row index to edit", value=int(df.index.min())))

                # Editable inputs for each column
                updated_values = {}
                for col in df.columns:
                    original_val = df.loc[row_index, col]
                    if pd.api.types.is_numeric_dtype(df[col]):
                        new_val = st.number_input(f"{col}", value=float(original_val), key=f"{col}_{row_index}")
                    else:
                        new_val = st.text_input(f"{col}", value=str(original_val), key=f"{col}_{row_index}")
                    updated_values[col] = new_val

                # Save Changes Button
                if st.button("Save Changes"):
                    original_row = df.loc[row_index].copy()
                    changes_made = False

                    for col, new_val in updated_values.items():
                        if str(original_row[col]) != str(new_val):
                            df.loc[row_index, col] = new_val
                            changes_made = True

                    if changes_made:
                        st.success("Row updated!")

                        # Update training data if relevant columns exist
                        if "Memo" in df.columns and "Predicted Account" in df.columns:
                            new_training_row = pd.DataFrame([{
                                "Description": df.loc[row_index, "Memo"],
                                "Category": df.loc[row_index, "Predicted Account"]
                            }])
                            bookkeeper_brain.update_training_data(new_training_row)
                            bookkeeper_brain.train_and_save_model()
                            st.info("Training data updated and model retrained.")
                    else:
                        st.warning("No changes detected. Nothing was updated.")

                    # Show updated DataFrame
                    st.write("### Updated DataFrame")
                    st.dataframe(df)

        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
    else:
        st.info("Please upload an Excel file.")
