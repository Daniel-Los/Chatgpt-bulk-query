import openai
import json

# Use your own API key from the openai website
# CAUTION: max 18 dollars per (telephone nr) account on the free trial
key = 'YOUR KEY HERE'

apikey_location = r"C:\Users\d.los\OneDrive - Berenschot\Bureaublad\chatgpt openai key.txt"
with open(apikey_location) as f:
    key = f.readline()
openai.api_key = key

with open('half short story.txt', encoding='utf8') as f:
    text = f.read()

# The prompt for the summary
prompt = (f"summarize: {text}")

# Generate a summary
completions = openai.Completion.create(engine="text-davinci-002", prompt=prompt)

# print(completions['choices'][0]['message']['content'])

# Print the summary
print(completions.choices[0].text)