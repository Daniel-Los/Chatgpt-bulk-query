
import openai
import time
from api_import import api_import
import tiktoken

class OpenAIGPT:
    def __init__(self, prompt):
        # Retrieve OpenAI API credentials

        openai.api_key = api_import()
        self.chunklist = []

        # Initialize variables to track rate limiting
        self.last_call_time = None
        rpm = 11
        self.min_time_between_calls = 1.0 / 59 * 60  # seconds (Max 59 requests per minute)
        self.output = str()

        self.prompt_list = []
        self.query = ''

        self.tokens_sent_in_current_minute = 0
        self.current_minute = time.time() // 60
        self.max_tokens_per_minute = 180000

        self.length_prompt = self.count_tokens(prompt)
        self.desired_output_length = 4000
        self.max_query_length = 15385 - self.length_prompt - self.desired_output_length # 16385 max for model, 4000 for output
        if self.max_query_length < 16000/2:
            raise "Careful, query lenght is shorter than a 1000, which may lead to a lot of iterations. \nConsider" \
                  "lowering the lenght of the prompt."


    def generate_text_with_prompt(self, prompt, mode, extra = ''):
        """ Generate text with a prompt and split into tokens of max length n. """
        mode = mode

        # Ensure that max_tokens is not greater than 2000

        self.prompt_list = self.tokenize(string = prompt)
        self.output = str()
        # Calculate the time elapsed since the last API call
        current_time = time.monotonic()
        progress = 0
        query = 0
        generated_text = str()

        for chunck in self.prompt_list:

            query = str(mode + '"Document: ' + extra + '"' + ' "Chuncknummer ' + chunck + '"')
            self.query = query
            self.count_tokens(query)

            # print(query.replace("\n", " "))
            # Generate text with the OpenAI API
            done = False
            while done is not True:
                start_time = time.time()

                tokens_to_send = self.count_tokens(query)
                self.wait_for_token_availability(tokens_to_send)
                print(f'\nSending {tokens_to_send} tokens.')
                try:
                    response = openai.ChatCompletion.create(
                        # model="gpt-3.5-turbo",
                        model = "gpt-3.5-turbo-16k-0613",

                        messages=[
                            {"role": "system", "content": ""},
                            {"role": "user", "content": query + '. '},
                            # {"role": "user", "content": chunck + '.'}
                        ],

                        temperature = 0,  # higher more random
                        max_tokens = 4000,  # The maximum number of tokens to generate in the completion.
                        # So 0.1 means only the tokens comprising the top 10% probability mass are considered.
                        frequency_penalty = 0.5,  # decreasing the model's likelihood to repeat the same line verbatim.
                        presence_penalty = 0.5,  # likelihood to talk about new topics

                    )
                    # Update the last API call time
                    self.last_call_time = time.monotonic()

                    # print(response.choices[0])
                    # Get the generated text from the OpenAI API response
                    generated_text = response.choices[0].message.content

                    # Print the progress counter
                    progress += 1

                    # self.progress_bar(progress, len(self.prompt_list))
                    print(f"\rProcessed {progress} pieces of text out of {len(self.prompt_list)}", sep='', end='')

                    # This section times that calls, so we don't exceed 60 calls per minute
                    end_time = time.time()
                    time_taken = end_time - start_time
                    if time_taken < self.min_time_between_calls:
                        time.sleep(self.min_time_between_calls - time_taken)

                    self.output += '\n' + generated_text
                    done = True
                except Exception as e:
                    print('An error occured: ')
                    print(e)
                    print('Trying again...')
                    time.sleep(self.min_time_between_calls)
                    
        return self.output

    def tokenize(self, string):
        """Split string into list of strings where each string has max length of n tokens (using tiktoken library)"""
        """The string is split """
        n = self.max_query_length - self.length_prompt - 10

        if isinstance(string, list):
            # This if gate enables processing of single documents
            string = string[0]

        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-16k-0613")
        tokens = encoding.encode(string)
        tokens = [encoding.decode([token]) for token in tokens]
        num_tokens = len(tokens)
        num_chunks = (num_tokens + n - 1) // n
        chunks = [tokens[i * n:(i + 1) * n] for i in range(num_chunks)] # Joins all tokens to create

        return [''.join(chunk) for chunk in chunks]

    def count_tokens(self,string):
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-16k-0613")
        tokens = encoding.encode(string)
        tokens = [encoding.decode([token]) for token in tokens]
        num_tokens = len(tokens)
        return num_tokens
    def reset_token_counter(self):
        self.tokens_sent_in_current_minute = 0

    def can_send_tokens(self, new_tokens_count):
        new_minute = time.time() // 60

        if new_minute > self.current_minute:
            self.current_minute = new_minute
            self.reset_token_counter()

        if self.tokens_sent_in_current_minute + new_tokens_count <= self.max_tokens_per_minute:
            self.tokens_sent_in_current_minute += new_tokens_count
            return True
        return False

    def wait_for_token_availability(self, new_tokens_count, check_interval=2):
        while not self.can_send_tokens(new_tokens_count):
            time.sleep(check_interval)
        # Now tokens are available, you can send the request


# Example usage


if __name__ == "__main__":
    # pass
    x = OpenAIGPT()
    with open(r'C:\Users\danie\OneDrive\Documenten\GitHub\Chatgpt-bulk-query\SLA filter\SLA Beschrijving van de maatregel lijst.txt', encoding = 'utf8', errors='replace') as f:
        text = f.read()
    text = text[0:5000-64]

    x.generate_text_with_prompt(text, mode = 'List all relevant methods to improve air quality in bullets, and make an estimate how far this has progressed by rating it from 1 to 5 : \n')
    answer = x.output
    print(answer)

    text_to_send = "Your text string here..."


