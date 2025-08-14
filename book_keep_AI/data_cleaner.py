import re


def janitor(text):
    phone_pattern = re.compile(
        r'(\+?\d{1,2}[\s.-]?)?'          # optional country code
        r'(\(?\d{3}\)?[\s.-]?)?'         # optional area code
        r'\d{3}[\s.-]?\d{4}'             # main phone number
    )
    pattern = r"\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\b"
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'




    new_text = phone_pattern.sub('', text)
    new_text = re.sub(email_pattern, "", new_text, flags = re.IGNORECASE)

    return re.sub(pattern, "", new_text, flags = re.IGNORECASE)
