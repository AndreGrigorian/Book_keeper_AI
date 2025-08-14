import numpy as np
import pandas as pd
from transformers import pipeline
from openpyxl import *
import data_cleaner

## Facebook Bart Large MNLI -- Able to categorize based off given labels by user
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def predict_COA(memo):
    entity_type="sole prop"
    if entity_type == "sole prop":
        labels = [
        # Income
        "Sales Revenue",
        "Service Income",
        "Other Income",

        # Cost of Goods Sold
        "Cost of Goods Sold",
        "Purchases",
        "Materials and Supplies",
        "Subcontractor Costs",
        "Freight and Shipping (COGS related)",

        # Expenses (Operating)
        "Advertising",
        "Bank Fees",
        "Contract Labor",
        "Depreciation Expense",
        "Insurance (Business)",
        "Interest Expense",
        "Legal and Professional Fees",
        "Office Supplies",
        "Rent or Lease - Vehicles, Machinery, Equipment",
        "Rent or Lease - Other Business Property",
        "Repairs and Maintenance",
        "Salaries and Wages",
        "Taxes and Licenses",
        "Travel",
        "Meals and Entertainment",
        "Utilities",
        "Internet and Phone",
        "Education and Training",
        "Business Dues and Subscriptions",
        "Vehicle Expenses",
        "Home Office Expenses",
        "Postage and Shipping",
        "Software and Online Services",

        # Other
        "Owner's Draw",
        "Estimated Tax Payments",
        "Income Tax Expense",
        "Payroll Taxes",
        "Business Loan Interest",
        "Amortization",
        ]
        result = classifier(memo, labels,  hypothesis_template="This transaction is related to {}.")
        # result['labels'][0] is the highest scored label
        return result['labels'][0]

    elif entity_type == "Partnership":
        labels = [
        # Income
        "Sales Revenue",
        "Service Income",
        "Rental Income",
        "Interest Income",
        "Dividend Income",
        "Other Income",

        # Cost of Goods Sold
        "Cost of Goods Sold",
        "Purchases",
        "Materials and Supplies",
        "Direct Labor",
        "Subcontractor Costs",
        "Freight and Shipping (COGS related)",

        # Operating Expenses
        "Advertising",
        "Bank Fees",
        "Contract Labor",
        "Depreciation Expense",
        "Insurance (Business)",
        "Interest Expense",
        "Legal and Professional Fees",
        "Office Supplies",
        "Rent or Lease - Vehicles, Machinery, Equipment",
        "Rent or Lease - Real Estate",
        "Repairs and Maintenance",
        "Salaries and Wages",
        "Taxes and Licenses",
        "Travel",
        "Meals and Entertainment",
        "Utilities",
        "Internet and Phone",
        "Education and Training",
        "Dues and Subscriptions",
        "Vehicle Expenses",
        "Postage and Shipping",
        "Software and Online Services",
        "Commissions and Fees",

        # Partner-Related Accounts
        "Partner Contributions",
        "Partner Distributions",
        "Guaranteed Payments to Partners",
        "Partner Loans",
        "Partner Capital Accounts",

        # Other
        "Payroll Taxes",
        "Estimated Tax Payments",
        "Income Tax Expense (if applicable)",
        "Amortization",
        "Bad Debt Expense",
        "Charitable Contributions",
        "Organization Costs",
        ]
        result = classifier(memo, labels, hypothesis_template="This transaction is related to {}.")
        # result['labels'][0] is the highest scored label
        return result['labels'][0]
        
    elif entity_type == "S-Corp":
        labels = [
        # Income
        "Sales Revenue",
        "Service Income",
        "Rental Income",
        "Interest Income",
        "Dividend Income",
        "Other Income",

        # Cost of Goods Sold
        "Cost of Goods Sold",
        "Purchases",
        "Materials and Supplies",
        "Direct Labor",
        "Subcontractor Costs",
        "Freight and Shipping (COGS related)",

        # Operating Expenses
        "Advertising",
        "Bank Fees",
        "Contract Labor",
        "Depreciation Expense",
        "Employee Salaries and Wages",
        "Officer Compensation",
        "Employee Benefits",
        "Health Insurance Premiums",
        "Insurance (General Business)",
        "Interest Expense",
        "Legal and Professional Fees",
        "Office Supplies",
        "Rent or Lease - Vehicles, Equipment",
        "Rent or Lease - Real Estate",
        "Repairs and Maintenance",
        "Taxes and Licenses",
        "Payroll Taxes",
        "Utilities",
        "Travel",
        "Meals and Entertainment (50%)",
        "Telephone and Internet",
        "Training and Education",
        "Dues and Subscriptions",
        "Software and Online Services",
        "Postage and Shipping",
        "Charitable Contributions (Deductible)",
        "Bad Debt Expense",
        "Amortization",
        "Other Deductions",

        # Shareholder/Equity Accounts
        "Shareholder Distributions",
        "Retained Earnings",
        "Shareholder Loans Payable",
        "Shareholder Loans Receivable",
        "Capital Stock",
        "Additional Paid-in Capital",

        # Tax-Specific Accounts
        "Estimated Tax Payments",
        "State Income Tax Expense",
        "Deferred Tax Assets",
        "Deferred Tax Liabilities",

        # Other Income/Expense
        "Gain/Loss on Asset Disposal",
        "Unrealized Gain/Loss",
        "Interest Expense - Non-deductible",
        ]
        result = classifier(memo, labels, hypothesis_template="This transaction is related to {}.")
        # result['labels'][0] is the highest scored label
        return result['labels'][0]
    elif entity_type == 'C-Corp':
        labels = [
        # Income
        "Sales Revenue",
        "Service Income",
        "Rental Income",
        "Interest Income",
        "Dividend Income",
        "Other Income",

        # Cost of Goods Sold
        "Cost of Goods Sold",
        "Purchases",
        "Materials and Supplies",
        "Direct Labor",
        "Subcontractor Costs",
        "Freight and Shipping (COGS related)",

        # Operating Expenses
        "Advertising",
        "Bank Fees",
        "Contract Labor",
        "Depreciation Expense",
        "Employee Salaries and Wages",
        "Employee Benefits",
        "Health Insurance Premiums",
        "Insurance (General Business)",
        "Interest Expense",
        "Legal and Professional Fees",
        "Office Supplies",
        "Rent or Lease - Vehicles, Equipment",
        "Rent or Lease - Real Estate",
        "Repairs and Maintenance",
        "Taxes and Licenses",
        "Payroll Taxes",
        "Utilities",
        "Travel",
        "Meals and Entertainment (50%)",
        "Telephone and Internet",
        "Training and Education",
        "Dues and Subscriptions",
        "Software and Online Services",
        "Postage and Shipping",
        "Charitable Contributions (Deductible)",
        "Bad Debt Expense",
        "Amortization",
        "Other Deductions",

        # Equity Accounts
        "Common Stock",
        "Preferred Stock",
        "Additional Paid-in Capital",
        "Retained Earnings",
        "Treasury Stock",

        # Tax-Specific Accounts
        "Estimated Tax Payments",
        "Federal Income Tax Expense",
        "State Income Tax Expense",
        "Deferred Tax Assets",
        "Deferred Tax Liabilities",

        # Other Income/Expense
        "Gain/Loss on Asset Disposal",
        "Unrealized Gain/Loss",
        "Interest Expense - Non-deductible",
        ]
        result = classifier(memo, labels, hypothesis_template="This transaction is related to {}.")
        # result['labels'][0] is the highest scored label
        return result['labels'][0]



    ## Let's assume the last type of entity is a NON-PROFIT
    else:
        labels = [
        # Revenue
        "Contributions and Donations",
        "Grants (Government)",
        "Grants (Private)",
        "Membership Dues",
        "Fundraising Event Income",
        "Program Service Revenue",
        "Investment Income",
        "Rental Income",
        "In-Kind Contributions",
        "Other Income",

        # Program Expenses
        "Program Salaries and Wages",
        "Program Supplies",
        "Educational Materials",
        "Scholarships and Grants",
        "Community Outreach",
        "Travel (Program Services)",
        "Contract Services (Program Related)",

        # Management and General Expenses
        "Admin Salaries and Wages",
        "Accounting and Legal Fees",
        "Office Supplies",
        "Rent and Utilities",
        "Insurance (General)",
        "Depreciation and Amortization",
        "Telephone and Internet",
        "Bank and Merchant Fees",
        "Board Meetings and Governance",
        "Postage and Shipping",

        # Fundraising Expenses
        "Fundraising Salaries",
        "Fundraising Event Costs",
        "Donor Communications",
        "Marketing and Advertising (Fundraising)",
        "Printing and Mailing (Fundraising)",

        # Tax and Compliance
        "Payroll Taxes",
        "State Filing Fees",
        "Professional Licenses and Permits",
        "Charitable Registration Fees",

        # Other Expenses
        "Bad Debt Expense",
        "Loss on Asset Disposal",
        "Miscellaneous Expense",

        # Equity / Net Assets (non-profit terminology)
        "Net Assets - Without Donor Restrictions",
        "Net Assets - With Donor Restrictions",
        "Opening Balance Equity",
        "Retained Earnings (Net Assets)",

        # Grant and Donor Tracking (if needed)
        "Temporarily Restricted Contributions",
        "Permanently Restricted Contributions",
        "Released from Restrictions",

        # Liabilities (typical)
        "Accounts Payable",
        "Deferred Revenue",
        "Accrued Expenses",
        "Loans Payable",

        # Assets (typical)
        "Cash and Cash Equivalents",
        "Accounts Receivable",
        "Grants Receivable",
        "Prepaid Expenses",
        "Property and Equipment",
        "Investments",
        ]
        result = classifier(memo, labels, hypothesis_template="This transaction is related to {}.")
        # result['labels'][0] is the highest scored label
        return result['labels'][0]

# Load your Excel sheet into a DataFrame
df = pd.read_excel("dummy_data.xlsx")
df["Memo"] = df["Memo"].apply(janitor)
df['Predicted Account'] = df['Memo'].apply(predict_COA)


df.to_excel("updated_csv.xlsx", index=False)

