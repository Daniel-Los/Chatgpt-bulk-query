
import openai
import time
from api_import import api_import
import tiktoken
import tiktoken_ext

class OpenAIGPT:
    def __init__(self, prompt, api_key_path):
        # Retrieve OpenAI API credentials

        openai.api_key = api_import(api_key_path)
        self.chunklist = []

        # Initialize variables to track rate limiting
        self.last_call_time = None
        rpm = 11
        self.min_time_between_calls = 1.0 / 59 * 60  # seconds (Max 59 requests per minute)
        self.output = str()

        self.prompt_list = []
        self.prompt = prompt
        self.query = ''

        self.tokens_sent_in_current_minute = 0
        self.current_minute = time.time() // 60
        self.max_tokens_per_minute = 180000

        self.model_max = 6000 - 110 # 16385 for 16k, 4097 for 4k, 110 for margin
        self.length_prompt = self.count_tokens(prompt)
        print(f'prompt length = {self.length_prompt}')
        self.desired_output_length = 2000
        self.max_query_length =  self.model_max - self.length_prompt - self.desired_output_length
        if self.max_query_length < self.model_max/2:
            raise "Careful, query lenght is shorter than a 1000, which may lead to a lot of iterations. \nConsider" \
                  "lowering the lenght of the prompt."


    def generate_text_with_prompt(self, text, mode, extra = ''):
        """ Generate text with a prompt and split into tokens of max length n. """
        mode = mode

        # Ensure that max_tokens is not greater than 2000
        self.prompt_list = self.tokenize(string = text)

        self.output = str()
        # Calculate the time elapsed since the last API call
        current_time = time.monotonic()
        progress = 1
        query = 0
        generated_text = str()

        for chunck in self.prompt_list:

            query = str(mode + '"Document: ' + extra + '"' + f' "[Deel {progress} van de {len(self.prompt_list)}] ' + self.prompt + '\n' +  chunck + '"')

            self.query = query
            self.count_tokens(query)

            # print(query.replace("\n", " "))
            # Generate text with the OpenAI API
            done = False
            while done is not True:
                start_time = time.time()

                tokens_to_send = self.count_tokens(query)
                self.wait_for_token_availability(tokens_to_send)
                print(f"\rProcessing chunk {progress} out of {len(self.prompt_list)}", sep='', end='')
                print(f'\nSending {tokens_to_send+110} tokens.')
                print('Processing')

                try:

                    response = openai.ChatCompletion.create(
                        # model="gpt-3.5-turbo",
                        model = "gpt-3.5-turbo-16k",

                        messages=[
                            {"role": "system", "content": "Je bent chatgpt, een persoonlijke assistent. "
                                                          "Je maakt teksten overzichtelijk. "
                                                          "Lees de vraag goed en antwoord in het Nederlands. "},
                            {"role": "user", "content": query + '. '},
                            # {"role": "user", "content": chunck + '.'}
                        ],

                        temperature = 0.1,  # higher more random
                        max_tokens = self.desired_output_length,  # The maximum number of tokens to generate in the completion.
                        # So 0.1 means only the tokens comprising the top 10% probability mass are considered.
                        frequency_penalty = 1,  # decreasing the model's likelihood to repeat the same line verbatim.
                        presence_penalty = 1,  # likelihood to talk about new topics

                    )
                    # Update the last API call time
                    self.last_call_time = time.monotonic()

                    # print(response.choices[0])
                    # Get the generated text from the OpenAI API response
                    generated_text = response.choices[0].message.content
                    print(generated_text)
                    # Print the progress counter

                    # self.progress_bar(progress, len(self.prompt_list))


                    # This section times that calls, so we don't exceed 60 calls per minute
                    end_time = time.time()
                    time_taken = end_time - start_time
                    if time_taken < self.min_time_between_calls:
                        # time.sleep(self.min_time_between_calls - time_taken)
                        time.sleep(1)
                    self.output += f'\n[Deel {progress} van de {len(self.prompt_list)}]\n' + generated_text
                    progress += 1

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

        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-16k")
        tokens = encoding.encode(string)
        tokens = [encoding.decode([token]) for token in tokens]
        num_tokens = len(tokens)
        num_chunks = (num_tokens + n - 1) // n
        chunks = [tokens[i * n:(i + 1) * n] for i in range(num_chunks)] # Joins all tokens to create

        return [''.join(chunk) for chunk in chunks]

    def count_tokens(self,string):
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-16k")
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

    # with open(r'C:\Users\danie\OneDrive\Documenten\GitHub\Chatgpt-bulk-query\SLA filter\SLA Beschrijving van de maatregel lijst.txt', encoding = 'utf8', errors='replace') as f:
    #     text = f.read()
    # text = text[0:5000-64]

    text_to_send = '''Op basis van andere woonzorgvisies van gemeenten willen wij de ontvangen documenten graag door jou laten onderzoeken op onderstaande thema’s/onderwerpen Demografie, woningmarkt, zorgbehoefte, leefomgeving, samenwerking en participatie. Geef per thema een samenvatting wat er in de bijgaande tekst wordt genoemd. 

Hier is extra informatie over de categorieen:

- Demografie
Beschrijving van bevolking en sociale samenhang in Hoorn. Ziet vooral op het inzicht
krijgen in de lokale demografische ontwikkeling.
Trefwoorden hierbij zijn onder andere: bevolkingsopbouw, doelgroepen, ouderen,
kwetsbaren, inwoners, bevolkingsprognose.
- Woningmarkt
Beschrijving van de beschikbare woningen en de noodzakelijke aanpassingen om tegemoet
te komen aan de specifieke behoeften van inwoners. Ziet voornamelijk op het inzicht geven
in de vraag en het aanbod van passende woningen.
Trefwoorden hierbij zijn onder andere: huisvesting(sopgave), passende woningen,
(geclusterde) woonvormen, woonwensen, woningvoorraad, spreiding, transformatie,
(sociale) huurwoningen, woningbouwcorporatie, gezinswoningen, doorstroming,
zelfstandige woningen, appartementen, woongebieden, vastgoed, nieuwbouw
(ontwikkeling).
- Zorgbehoefte
Beschrijving van de meest voorkomende manieren van zorgverlening binnen de gemeente
Hoorn. Ziet voornamelijk op het inzicht geven in de vraag naar verschillende zorgvormen,
het beschikbare aanbod daarvan en hoe deze zorg wordt georganiseerd en verstrekt.
Trefwoorden hierbij zijn onder andere: intramuraal, extramuraal, zorgvormen,
verblijfsvormen, 24-uur zorg, beperking, verpleegd wonen, kortdurend verblijf, zelfstandig
wonen, thuiszorg, ondersteuning, woningaanpassing, (kwetsbare) doelgroepen,
dagbesteding, huishoudelijke hulp, Wet maatschappelijke ondersteuning 2015 (Wmo
2015), Wet langdurige zorg (Wlz), Zorgverzekeringswet (Zvw).
- Leefomgeving
Beschrijft hoe de fysieke woonomgeving is ontworpen en wordt aangepast om tegemoet te
komen aan de specifieke behoeften van de bewoners, zoals toegankelijkheid, veiligheid en
leefbaarheid. Denk hierbij aan het voorzieningenniveau binnen de gemeente op het gebied
van wonen en zorg. Het benadrukt doelen zoals het bevorderen van sociale interactie,
autonomie, welzijn, en de algemene tevredenheid van bewoners.
Trefwoorden hierbij zijn onder andere: welzijn, voorzieningen, woonomgeving, gelukkig,
ongelukkig, gezond, eenzaam, overlast, veiligheid, leefbaarheid, tevredenheid, autonomie,
interactie
- Samenwerking
Beschrijving van reeds bestaande samenwerkingen en partnerschappen. Kan onder andere
beschrijven hoe de gemeente momenteel al samenwerkt met zorgaanbieders,
woningbouwcorporaties en zorgverzekeraars om goede zorg en ondersteuning te bieden.
Trefwoorden hierbij zijn onder andere: samenwerking, afspraken, partnerschap, convenant,
zorgverzekeraar, zorgkantoor, zorgaanbieders
- Participatie
Beschrijft op welke wijze de gemeente inwoners betrekt bij het maken van plannen rondom
wonen en zorg en op welke wijze hiermee rekening wordt gehouden.
Trefwoorden hierbij zijn: participatie, betrokkenheid, besluitvorming, inspraak.
'''
    x = OpenAIGPT(text_to_send).count_tokens(text_to_send)



