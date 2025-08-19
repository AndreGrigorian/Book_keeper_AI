import os
from openai import OpenAI
from dotenv import load_dotenv
import bookkeeper_brain

load_dotenv()  # loads OPENAI_API_KEY from .env

CATEGORIES = [
    "Sales Revenue", "Service Income", "Other Income",
    "Cost of Goods Sold", "Purchases", "Materials and Supplies",
    "Subcontractor Costs", "Freight and Shipping (COGS related)",
    "Advertising", "Bank Fees", "Contract Labor",
    "Depreciation Expense", "Insurance (Business)", "Interest Expense",
    "Legal and Professional Fees", "Office Supplies",
    "Rent or Lease - Vehicles, Machinery, Equipment",
    "Rent or Lease - Other Business Property",
    "Repairs and Maintenance", "Salaries and Wages",
    "Taxes and Licenses", "Travel", "Meals and Entertainment",
    "Utilities", "Internet and Phone", "Education and Training",
    "Business Dues and Subscriptions", "Vehicle Expenses",
    "Home Office Expenses", "Postage and Shipping",
    "Software Expense", "Miscelleanous City Taxes",
    "Owner's Draw", "Estimated Tax Payments", "Income Tax Expense",
    "Payroll Taxes", "Business Loan Interest", "Amortization", "Ask My Accountant"
]

client = OpenAI()


def categorize_batch(memos):

    formatted_memos = "\n".join(
        [f"{i+1}. {memo}" for i, memo in enumerate(memos)])

    prompt = f"""
You are a professional bookkeeping AI. You will categorize memos into the best matching accounting category from the list below.




Categories:
{", ".join(CATEGORIES)}

Below is a list of memos. Respond with one category per line in the same order, numbered, and nothing else.

Memos:
{formatted_memos}

Only output the categories like this:
1. Category
2. Category
...

Begin:
    """

    response = client.chat.completions.create(
        model="gpt-4o",  # use GPT-4o or "gpt-3.5-turbo" if you want to save cost
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw_output = response.choices[0].message.content
    lines = raw_output.strip().splitlines()
    categories = [line.split(". ", 1)[1].strip()
                  for line in lines if ". " in line]
    return categories


# Example usage
# if __name__ == "__main__":
    # -> Internet and Phone
    # print(categorize_batch(["US CELLULAR PMT #5679 568-901-1345 OH","DELTA AIRLINES TXN 9832, 800-922-0204, NJ"]))
    # print(categorize_batch("DELTA AIRLINES TXN 9832, 800-922-0204, NJ"))  # -> Travel
