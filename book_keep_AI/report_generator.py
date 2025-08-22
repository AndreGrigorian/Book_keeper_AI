import re
import pandas as pd
from io import BytesIO
import streamlit as st



def is_income(category):
    INCOME_KEYWORDS = ["sales", "revenue", "income"]
    return any(keyword in category.lower() for keyword in INCOME_KEYWORDS)

def excel_template_generator(df):
    if "Predicted Account" in df.columns and "Category" not in df.columns:
        df = df.rename(columns={"Predicted Account": "Category"})

    required_cols = {"Memo", "Category", "Amount"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"Required columns missing: {missing_cols}")

    df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce').fillna(0)

    income_df = df[df["Category"].apply(is_income)].sort_values("Category")
    expense_df = df[~df["Category"].apply(is_income)].sort_values("Category")

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet("P&L")
    writer.sheets["P&L"] = worksheet

    base_font = {'font_name': 'Georgia', 'indent': 0}
    title_fmt = workbook.add_format({
        **base_font, 'bold': True, 'font_size': 16, 'align': 'center', 'valign': 'vcenter'
    })
    header_fmt = workbook.add_format({
        **base_font, 'bold': True, 'border': 1, 'align': 'center',
        'valign': 'vcenter', 'bg_color': '#F2F2F2'
    })
    normal_fmt = workbook.add_format({**base_font, 'border': 1, 'valign': 'top'})
    currency_fmt = workbook.add_format({**base_font, 'num_format': '#,##0.00', 'border': 1})
    subtotal_fmt = workbook.add_format({
        **base_font, 'bold': True, 'border': 1, 'italic': True
    })
    subtotal_currency_fmt = workbook.add_format({
        **base_font, 'num_format': '#,##0.00', 'border': 1, 'bold': True, 'italic': True
    })
    net_fmt = workbook.add_format({
        **base_font, 'bold': True, 'top': 2, 'align': 'right'
    })
    net_currency_fmt = workbook.add_format({
        **base_font, 'num_format': '#,##0.00', 'bold': True, 'top': 2
    })

    worksheet.merge_range('A1:C1', '<< COMPANY NAME >>', title_fmt)
    headers = ["Memo", "Category", "Amount"]
    worksheet.write_row(1, 0, [h.upper() for h in headers], header_fmt)

    row = 2
    worksheet.write(row, 0, "INCOME", title_fmt)
    row += 1
    income_start_row = row

    for category, group in income_df.groupby("Category"):
        cat_start = row
        for _, entry in group.iterrows():
            worksheet.write(row, 0, str(entry["Memo"]).upper(), normal_fmt)
            worksheet.write(row, 1, str(entry["Category"]).upper(), normal_fmt)
            worksheet.write(row, 2, entry["Amount"], currency_fmt)
            worksheet.set_row(row, None, None, {'level': 1})
            row += 1
        worksheet.write(row, 0, f"{category.upper()} TOTAL", subtotal_fmt)
        worksheet.write_blank(row, 1, None, subtotal_fmt)
        worksheet.write_formula(row, 2, f"=SUM(C{cat_start + 1}:C{row})", subtotal_currency_fmt)
        row += 1
    income_end_row = row - 1

    worksheet.write(row, 0, "EXPENSES", title_fmt)
    row += 1
    expense_start_row = row

    for category, group in expense_df.groupby("Category"):
        cat_start = row
        for _, entry in group.iterrows():
            worksheet.write(row, 0, str(entry["Memo"]).upper(), normal_fmt)
            worksheet.write(row, 1, str(entry["Category"]).upper(), normal_fmt)
            worksheet.write(row, 2, entry["Amount"], currency_fmt)
            worksheet.set_row(row, None, None, {'level': 1})
            row += 1
        worksheet.write(row, 0, f"{category.upper()} TOTAL", subtotal_fmt)
        worksheet.write_blank(row, 1, None, subtotal_fmt)
        worksheet.write_formula(row, 2, f"=SUM(C{cat_start + 1}:C{row})", subtotal_currency_fmt)
        row += 1
    expense_end_row = row - 1

    worksheet.write(row, 1, "NET PROFIT / LOSS", net_fmt)
    worksheet.write_formula(
        row, 2,
        f"=SUM(C{income_start_row + 1}:C{income_end_row + 1})-SUM(C{expense_start_row + 1}:C{expense_end_row + 1})",
        net_currency_fmt
    )

    worksheet.freeze_panes(2, 0)
    worksheet.set_column("A:A", 30)
    worksheet.set_column("B:B", 18)
    worksheet.set_column("C:C", 14)

    # Optional: Write full raw data to a second sheet
    df.to_excel(writer, index=False, sheet_name='Report')
    writer.close()
    processed_data = output.getvalue()
    return processed_data # Return raw bytes


