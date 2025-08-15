import os
from openai import OpenAI
from dotenv import load_dotenv

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
    "Software and Online Services",
    "Owner's Draw", "Estimated Tax Payments", "Income Tax Expense",
    "Payroll Taxes", "Business Loan Interest", "Amortization"
]

client = OpenAI()


def categorize(memo):
    """
    Takes a transaction memo string and returns the matching bookkeeping category.
    """
    custom_prompt = f"""
You are a bookkeeping transaction categorizer.
Choose the single best category from the list below for the given memo.
If its not in the list, put "Ask my accountant"

Categories:
{", ".join(CATEGORIES)}

Memo: "{memo}"
Only respond with the category name, nothing else.
    """
    # resp = client.responses.create(
    #     model="gpt-4.1-mini",
    #     temperature=0,
    #     messages=[
    #         {"role": "system", "content": "You are a helpful bookkeeping categorization assistant."},
    #         {"role": "user", "content": custom_prompt}
    #     ]
    # )

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=custom_prompt
    )
    return response.output_text.strip()

# Example usage
# if __name__ == "__main__":
#     print(categorize("US CELLULAR PMT #5679 568-901-1345 OH"))  # -> Internet and Phone
#     print(categorize("DELTA AIRLINES TXN 9832, 800-922-0204, NJ"))  # -> Travel
