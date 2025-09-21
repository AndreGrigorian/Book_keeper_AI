import streamlit as st
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import data_cleaner  # your custom module
import classify_transactions  # your categorizer module
import bookkeeper_brain  # your model training module
import os
import re
import ast
from dotenv import load_dotenv
from openai import OpenAI
import openai
import io
import report_generator  # your report generation module
from streamlit_option_menu import option_menu
import plotly.express as px
import seaborn as sns
from pathlib import Path
from datetime import date
import contextlib
import zipfile
import qbo_parser
import time
import itertools
from streamlit_chat import message

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



def find_subset_sum(transactions, target, tolerance=0.00, max_time=10.0):
    start_time = time.time()

    def backtrack(start, current_sum, path):
        # Stop if time exceeded
        if time.time() - start_time > max_time:
            return None
        if abs(current_sum - target) <= tolerance:
            return path
        if current_sum > target + tolerance:
            return None
        for i in range(start, len(transactions)):
            result = backtrack(i + 1, current_sum + transactions[i], path + [i])
            if result is not None:
                return result
        return None

    return backtrack(0, 0.0, [])


def find_subset_sum_ordered(transactions, target, tolerance=0.00, max_time=10.0):
    start_time = time.time()
    n = len(transactions)

    # Try subsets starting from largest size to smallest
    for r in range(n, 0, -1):
        if time.time() - start_time > max_time:
            return None

        for indices in itertools.combinations(range(n), r):
            subset_sum = sum(transactions[i] for i in indices)

            if abs(subset_sum - target) <= tolerance:
                return list(indices)

    return None




