import streamlit as st
import pandas as pd
from io import BytesIO
import data_cleaner  # your custom module
import classify_transactions  # your categorizer module
import bookkeeper_brain  # your model training module
import os
import report_generator  # your report generation module
from streamlit_option_menu import option_menu
import plotly.express as px
import seaborn as sns
from pathlib import Path


def extract_categories_from_uploaded_chart(uploaded_file):
    try:
        # ✅ FIX: Check if it's a list and grab the first file
        if isinstance(uploaded_file, list):
            uploaded_file = uploaded_file[0]

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Try to auto-detect the category column
        category_column = None
        for col in df.columns:
            if "category" in col.lower():
                category_column = col
                break

        if category_column is None:
            st.warning(
                "Could not detect a 'Category' column. Please make sure your file has one.")
            return None

        categories = df[category_column].dropna().unique().tolist()
        categories = [str(cat).strip()
                      for cat in categories if isinstance(cat, str)]
        return categories

    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None


def run():

    tab1, tab2, tab3, tab4 = st.tabs(["Main", "Help", "About", "Analytics"])
    st.markdown(
        """
    <style>
        /* When sidebar is open */
        [data-testid="stSidebar"][aria-expanded="true"] {
            width: 450px !important;
        }

        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 450px !important;
        }

        /* When sidebar is collapsed */
        [data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(-100%) !important;
        }
    </style>
    """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        selected = option_menu("Chart of Accounts", ["Default", "Upload Custom"],
                               icons=['pip-fill', 'bi bi-upload'], menu_icon="Journal bookmark", default_index=1)

        categories = []

        if selected == "Upload Custom":
            uploaded_file = st.file_uploader("Upload Custom Chart of Accounts", type=[
                                             "xlsx", "xls", "csv"], key="custom_upload")
            if uploaded_file:
                categories = extract_categories_from_uploaded_chart(
                    uploaded_file)
                if categories:
                    st.success(f"Loaded {len(categories)} custom categories.")
                    st.write(categories)
                else:
                    st.error(
                        "⚠️ Failed to load categories. Using default categories instead.")
        if not categories:
            categories = [  # Default list
                "Sales Revenue", "Service Income", "Other Income", "Cost of Goods Sold", "Purchases",
                "Materials and Supplies", "Subcontractor Costs", "Freight and Shipping (COGS related)",
                "Advertising", "Bank Fees", "Contract Labor", "Depreciation Expense", "Insurance (Business)",
                "Interest Expense", "Legal and Professional Fees", "Office Supplies",
                "Rent or Lease - Vehicles, Machinery, Equipment", "Rent or Lease - Other Business Property",
                "Repairs and Maintenance", "Salaries and Wages", "Taxes and Licenses", "Travel",
                "Meals and Entertainment", "Utilities", "Internet and Phone", "Education and Training",
                "Business Dues and Subscriptions", "Vehicle Expenses", "Home Office Expenses",
                "Postage and Shipping", "Software Expense", "Miscelleanous City Taxes", "Owner's Draw",
                "Estimated Tax Payments", "Income Tax Expense", "Payroll Taxes", "Business Loan Interest",
                "Amortization", "Ask My Accountant"
            ]

        st.markdown("---")
        st.markdown("### 👨‍💻 How RoboLedger Works For YOU! 👨‍💻")
        st.markdown(
            "RoboLedger is your AI-powered bookkeeping assistant, designed to simplify your financial management. Here's how it works:")
        st.markdown(
            "We have two AI models working together to categorize your transactions accurately.")
        st.markdown(
            "One baseline model which is able to categorize everything regardless of prior information.")
        st.markdown(
            "One custom model which learns from your specific business data to provide tailored categorizations.")
        st.markdown("When you upload your transaction data, RoboLedger first uses the custom model to categorize your transactions based on patterns it has learned from your previous data.")
        st.markdown("If the custom model is unsure about a transaction or if it hasn't seen similar data before, it falls back to the baseline model to ensure every transaction is categorized.")
        st.markdown("This dual-model approach ensures that you get the most accurate and relevant categorizations possible, helping you maintain clear and organized financial records.")
        st.markdown(
            "Our mission: make bookkeeping something that should take a couple of clicks, not hours.")
        st.markdown("---")

        FEEDBACK_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeCHmPbM_RR1_rgu13Zuobka3GmImsfXLceqX7F--QaVc89gg/viewform"
        st.link_button("📝 Leave feedback", FEEDBACK_URL,
                       use_container_width=False)
        if st.button("💖 Donate to Us 💖"):
            st.markdown(
                "Thank you for considering a donation! Please visit [WEBSITE] to support our work.")

    def main_run():
        st.subheader("📚 Your AI-powered financial assistant 📚")
        # st.subheader("Choose a file and view the contents below")

        # --- Upload Type Selection ---
        upload_type = st.radio("Choose file type to upload:", ("Excel", "QBO"))
        st.markdown("---")
        st.subheader("🔍 Reconciliation Check")

        col1, col2 = st.columns(2)

        with col1:
            starting_balance = st.number_input(
                "🏁 Starting Balance 🏁", value=0.0)

        with col2:
            ending_balance = st.number_input("🏁 Ending Balance 🏁", value=0.0)

        reconciliation_result = None

        if "df" in st.session_state:
            df = st.session_state.df
            if "Amount" in df.columns:
                total_activity = df["Amount"].sum()
                expected_ending = starting_balance + total_activity
                # tolerance for rounding
                reconciled = abs(expected_ending - ending_balance) < 0.01

                st.write(
                    f"**Total Activity (sum of Amount column):** {total_activity:,.2f}")
                st.write(
                    f"**Expected Ending Balance:** {expected_ending:,.2f}")
                st.write(f"**Provided Ending Balance:** {ending_balance:,.2f}")

                if reconciled:
                    st.success(
                        "✅ Reconciled! Ending balance matches the expected total.")
                else:
                    st.error(
                        "❌ Not Reconciled. Please check your entries or data.")
            else:
                st.warning(
                    "⚠️ Column 'Amount' not found in uploaded data. Cannot perform reconciliation.")
        else:
            pass

        # Shared preprocessing function
        @st.cache_data
        def preprocess_and_categorize(df_input):
            df_copy = df_input.copy()

            # Clean and normalize memos
            df_copy["Memo"] = df_copy["Memo"].fillna(
                "").astype(str).apply(data_cleaner.janitor)
            # Convert to uppercase for consistency
            df_copy["Memo"] = df_copy["Memo"].str.upper()
            memos = df_copy["Memo"].tolist()

            if os.path.exists(bookkeeper_brain.MODEL_PATH):
                # Primary prediction
                primary_preds = bookkeeper_brain.categorize_batch(memos)
            else:
                primary_preds = [None] * len(memos)  # fallback mode only

            # Fallback prediction
            fallback_preds = classify_transactions.categorize_batch(
                memos, categories)

            # Combine: use primary if not None/empty, else fallback
            final_preds = [
                primary if primary not in [None, "", "unknown"]
                else fallback
                for primary, fallback in zip(primary_preds, fallback_preds)
            ]

            df_copy["Predicted Account"] = final_preds

            return df_copy

        if upload_type == "Excel":

            uploaded_file = st.file_uploader(
                "Upload an Excel or CSV file", type=["xlsx", "xls", "csv"])
            SAMPLE_PATH = Path(__file__).parent / "Fake Transactions" / "dummy_data_pt2.xlsx"
            with st.container():
                st.write("Don’t have a file handy? Download a small demo file and try the workflow before using your own data.")
                with open(SAMPLE_PATH, "rb") as f:
                    st.download_button(
                        label="⬇️ Download sample transactions (.xlsx)",
                        data=f,
                        file_name="sample_transactions.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

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
                    row_index_input = st.text_input(
                        "Enter row index to edit", value=str(default_row))

                    try:
                        row_index = int(row_index_input)
                        if row_index not in df.index:
                            st.warning(
                                f"Row index {row_index} not found. Using default {default_row}.")
                            row_index = default_row
                    except ValueError:
                        st.warning("Invalid row index input. Using default.")
                        row_index = default_row

                    updated_values = {}
                    for col in df.columns:
                        original_value = df.at[row_index, col]
                        if pd.api.types.is_numeric_dtype(df[col]):
                            new_val = st.number_input(f"{col}", value=float(
                                original_value), key=f"{col}_{row_index}")
                        else:
                            new_val = st.text_input(f"{col}", value=str(
                                original_value), key=f"{col}_{row_index}")
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
                    st.caption("Saving the data will fine-tune the model tailored for your business. The Model will start working once the number of transactions are greater than 100. This is done because intializing a model with little transactions forces the model to overgeneralize.")
                    if st.button("Save All to Training Data"):
                        if {"Memo", "Predicted Account"}.issubset(df.columns):
                            training_data = df[["Memo", "Predicted Account"]].rename(
                                columns={"Memo": "Description",
                                         "Predicted Account": "Category"}
                            )
                            bookkeeper_brain.update_training_data(
                                training_data)
                            bookkeeper_brain.train_and_save_model()
                            st.success("All data saved and model retrained.")
                        else:
                            st.error(
                                "Required columns ('Memo', 'Predicted Account') missing.")
                    try:
                        st.subheader(
                            "🏦 Download Profit & Loss Excel Template 🏦")
                        st.caption("Download a Profit & Loss Excel template based on your categorized transactions. You do not need to fill out the template, it is automatically generated based on your transactions. You can use this for filing your taxes or for your accounting purposes.")
                        excel_bytes = report_generator.excel_template_generator(
                            df)

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
        st.subheader(" How to Use RoboLedger ")
        st.write("1. **Upload Chart of Accounts**: Start by uploading your custom Chart of Accounts in the sidebar. Ensure the file has a single column named 'Category'. If you don't upload one, the default categories will be used.")
        st.write("2. **Upload Transaction File**: Choose the file type (Excel or QBO) and upload your transaction data. The file should contain at least 'Date', 'Memo', and 'Amount' columns.")
        st.write("3. **Reconciliation Check**: Input your starting and ending balances to verify that your transactions reconcile correctly.")
        st.write("4. **Review and Edit Transactions**: After uploading, review the categorized transactions. You can edit any row directly within the app to correct misclassifications.")
        st.write("5. **Save to Training Data**: Once you're satisfied with the categorizations, save the processed data to the training set. This will help fine-tune the AI model for your specific business needs.")
        st.write(
            "6. **Download Reports**: Finally, download the generated Profit & Loss Excel template for your records.")

    with tab3:
        st.write("RoboLedger is the synthesis between AI and bookkeeping, designed to streamline your financial management. It automates data entry, categorizes transactions, and provides insights into your business finances. With RoboLedger, you can focus on growing your business while we handle the numbers.")
        st.write("**My Business is very specific, how can I use this?**")
        st.write("RoboLedger is designed to adapt to your unique business needs. By uploading your transaction data, the AI learns your specific categorization patterns, ensuring that it aligns with your financial practices. This means you can trust RoboLedger to handle your bookkeeping accurately and efficiently, tailored to your business model.")
        st.write("**What else RoboLedger do?**")
        st.write("RoboLedger not only categorizes transactions but also provides reconciliation checks. The team of developers are currently working on invoice and receipt processing, expense tracking, and financial reporting features. This will allow you to manage your finances comprehensively, all in one platform.")
        st.write("**How can I contribute to RoboLedger?**")
        st.write("We welcome contributions to RoboLedger! You can help by providing feedback, suggesting features, or even contributing code. If you're interested in collaborating, please reach out to us through our GitHub repository or contact us directly. Your input is invaluable in making RoboLedger better for everyone.")
    with tab4:
        if "df" in st.session_state:
            df = st.session_state.df
            account_summary = df["Predicted Account"].value_counts(
            ).reset_index()
            account_summary.columns = ["Predicted Account", "Count"]
            account_counts = df["Predicted Account"].value_counts(
            ).reset_index()
            account_counts.columns = ["Predicted Account", "Count"]
            if not df.empty:
                try:
                    fig = px.histogram(
                        df,
                        x="Amount",
                        nbins=30,
                        marginal="box",
                        title="Transaction Amount Distribution",
                    )
                    fig.update_layout(
                        xaxis_title="Amount",
                        yaxis_title="Frequency",
                        bargap=0.1,
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    fig = px.pie(
                        account_summary,
                        names="Predicted Account",
                        values="Count",
                        title="Transaction Count per Account",
                        hole=0.4  # Optional: makes it a donut chart
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    fig = px.bar(
                        account_counts,
                        x="Predicted Account",
                        y="Count",
                        title="Frequency of Predicted Accounts",
                        text="Count",
                        color="Predicted Account"  # Optional: adds color by category
                    )

                    fig.update_layout(
                        xaxis_title="Predicted Account",
                        yaxis_title="Frequency",
                        showlegend=False
                    )

                    st.plotly_chart(fig, use_container_width=True)

                except Exception as e:
                    st.error(f"Error generating plot: {e}")
            else:
                st.info(
                    "No data available for analytics. Please upload and process a file first.")
        else:
            st.info(
                "No data available for analytics. Please upload and process a file first.")


run()
