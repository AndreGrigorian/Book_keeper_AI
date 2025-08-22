import streamlit as st
import pandas as pd
from io import BytesIO
import data_cleaner  # your custom module
import classify_transactions  # your categorizer module
import bookkeeper_brain  # your model training module
import os
import report_generator  # your report generation module
from streamlit_option_menu import option_menu


def run():

    tab1, tab2, tab3 = st.tabs(["Main", "Receipt Categorizer", "About Section"])
    st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 500px !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            width: 500px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
    )
    with st.sidebar:
        selected = option_menu("Chart of Accounts", ["Default", 'Upload Custom'], 
        icons=['pip-fill', 'bi bi-upload'], menu_icon="Journal bookmark", default_index=1)
        selected
        if selected == "Upload Custom":
            uploaded_file = st.file_uploader("Upload Custom Chart of Accounts", type=["xlsx", "xls", "csv"], key="custom_upload")
        st.markdown("---")
        st.markdown("### 👨‍💻 How RoboLedger Works For YOU! 👨‍💻")
        st.markdown("In order for RoboLedger to work, the documents you upload must have follow our formating guidelines. Chart of Accounts must be in a single column with the header 'Category'. Transaction documents must have at least the following columns: 'Date', 'Memo', and 'Amount'.")
        st.markdown("---")  # optional divider line
    
        if st.button("💖 Donate to Us"):
            st.markdown("Thank you for considering a donation! Please visit [WEBSITE] to support our work.")
    def main_run():
        st.subheader("📚 Your AI-powered financial assistant 📚")
        # st.subheader("Choose a file and view the contents below")
    
        # --- Upload Type Selection ---
        upload_type = st.radio("Choose file type to upload:", ("Excel", "QBO"))
        st.markdown("---")
        st.subheader("🔍 Reconciliation Check")

        col1, col2 = st.columns(2)

        with col1:
            starting_balance = st.number_input("🏁 Starting Balance 🏁", value=0.0)

        with col2:
            ending_balance = st.number_input("🏁 Ending Balance 🏁", value=0.0)

        reconciliation_result = None

        if "df" in st.session_state:
                df = st.session_state.df
                if "Amount" in df.columns:
                    total_activity = df["Amount"].sum()
                    expected_ending = starting_balance + total_activity
                    reconciled = abs(expected_ending - ending_balance) < 0.01  # tolerance for rounding

                    st.write(f"**Total Activity (sum of Amount column):** {total_activity:,.2f}")
                    st.write(f"**Expected Ending Balance:** {expected_ending:,.2f}")
                    st.write(f"**Provided Ending Balance:** {ending_balance:,.2f}")

                    if reconciled:
                        st.success("✅ Reconciled! Ending balance matches the expected total.")
                    else:
                        st.error("❌ Not Reconciled. Please check your entries or data.")
                else:
                    st.warning("⚠️ Column 'Amount' not found in uploaded data. Cannot perform reconciliation.")
        else:
                pass

        # Shared preprocessing function
        @st.cache_data
        def preprocess_and_categorize(df_input):
            df_copy = df_input.copy()

            # Clean and normalize memos
            df_copy["Memo"] = df_copy["Memo"].fillna("").astype(str).apply(data_cleaner.janitor)
            df_copy["Memo"] = df_copy["Memo"].str.upper()  # Convert to uppercase for consistency
            memos = df_copy["Memo"].tolist()

            if os.path.exists(bookkeeper_brain.MODEL_PATH):
                # Primary prediction
                primary_preds = bookkeeper_brain.categorize_batch(memos)
            else:
                primary_preds = [None] * len(memos)  # fallback mode only

            # Fallback prediction
            fallback_preds = classify_transactions.categorize_batch(memos)

            # Combine: use primary if not None/empty, else fallback
            final_preds = [
                primary if primary not in [None, "", "unknown"]
                else fallback
                for primary, fallback in zip(primary_preds, fallback_preds)
            ]

            df_copy["Predicted Account"] = final_preds

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
                    try:
                        excel_bytes = report_generator.excel_template_generator(df)

                        # Create a download button
                        st.download_button(
                            label="💾 Download P&L Excel Template 💾",
                            data=excel_bytes,
                            file_name="P&L_Template.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                    except ValueError as e:
                        st.error(f"Error: {e}")
            else:
                st.info("Please upload a file.")
        else:
            st.info("The file type you have uploaded is not supported")

    with tab1:
        main_run()

    with tab2:
        st.write("This tab is for categorizing receipts and transactions.")
        
        

    with tab3:
        st.write("RoboLedger is the synthesis between AI and bookkeeping, designed to streamline your financial management. It automates data entry, categorizes transactions, and provides insights into your business finances. With RoboLedger, you can focus on growing your business while we handle the numbers.")
        st.write("**My Business is very specific, how can I use this?**")
        st.write("RoboLedger is designed to adapt to your unique business needs. By uploading your transaction data, the AI learns your specific categorization patterns, ensuring that it aligns with your financial practices. This means you can trust RoboLedger to handle your bookkeeping accurately and efficiently, tailored to your business model.")
        st.write("**What else RoboLedger do?**")
        st.write("RoboLedger not only categorizes transactions but also provides reconciliation checks. The team of developers are currently working on invoice and receipt processing, expense tracking, and financial reporting features. This will allow you to manage your finances comprehensively, all in one platform.")
        st.write("**How can I contribute to RoboLedger?**")
        st.write("We welcome contributions to RoboLedger! You can help by providing feedback, suggesting features, or even contributing code. If you're interested in collaborating, please reach out to us through our GitHub repository or contact us directly. Your input is invaluable in making RoboLedger better for everyone.")
