import re
import pandas as pd

def janitor(text):
    phone_pattern = re.compile(
        r'(\+?\d{1,2}[\s.-]?)?'          # optional country code
        r'(\(?\d{3}\)?[\s.-]?)?'         # optional area code
        r'\d{3}[\s.-]?\d{4}'             # main phone number
    )
    pattern = r"\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\b"





    new_text = phone_pattern.sub('', text)

    return re.sub(pattern, "", new_text, flags = re.IGNORECASE)


INCOME_KEYWORDS = ["sales", "revenue", "income"]

def is_income(category):
    return any(keyword in category.lower() for keyword in INCOME_KEYWORDS)


def excel_template_generator(df):
    income_df = df[df["Category"].apply(is_income)].sort_values("Category")
    expense_df = df[~df["Category"].apply(is_income)].sort_values("Category")

    output_file = "P&L.xlsx"

    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet("P&L")
        writer.sheets["P&L"] = worksheet

        # Define common font settings
        base_font = {'font_name': 'Georgia', 'indent': 0}

        # Formats
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

        # Title Row (Merged)
        worksheet.merge_range('A1:C1', '<< COMPANY NAME >>', title_fmt)

        # Column Headers
        headers = ["Memo", "Category", "Amount"]
        worksheet.write_row(1, 0, [h.upper() for h in headers], header_fmt)

        row = 2

        ### INCOME ###
        worksheet.write(row, 0, "INCOME", title_fmt)
        row += 1
        income_start_row = row

        for category, group in income_df.groupby("Category"):
            cat_start = row
            for _, entry in group.iterrows():
                worksheet.write(row, 0, entry["Memo"].upper(), normal_fmt)
                worksheet.write(row, 1, entry["Category"].upper(), normal_fmt)
                worksheet.write(row, 2, entry["Amount"], currency_fmt)
                worksheet.set_row(row, None, None, {'level': 1})  # No indent because of indent=0 in format
                row += 1
            # Subtotal
            worksheet.write(row, 0, f"{category.upper()} TOTAL", subtotal_fmt)
            worksheet.write_blank(row, 1, None, subtotal_fmt)
            worksheet.write_formula(row, 2, f"=SUM(C{cat_start + 1}:C{row})", subtotal_currency_fmt)
            row += 1
        income_end_row = row - 1

        ### EXPENSES ###
        worksheet.write(row, 0, "EXPENSES", title_fmt)
        row += 1
        expense_start_row = row

        for category, group in expense_df.groupby("Category"):
            cat_start = row
            for _, entry in group.iterrows():
                worksheet.write(row, 0, entry["Memo"].upper(), normal_fmt)
                worksheet.write(row, 1, entry["Category"].upper(), normal_fmt)
                worksheet.write(row, 2, entry["Amount"], currency_fmt)
                worksheet.set_row(row, None, None, {'level': 1})
                row += 1
            # Subtotal
            worksheet.write(row, 0, f"{category.upper()} TOTAL", subtotal_fmt)
            worksheet.write_blank(row, 1, None, subtotal_fmt)
            worksheet.write_formula(row, 2, f"=SUM(C{cat_start + 1}:C{row})", subtotal_currency_fmt)
            row += 1
        expense_end_row = row - 1

        ### NET PROFIT / LOSS ###
        worksheet.write(row, 1, "NET PROFIT / LOSS", net_fmt)
        worksheet.write_formula(
            row, 2,
            f"=SUM(C{income_start_row + 1}:C{income_end_row + 1})-SUM(C{expense_start_row + 1}:C{expense_end_row + 1})",
            net_currency_fmt
        )

        # Layout tweaks
        worksheet.freeze_panes(2, 0)
        worksheet.set_column("A:A", 30)
        worksheet.set_column("B:B", 18)
        worksheet.set_column("C:C", 14)