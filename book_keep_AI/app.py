import streamlit as st
import pandas as pd
import xlsxwriter
import io  # for in-memory bytes buffer

st.title("RoboLedger")
st.subheader("Your AI-powered financial assistant")
st.subheader("Choose a file and view the contents below")

# Select upload type
upload_type = st.radio("Choose file type to upload:", ("PDF", "Excel"))

# PDF Upload
if upload_type == "PDF":
    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")
    if pdf_file is not None:
        st.success("PDF uploaded successfully!")
        st.write("File name:", pdf_file.name)
        # Optional: PDF processing can go here
    else:
        st.info("Please upload a PDF file.")

# Excel Upload
elif upload_type == "Excel":
    excel_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls", "csv"])
    if excel_file is not None:
        try:
            df = pd.read_excel(excel_file)

            st.success("Excel uploaded successfully!")
            st.write("Preview of Excel data:")
            st.dataframe(df)

            # Proceed if DataFrame is not empty
            if not df.empty:
                st.subheader("Edit a Row in the Excel File")

                # Select row index manually
                row_index = int(st.text_input("Enter row index to edit", value=int(df.index.min())))

                # Editable inputs for each column
                updated_values = {}
                for col in df.columns:
                    val = df.loc[row_index, col]
                    if pd.api.types.is_numeric_dtype(df[col]):
                        updated = st.number_input(f"{col}", value=float(val), key=f"{col}_{row_index}")
                    else:
                        updated = st.text_input(f"{col}", value=str(val), key=f"{col}_{row_index}")
                    updated_values[col] = updated

                # Save changes
                if st.button("Save Changes"):
                    for col, new_val in updated_values.items():
                        df.loc[row_index, col] = new_val
                    st.success("Row updated!")

                st.write("### 🔄 Updated DataFrame")
                st.dataframe(df)
                for col, new_val in updated_values.items():
                    df.loc[row_index, col] = new_val
                st.success("Row updated!")

                # Optional: add to training data
                if "Description" in df.columns and "Predicted Account" in df.columns:
                    new_training_row = pd.DataFrame([{
                    "Description": df.loc[row_index, "Description"],
                    "Category": df.loc[row_index, "Predicted Account"]
                 }])
                    update_training_data(new_training_row)
                    train_and_save_model()
                    st.info("Training data updated and model retrained.")
                
        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
    else:
        st.info("Please upload an Excel file.")