def run():
    st.markdown("# ```🤖 RoboLedger © 🤖```")
    st.markdown("```AI-Powered Bookkeeping and Reconciliation```")
    st.markdown("```FREE Access • No Credit Card Required • Open Source```")
    matched_indices = None
    tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Getting Started", "Main", "Reconcile", "Analytics", "Meet RoboLedger", "Help", "About"])
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

    FEEDBACK_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeCHmPbM_RR1_rgu13Zuobka3GmImsfXLceqX7F--QaVc89gg/viewform"
    DONATION_URL = "https://buymeacoffee.com/roboledger"
    st.divider()
    st.caption(
        f"© {date.today().year} RoboLedger • 📝 [Leave feedback]({FEEDBACK_URL}) • 💖[Donate to Us]({DONATION_URL}) •")

    with st.sidebar:
        selected = option_menu("Chart of Accounts", ["Default", "Upload Custom"],
                               icons=['pip-fill', 'bi bi-upload'], menu_icon="Journal bookmark", default_index=0)
        st.markdown("---")
        reports = option_menu("Reports", ["Profit & Loss", "Balance Sheet", "Cash Flow", "Trial Balance"],
                              icons=['file-earmark-text', 'file-earmark-spreadsheet', 'file-earmark-bar-graph'], menu_icon="file-earmark-text", default_index=0)
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
    with tab0:
        st.markdown("## ```Getting Started with RoboLedger```")
        st.markdown("---")
        st.video("https://www.youtube.com/watch?v=lnhUs7_bT5s")
    with tab1:
        
        # st.subheader("Choose a file and view the contents below")

        # --- Upload Type Selection ---
        upload_type = st.radio("Choose file type to upload:", ("Excel", "QBO"))
        st.markdown("---")

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

        if upload_type == "Excel" or upload_type == "QBO":
            if upload_type == "QBO":
                st.info("ℹ️ QBO upload selected. Please upload a ZIP file containing your QBO files.")
            uploaded_file = st.file_uploader(
                "Upload an Excel or CSV file", type=["xlsx", "xls", "csv", "zip"])
            SAMPLE_PATH = Path(__file__).parent / \
                "Fake Transactions" / "dummy_data_pt2.xlsx"
            with st.container():
                st.write(
                    "Don’t have a file handy? Download a small demo file and try the workflow before using your own data.")
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
                            df_raw['Amount'] = df_raw['Amount'].astype(float)
                        elif uploaded_file.name.endswith(".csv"):
                            df_raw = pd.read_csv(uploaded_file)
                            df_raw['Amount'] = df_raw['Amount'].astype(float)
                        elif uploaded_file.name.endswith(".zip"):
                            try:
                                # ✅ Ensure the uploaded file is passed as a binary buffer
                                with zipfile.ZipFile(uploaded_file) as z:
                                    qbo_files = [f for f in z.namelist() if f.endswith(".qbo")]

                                    if not qbo_files:
                                        st.warning("⚠️ No .qbo files found inside the ZIP archive.")
                                    else:
                                        qbo_filename = qbo_files[0]
                                        with z.open(qbo_filename) as qbo_file:
                                            df_raw = qbo_parser.parse_qbo_file(qbo_file)
                                            df_raw['Amount'] = df_raw['Amount'].astype(float)
                                            if not df_raw.empty:
                                                st.success("✅ Parsed QBO file successfully!")
                                                st.dataframe(df_raw)
                                            else:
                                                st.warning("⚠️ No transactions found in QBO file.")
                            except zipfile.BadZipFile:
                                st.error("❌ Uploaded file is not a valid ZIP archive.")
                            except Exception as e:
                                st.error(f"❌ Unexpected error: {e}")                
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
                st.info("Please upload a file to get started.")
        else:
            st.info("The file type you have uploaded is not supported at the moment. Please use the Excel upload option instead.")

    if "original_amounts" not in st.session_state and "df" in st.session_state:
        st.session_state.original_amounts = st.session_state.df["Amount"].copy(
        )
    with tab2:
        df = st.session_state.get("df")
        # ----
        # ---

        if isinstance(df, pd.DataFrame) and not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                beginning_balance = st.number_input(
                    "Beginning Balance", value=0.00, format="%.2f")
            with col2:
                ending_balance = st.number_input(
                    "Ending Balance", value=0.00, format="%.2f")
            
            
            
            if st.button("📚 AutoReconcile 📚"):
                target = ending_balance - beginning_balance
                matched_indices = find_subset_sum_ordered(df["Amount"].tolist(), target)

                if matched_indices is not None:
                    df["Selected"] = False  # Reset
                    for i in matched_indices:
                        df.at[i, "Selected"] = True
                    st.success("✅ Match found and selected.")
                else:
                    st.warning("⚠️ No matching combination found.")
                # Add a checkbox column to the dataframe
            if "Selected" not in df.columns:
                df["Selected"] = False
            if "all_selected" not in st.session_state:
                st.session_state.all_selected = False



            switch_sign = st.toggle("🔁 Switch Debits and Credits", value=False)

            # 🔄 Apply sign change if toggled
            if switch_sign:
                df["Amount"] = st.session_state.original_amounts * -1
            else:
                df["Amount"] = st.session_state.original_amounts.copy()
            # Button to toggle select all/deselect all
            if st.button("Select All" if not st.session_state.all_selected else "Deselect All"):
                st.session_state.all_selected = not st.session_state.all_selected
                df["Selected"] = st.session_state.all_selected

            st.subheader("Transactions")
            edited_df = st.data_editor(
                df,
                column_config={
                    "Selected": st.column_config.CheckboxColumn("✓"),
                    "Amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
                },
                use_container_width=True,
                hide_index=True,
            )

            # Filter selected transactions
            selected = edited_df[edited_df["Selected"]
                                 == True]["Amount"].tolist()
            
            cleared_total = sum(selected)
            expected_cleared = ending_balance - beginning_balance
            difference = round(cleared_total - expected_cleared, 2)

            is_reconciled = difference == 0.00

            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            col1.metric("✅ Cleared Total", f"${cleared_total:.2f}")
            col2.metric("📘 Expected Total", f"${expected_cleared:.2f}")
            col3.metric("🔁 Difference", f"${difference:.2f}")

            if is_reconciled:
                st.success("🎉 Reconciled!")
            else:
                st.warning("❌ Not Reconciled")
        else:
            st.info(
                "No data available for reconciliation. Please upload and process a file first.")

    with tab5:
        st.subheader(" How to Use RoboLedger ")
        st.write("1. **Upload Chart of Accounts**: Start by uploading your custom Chart of Accounts in the sidebar. Ensure the file has a single column named 'Category'. If you don't upload one, the default categories will be used.")
        st.write("2. **Upload Transaction File**: Choose the file type (Excel or QBO) and upload your transaction data. The file should contain at least ```Date```, ```Memo```, and ```Amount``` columns.")
        st.write("3. **Reconciliation Check**: Input your starting and ending balances to verify that your transactions reconcile correctly.")
        st.write("4. **Review and Edit Transactions**: After uploading, review the categorized transactions. You can edit any row directly within the app to correct misclassifications.")
        st.write("5. **Save to Training Data**: Once you're satisfied with the categorizations, save the processed data to the training set. This will help fine-tune the AI model for your specific business needs.")
        st.write("6. **Download Reports**: Finally, download the generated Profit & Loss Excel template for your records.")

    with tab6:
        st.write("RoboLedger is the synthesis between AI and bookkeeping, designed to streamline your financial management. It automates data entry, categorizes transactions, and provides insights into your business finances. With RoboLedger, you can focus on growing your business while we handle the numbers.")
        st.write("**My Business is very specific, how can I use this?**")
        st.write("RoboLedger is designed to adapt to your unique business needs. By uploading your transaction data, the AI learns your specific categorization patterns, ensuring that it aligns with your financial practices. This means you can trust RoboLedger to handle your bookkeeping accurately and efficiently, tailored to your business model.")
        st.write("**What else RoboLedger do?**")
        st.write("RoboLedger not only categorizes transactions but also provides reconciliation checks. The team of developers are currently working on invoice and receipt processing, expense tracking, and financial reporting features. This will allow you to manage your finances comprehensively, all in one platform.")
        st.write("**How can I contribute to RoboLedger?**")
        st.write("We welcome contributions to RoboLedger! You can help by providing feedback, suggesting features, or even contributing code. If you're interested in collaborating, please reach out to us through our GitHub repository or contact us directly. Your input is invaluable in making RoboLedger better for everyone.")

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
    with tab3:
        df = st.session_state.get("df")

        # Make sure it's not empty
        if isinstance(df, pd.DataFrame) and not df.empty:
            # Sum of Amounts per Predicted Account
            account_summary = df.groupby("Predicted Account")[
                "Amount"].sum().reset_index()
            account_summary.columns = ["Predicted Account", "Total Amount"]

            # Histogram of Amounts
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

            account_summary_abs = df.groupby("Predicted Account")["Amount"].apply(
                lambda x: x.abs().sum()).reset_index()
            account_summary_abs.columns = ["Predicted Account", "Total Amount"]

            fig = px.pie(
                account_summary_abs,
                names="Predicted Account",
                values="Total Amount",
                title="Total Amount per Predicted Account (Absolute Values)",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

            # Bar chart (sums instead of counts)
            fig = px.bar(
                account_summary,
                x="Predicted Account",
                y="Total Amount",
                title="Total Amount by Predicted Account",
                text="Total Amount",
                color="Predicted Account"
            )
            fig.update_layout(
                xaxis_title="Predicted Account",
                yaxis_title="Total Amount",
                showlegend=False
            )
            df = st.session_state.df
            st.plotly_chart(fig, use_container_width=True)
            df['Date'] = pd.to_datetime(df['Date'])

            # Sum amount per day
            daily_expenses = df.groupby('Date')['Amount'].sum().reset_index()

            fig = px.line(
                daily_expenses,
                x='Date',
                y='Amount',
                title='Expenses Over Time',
                markers=True
            )
            fig.update_layout(
                xaxis_title='Date',
                yaxis_title='Total Daily Expenses',
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(
                "No data available for analytics. Please upload and process a file first.")

    with tab4:
        load_dotenv()  # loads OPENAI_API_KEY from .env


        def get_secret(name: str, default=None):
            # 1) env var wins (works everywhere, including Docker/Render/etc.)
            v = os.getenv(name)
            if v:
                return v
            # 2) only try Streamlit secrets if file exists
            try:
                return st.secrets.get(name, default)
            except FileNotFoundError:
                return default


        OPENAI_API_KEY = get_secret("OPENAI_API_KEY")


        client = OpenAI(api_key=OPENAI_API_KEY)

        st.session_state.setdefault("past", [])
        st.session_state.setdefault("generated", [])

        def ask_gpt_for_code(user_input, df_preview):
            system_prompt = f"""
        You are a Python data analyst. The user provides a pandas DataFrame called `df`.
        They ask a question about the data.
        Your job is to generate only Python code that uses `df` to answer the question.
        Requirements:
        - Do not include markdown or explanations.
        - Assign the final output to a variable named `result`.
        - Do not use print().
        - import any libraries you need (e.g. pandas as pd, matplotlib.pyplot as plt).
        - import pandas, numpy, matplotlib, seaborn, plotly whenever you generate a plot
        DataFrame preview:
        {df_preview}
        """
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]

            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0,
            )

            base_imports = (
            "import pandas as pd\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n"
            "import plotly.express as px\n"
            "import scipy.stats as stats\n"
            )

            raw_code = response.choices[0].message.content.strip()
            return base_imports + "\n" + raw_code


        def clean_code(code: str) -> str:
            """
            Extract and clean Python code from GPT response.
            Removes markdown fences and trims output text.
            """
            code = re.sub(r"^```(?:python)?\s*", "", code, flags=re.MULTILINE)
            code = code.replace("```", "")
            code = code.strip()

            split_keywords = ["Output:", "Result:", "Explanation:", "Answer:"]
            for kw in split_keywords:
                if kw in code:
                    code = code.split(kw)[0].strip()

            return code


        def is_expression(code: str) -> bool:
            try:
                parsed = ast.parse(code)
                return len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr)
            except Exception:
                return False


        def run_code_on_df(code, df):
            import matplotlib.pyplot as plt
            import pandas as pd
            import numpy as np
            local_vars = {"df": df.copy()}
            f = io.StringIO()
            fig = None

            if is_expression(code):
                code = f"result = {code}"

            try:
                with contextlib.redirect_stdout(f):
                    exec(code, {}, local_vars)

                output = f.getvalue().strip()

                # Detect if a matplotlib plot was created
                if ".show" in code or "fig." in code or isinstance(local_vars.get("result"), plt.Axes):
                    fig = plt.gcf()
                    ## plt.clf()
                    output = output or "📊 Plot generated."

                elif "result" in local_vars:
                    output = output or str(local_vars["result"])

                else:
                    output = output or "✅ Code executed but no result was assigned to `result`."

                return output, fig

            except Exception as e:
                return f"❌ Error running code: {e}\n\nCode:\n{code}", None



        # Load df from session state
        df = st.session_state.get("df")


        def on_input_change():
            user_input = st.session_state.user_input
            st.session_state.past.append(user_input)

            df = st.session_state.df
            df_preview = df.head().to_string()

            code = ask_gpt_for_code(user_input, df_preview)
            cleaned_code = clean_code(code)
            output, fig = run_code_on_df(cleaned_code, df)

            # Append result text
            message_data = f"```python\n{cleaned_code}\n```\n\n**Output:**\n{output}"
            st.session_state.generated.append({
                "type": "normal",
                "data": message_data,
                "fig": fig  # store figure if available
    })


        def on_btn_click():
            st.session_state.past.clear()
            st.session_state.generated.clear()


        # === Streamlit App UI ===
        # Page setup and styles
        st.set_page_config(page_title="RoboLedger", layout="centered")

        # Init session state
        if "past" not in st.session_state:
            st.session_state.past = []
        if "generated" not in st.session_state:
            st.session_state.generated = []

        st.title("👾 RoboLedger ChatBot 👾")
        st.markdown("Ask questions about your transaction data. The AI will generate insights, plots, and summaries.")
        st.caption("Note: Responses are generated by an AI model and may not always be accurate. Please verify critical information independently.")
        st.markdown("---")
        st.session_state.setdefault("plot_type", "Static")

        # Only show chat if df exists
        if isinstance(df, pd.DataFrame) and not df.empty:
            # Full-page chat layout
            for i in range(len(st.session_state.generated)):
                with st.chat_message("user", avatar="🤓"):
                    st.markdown(st.session_state.past[i])

                with st.chat_message("assistant", avatar="👾"):
                    st.markdown("**Generated Code:**")
                    st.code(clean_code(st.session_state.generated[i]["data"]), language="python")

                    st.markdown("**Output:**")
                    st.markdown(st.session_state.generated[i]["data"].split("**Output:**")[-1])

                    if st.session_state.generated[i].get("fig"):
                        st.pyplot(st.session_state.generated[i]["fig"])

            # Input at the bottom
            col1, col2 = st.columns([5, 1])
            with col1:
                st.text_input("Ask about your data...", key="user_input", on_change=on_input_change, label_visibility="collapsed")
            with col2:
                st.button("🧹", on_click=on_btn_click, help="Clear chat")

        else:
            st.info("No data available. Please upload and process a file first.")



        

run()
