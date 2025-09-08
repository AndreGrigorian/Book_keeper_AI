import pandas as pd
from ofxparse import OfxParser
import streamlit as st

def parse_qbo_file(file_obj) -> pd.DataFrame:
    try:
        ofx = OfxParser.parse(file_obj)
        transactions = ofx.account.statement.transactions

        data = [{
            "Date": txn.date,
            "Amount": txn.amount,
            "Type": txn.type,
            "Memo": txn.payee
        } for txn in transactions]

        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"❌ Failed to parse QBO file: {e}")
        return pd.DataFrame()  # ✅ Always return a DataFrame
