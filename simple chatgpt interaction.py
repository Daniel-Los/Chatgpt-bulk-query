import openai

# Use your own API key from the openai website
# CAUTION: max 18 dollars per (telephone nr) account on the free trial
key = 'YOUR KEY HERE'
apikey_location = r"C:\Users\danie\OneDrive\Bureaublad\Coding\api keys\openai key.txt"
with open(apikey_location) as f:
    key = f.readline()
openai.api_key = key

# The document you want to summarize
with open(r'C:\Users\danie\OneDrive\Documenten\GitHub\Chatgpt-bulk-query\SLA filter\SLA Beschrijving van de maatregel lijst.txt',
          encoding='utf8') as f:
    text = f.read()

# The prompt for the summary
# prompt = f"Summarize this text: {text}"
prompt = 'finish this sentence: hello darkness my old friend'

# Generate a summary
# completions = openai.ChatCompletion.create(model="gpt-3.5-turbo",
#                                            messages=[{"role": "assistant", "content": prompt}])

completions = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
)

# Print the result
print(completions.choices)
