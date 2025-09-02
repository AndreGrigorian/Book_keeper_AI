import pandas as pd
from ofxparse import OfxParser

def parse_qbo_to_df(qbo_file_path: str) -> pd.DataFrame:
    """
    Parses a QBO (QuickBooks) file and returns a DataFrame of transactions.

    Parameters:
        qbo_file_path (str): Path to the .qbo file.

    Returns:
        pd.DataFrame: DataFrame with columns [date, amount, type, payee, memo, id]
    """
    try:
        with open(qbo_file_path, 'r') as f:
            ofx = OfxParser.parse(f)

        transactions = ofx.account.statement.transactions

        data = [{
            "date": txn.date,
            "amount": txn.amount,
            "type": txn.type,
            "payee": txn.payee,
            "memo": txn.memo,
            "id": txn.id
        } for txn in transactions]

        df = pd.DataFrame(data)

        return df
    
    except Exception as e:
        print(f"❌ Failed to parse QBO file: {e}")