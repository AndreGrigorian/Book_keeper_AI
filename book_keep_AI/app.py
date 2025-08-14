import streamlit as st
import pandas as pd

st.title("🤖 RoboLedger 🤖")
st.subheader("Choose a file and view the contents below")


# Select upload type
upload_type = st.radio("Choose file type to upload:", ("PDF", "Excel"))

# PDF Upload
if upload_type == "PDF":
    pdf_file = st.file_uploader("Upload a PDF file", type="pdf")
    if pdf_file is not None:
        st.success("PDF uploaded successfully!")
        st.write("File name:", pdf_file.name)
        # Optional: You could add PDF processing here later (e.g., extract text)
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
        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
    else:
        st.info("Please upload an Excel file.")