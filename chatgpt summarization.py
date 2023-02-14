import openai

# Use your own API key from the openai website
# CAUTION: max 18 dollars per (telephone nr) account on the free trial
key = 'YOUR KEY HERE'

openai.api_key = key

# The document you want to summarize
text = "The document you want to summarize"

# The prompt for the summary
prompt = (f"summarize: {text}")

# Generate a summary
completions = openai.Completion.create(engine="text-davinci-002", prompt=prompt)

# Print the summary
print(completions.choices[0].text)