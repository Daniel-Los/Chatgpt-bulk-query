
import openai
import time

class OpenAIGPT:
    def __init__(self):
        # Retrieve OpenAI API credentials
        apikey_location = r"C:\Users\d.los\OneDrive - Berenschot\Bureaublad\chatgpt openai key.txt"
        # apikey_location = r"C:\Users\danie\OneDrive\Bureaublad\Coding\api keys\openai key.txt"
        with open(apikey_location) as f:
            self.key = f.readline()
        openai.api_key = self.key
        self.chunklist = []


        # Initialize variables to track rate limiting
        self.last_call_time = None
        self.min_time_between_calls = 1.0 / 59  # 59 requests per minute
        self.output = str()

        self.prompt_list = []

        self.max_tokens = 1500

    def generate_text_with_prompt(self, prompt, mode):
        """ Generate text with a prompt and split into tokens of max length n. """

        # Ensure that max_tokens is not greater than 2000

        self.prompt_list = self.tokenize(string = prompt)

        # Calculate the time elapsed since the last API call
        current_time = time.monotonic()
        progress = 0
        query = 0
        generated_text = str()
        print('prompt list = ', type(self.prompt_list))
        for chunck in self.prompt_list:
            print('chunck = ', type(chunck))
            if not query:
                query = str(mode +'"' +  chunck + '."')
            # else:
            #     query = str(mode + "en vul deze tekst aan :" + generated_text + '. ' + chunck + '.')
            else:
                query = str(mode +'"' +  chunck + '."')

            print(query)
            # Generate text with the OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Answer in dutch"},
                    {"role": "user", "content": query + '.'},
                    # {"role": "user", "content": chunck + '.'}
                ]
            )

            # Update the last API call time
            self.last_call_time = time.monotonic()

            print(response.choices[0])
            # Get the generated text from the OpenAI API response
            generated_text += response.choices[0].message.content

            # Print the progress counter
            progress += 1
            print(f"Processed {progress} pieces of text out of {len(self.prompt_list)}")

            # This section times that calls, so we don't exceed 60 calls per minute

            time.sleep(self.min_time_between_calls)

            self.output += '\n' + generated_text
        return self.output

    def tokenize(self, string):
        """Split string into list of strings where each string has max length of n tokens."""
        n = self.max_tokens
        if isinstance(string, list):
            string = string[0]
        tokens = string.split()
        num_tokens = len(tokens)
        num_chunks = (num_tokens + n - 1) // n
        chunks = [tokens[i * n:(i + 1) * n] for i in range(num_chunks)]
        self.chunklist = [' '.join(chunk) for chunk in chunks]
        return [' '.join(chunk) for chunk in chunks]

if __name__ == "__main__":
    # pass
    x = OpenAIGPT()
    with open(r'C:\Users\danie\OneDrive\Documenten\GitHub\Chatgpt-bulk-query\SLA filter\SLA Beschrijving van de maatregel lijst.txt', encoding = 'utf8', errors='replace') as f:
        text = f.read()
    text = text[0:5000-64]

    x.generate_text_with_prompt(text, mode = 'List all relevant methods to improve air quality in bullets, and make an estimate how far this has progressed by rating it from 1 to 5 : \n')
    answer = x.output
    print(answer)
