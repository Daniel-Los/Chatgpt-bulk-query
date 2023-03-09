
import openai
import time

class OpenAIGPT:
    def __init__(self):
        # Retrieve OpenAI API credentials
        apikey_location = r"C:\Users\d.los\OneDrive - Berenschot\Bureaublad\chatgpt openai key.txt"
        with open(apikey_location) as f:
            self.key = f.readline()
        openai.api_key = self.key
        self.chunklist = []


        # Initialize variables to track rate limiting
        self.last_call_time = None
        self.min_time_between_calls = 1.0 / 59  # 59 requests per minute
        self.output = str()

        self.tokens = 2000

    def generate_text_with_prompt(self, prompt, mode):
        """ Generate text with a prompt and split into tokens of max length n. """

        # Ensure that max_tokens is not greater than 2000

        prompt_list = self.AI.tokenize(self = self.AI, string = prompt)

        # Calculate the time elapsed since the last API call
        current_time = time.monotonic()
        progress = 0
        query = 0
        generated_text = str()
        for chunck in prompt_list:
            if not query:
                query = mode + chunck
            else:
                query = mode + "en vul aan" + generated_text

            print(query)
            # Generate text with the OpenAI API
            response = openai.Completion.create(
                engine="davinci",
                prompt=query,
                max_tokens=self.AI.tokens,
                n=1,
                stop=None,
                temperature=0.2,
            )

            # Update the last API call time
            self.last_call_time = time.monotonic()

            # Get the generated text from the OpenAI API response
            generated_text += response.choices[0].text

            # Split the generated text into tokens of max length n
            tokens = self.AI.tokenize(generated_text)

            # Print the progress counter
            progress += 1
            print(f"Processed {progress} pieces of text out of {len(prompt_list)}")

            # This section times that calls, so we don't exceed 60 calls per minute

            time.sleep(self.AI.min_time_between_calls)

        self.AI.output += generated_text
        return generated_text

    def tokenize(self, string):
        """Split string into list of strings where each string has max length of n tokens."""
        n = 30
        string = string[0]
        tokens = string.split()
        num_tokens = len(tokens)
        num_chunks = (num_tokens + n - 1) // n
        chunks = [tokens[i * n:(i + 1) * n] for i in range(num_chunks)]
        self.chunklist = [' '.join(chunk) for chunk in chunks]
        return [' '.join(chunk) for chunk in chunks]

if __name__ == "__main__":
    # pass
    # x = OpenAIGPT()
    text = 'blub'
    x.generate_text_with_prompt(text, mode = 'repeat this word 1 time after: ')
    print()
