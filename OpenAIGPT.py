
import openai
import time
from api_import import api_import

class OpenAIGPT:
    def __init__(self):
        # Retrieve OpenAI API credentials

        openai.api_key = api_import()
        self.chunklist = []


        # Initialize variables to track rate limiting
        self.last_call_time = None
        self.min_time_between_calls = 1.0 / 59  # 59 requests per minute
        self.output = str()

        self.prompt_list = []

        self.max_tokens = 1000

    def generate_text_with_prompt(self, prompt, mode):
        """ Generate text with a prompt and split into tokens of max length n. """
        mode = mode

        # Ensure that max_tokens is not greater than max_tokens

        self.prompt_list = self.tokenize(string = prompt)
        self.output = str()
        # Calculate the time elapsed since the last API call
        current_time = time.monotonic()
        progress = 0
        query = 0
        generated_text = str()
        print('prompt list = ', type(self.prompt_list))
        print(len(self.prompt_list))

        for chunck in self.prompt_list:

            query = str(mode + '"' +  chunck + '."')
            print(query)
            # Generate text with the OpenAI API
            done = False
            while done is not True:
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",

                        messages=[
                            {"role": "system", "content": "You are a text processesor. Answer as concisely as possible and in dutch"},
                            {"role": "user", "content": query + '.'},
                            # {"role": "user", "content": chunck + '.'}
                        ],

                        temperature = 0,  # higher more random
                        max_tokens = 200,  # The maximum number of tokens to generate in the completion.
                        top_p = 0.9,  # So 0.1 means only the tokens comprising the top 10% probability mass are considered.
                        frequency_penalty = 0,  # decreasing the model's likelihood to repeat the same line verbatim.
                        presence_penalty = 0  # likelihood to talk about new topics

                    )

                    # Update the last API call time
                    self.last_call_time = time.monotonic()

                    print(response.choices[0])
                    # Get the generated text from the OpenAI API response
                    generated_text = response.choices[0].message.content

                    # Print the progress counter
                    progress += 1
                    print(f"Processed {progress} pieces of text out of {len(self.prompt_list)}")

                    # This section times that calls, so we don't exceed 60 calls per minute

                    time.sleep(self.min_time_between_calls)

                    self.output += '\n' + generated_text
                    done = True
                except:
                    print('An error occured: Tryng again...')
                    time.sleep(self.min_time_between_calls)

        return self.output

    def tokenize(self, string):
        """Split string into list of strings where each string has max length of n tokens."""
        n = self.max_tokens
        if not isinstance(string, str):
            string = str(string)
        tokens = string.split()
        num_tokens = len(tokens)
        print(num_tokens)
        num_chunks = (num_tokens + n - 1) // n
        chunks = [tokens[i * n:(i + 1) * n] for i in range(num_chunks)]
        self.chunklist = [' '.join(chunk) for chunk in chunks]
        return [' '.join(chunk) for chunk in chunks]

    def summarize(self, output):

        summarize_mode = "Vat deze tekst samen: "
        self.categorized = self.generate_text_with_prompt(prompt = str(output), mode = summarize_mode)

    def to_bullets(self, string):
        if not isinstance(string, str):
            string = str(string)
        mode = "Vat de volgende tekst samen in bullets: "
        prompt = string
        output = self.generate_text_with_prompt(self, prompt, mode)
        return output




if __name__ == "__main__":
    # pass
    x = OpenAIGPT()
    with open(r'C:\Users\danie\OneDrive\Documenten\GitHub\Chatgpt-bulk-query\SLA filter\SLA Beschrijving van de maatregel lijst.txt', encoding = 'utf8', errors='replace') as f:
        text = f.read()
    text = text[0:5000-64]

    x.generate_text_with_prompt(text, mode = 'List all relevant methods to improve air quality in bullets, and make an estimate how far this has progressed by rating it from 1 to 5 : \n')
    answer = x.output
    print(answer)
