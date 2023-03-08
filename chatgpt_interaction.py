
import openai
import time

class OpenAIGPT:
    def __init__(self):
        # Retrieve OpenAI API credentials
        apikey_location = r"C:\Users\d.los\OneDrive - Berenschot\Bureaublad\chatgpt openai key.txt"
        with open(apikey_location) as f:
            self.key = f.readline()
        openai.api_key = self.key

        # Initialize variables to track rate limiting
        self.last_call_time = None
        self.min_time_between_calls = 1.0 / 59  # 59 requests per minute

    def generate_text_with_prompt(self, prompt, max_tokens, mode, n):
        """ Generate text with a prompt and split into tokens of max length n. """
        # Ensure that max_tokens is not greater than 2000
        if len(prompt) < max_tokens:

        #Calculate the time elapsed since the last API call
        current_time = time.monotonic()
        time_since_last_call = current_time - self.last_call_time if self.last_call_time is not None else self.min_time_between_calls

        # Wait for the appropriate amount of time to ensure that we don't exceed the rate limit
        if time_since_last_call < self.min_time_between_calls:
            time.sleep(self.min_time_between_calls - time_since_last_call)

        # Generate text with the OpenAI API
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Update the last API call time
        self.last_call_time = time.monotonic()

        # Get the generated text from the OpenAI API response
        generated_text = response.choices[0].text

        # Split the generated text into tokens of max length n
        tokens = self.tokenize(generated_text, n)

        # Print the progress counter
        progress = f"{len(tokens)}/{response.total_generated_tokens // n}"
        print(f"Processed {progress} pieces of text.")

        return tokens

    def tokenize(self, text, n):
        """Split text into tokens of max length n."""
        tokens = []
        words = text.split()
        current_token = words[0]
        for word in words[1:]:
            if len(current_token) + len(word) + 1 <= n:
                current_token += " " + word
            else:
                tokens.append(current_token)
                current_token = word

        tokens.append(current_token)
        return tokens


        # Initialize variables to track rate limiting
        self.last_call_time = None
        self.min_time_between_calls = 1.0 / 59  # 59 requests per minute

if __name__ == "__main__":
    pass
    # x = OpenAIGPT()

    # x.generate_text_with_prompt(f'summarize: {text}')
