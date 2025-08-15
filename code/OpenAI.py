import os
import openai

openai.api_key = "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"
question = input("Ask me anything:  ")


response = openai.Completion.create(
  model="text-davinci-002",
  prompt=question,
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response.choices[0].text.strip())


