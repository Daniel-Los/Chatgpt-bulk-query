
import openai
import time

class OpenAIGPT:
    def __init__(self):
        # Retrieve OpenAI API credentials
        apikey_location = r"C:\Users\d.los\OneDrive - Berenschot\Bureaublad\chatgpt openai key.txt"
        with open(apikey_location) as f:
            self.key = f.readline()
        openai.api_key = self.key

        self.max_tokens = 2000
        # Initialize variables to track rate limiting
        self.last_call_time = None
        self.min_time_between_calls = 1.0 / 59  # 59 requests per minute
        self.output = str()

    def generate_text_with_prompt(self, prompt, mode):
        """ Generate text with a prompt and split into tokens of max length n. """

        # Ensure that max_tokens is not greater than 2000
        if len(prompt) > self.max_tokens:
            prompt_list = self.tokenize(prompt)
        else:
            prompt_list = [prompt]

        # Calculate the time elapsed since the last API call
        current_time = time.monotonic()
        progress = 0
        query = 0
        generated_text = str()
        for chunck in prompt_list:
            if not query:
                query = mode + chunck
            else:
                mode + "en vul aan" + generated_text

            # Generate text with the OpenAI API
            response = openai.Completion.create(
                engine="davinci",
                prompt=query,
                max_tokens=self.max_tokens,
                n=1,
                stop=None,
                temperature=0.2,
            )

            # Update the last API call time
            self.last_call_time = time.monotonic()

            # Get the generated text from the OpenAI API response
            generated_text += response.choices[0].text

            # Split the generated text into tokens of max length n
            tokens = self.tokenize(generated_text)

            # Print the progress counter
            progress += 1
            print(f"Processed {progress} pieces of text out of {len(prompt_list)}")

            # This section times that calls, so we don't exceed 60 calls per minute

            time.sleep(self.min_time_between_calls)

        self.output += generated_text
        return generated_text

    def tokenize(self, string):
        """Split string into list of strings where each string has max length of n tokens."""
        n = self.max_tokens
        tokens = string.split()
        num_tokens = len(tokens)
        num_chunks = (num_tokens + n - 1) // n
        chunks = [tokens[i * n:(i + 1) * n] for i in range(num_chunks)]
        return [' '.join(chunk) for chunk in chunks]

if __name__ == "__main__":
    # pass
    # x = OpenAIGPT()
    text = 'blub'
    x.generate_text_with_prompt(text, mode = 'repeat this word 1 time after: ')
    print()
