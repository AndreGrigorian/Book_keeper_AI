import os
from openai import OpenAI
from dotenv import load_dotenv
import bookkeeper_brain

load_dotenv()  # loads OPENAI_API_KEY from .env


client = OpenAI()


def categorize_batch(memos, CATEGORIES):

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


