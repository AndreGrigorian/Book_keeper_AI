import pandas as pd
from ofxparse import OfxParser

def parse_qbo_file(file_obj) -> pd.DataFrame:
    try:
        ofx = OfxParser.parse(file_obj)
        transactions = ofx.account.statement.transactions

        data = [{
            "date": txn.date,
            "amount": txn.amount,
            "type": txn.type,
            "payee": txn.payee,
            "memo": txn.memo,
            "id": txn.id
        } for txn in transactions]

        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"❌ Failed to parse QBO file: {e}")
        return pd.DataFrame()  # ✅ Always return a DataFrame
