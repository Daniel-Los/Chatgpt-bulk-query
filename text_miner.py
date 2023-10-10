import os

from OpenAIGPT import OpenAIGPT
import tiktoken

import pandas as pd

# Use your own API key
from api_import import api_import

from uniquename import uniquename

import io
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import docx

class Text_Miner():
    def __init__(self, root, mode, project_name, output_folder, word_formatting):

        self.key = api_import()
        # the base of the folder that you want to siff through as input
        self.root = root

        self.prompt = str() # the actual prompt that will be sent to the ai
        self.project_name = project_name
        self.output_folder = output_folder
        self.word_formatting = word_formatting

        self.mode = mode # can be used to add additional stuff to the prompt

        self.name = str(os.path.basename(root))

        # TODO: specify modes that this thing can operate with

        # the list of documents for every file in the root
        self.doclist = {}
        self.doclist_short = {}

        # list of all strings in all docments per dict.
        self.stringdict = {}
        self.outputdict = {}

        self.df = pd.DataFrame()

        # make an unique filename
        # self.file_name = str("Output " + str(time.strftime("%m %d %H%M%S ")) + ".json")

        self.process_speed = 50  # docs per minute
        self.max_query_length = 1000

        self.output = {}
        self.estimated_tokencount = False
        self.estim_costs = {}
        self.accord = False
        self.AI = OpenAIGPT(self.prompt)

        self.table_data = []

    def get_structure(self):
        # this fucntion reads in all the filenames, as well as order them per extension into a dict.
        self.doclist = {}
        self.doclist_short = {}
        for root, place, documents in os.walk(self.root):
            print(f'Documents found: {str(documents)}')
            for document in documents:
                #if document != "Beleidsnota Ruimte voor Ruimte gemeente Zundert _ Lokale wet- en regelgeving.pdf":
                    #continue

                # add extension name into dict
                # name, extension = document.split(".", 1)
                name, extension = os.path.splitext(document)

                if extension not in self.doclist.keys():
                    self.doclist[extension] = []
                    self.doclist_short[extension] = []

                # add document file location to the dict
                self.doclist[extension].append(root + '\\' + document)
                # add document name to the sort dict
                self.doclist_short[extension].append(document)
                # create a dictionary per document name so the text can be put in there
                # self.stringlist[name] = []

    def scrubstring(self, text):
        text = text.replace("\x00", "")  # Verwijder NULL-karakters
        text = re.sub(r'[^\x00-\x7F]+', '', text)  # Verwijder niet-UTF-8-karakters
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")

        # Vervang opeenvolgende interpunctietekens en spaties door een enkel punt of spatie
        text = re.sub(r'([.!?_ -])\1+', r'\1', text)

        # Identificeer en verwijder reeksen van 10 of meer cijfers
        pattern1 = r'\d{10,}'  # Dit patroon matcht reeksen van 10 of meer cijfers
        pattern2 = r'\d+(\s|\.)+\d+'  # Dit patroon matcht cijferreeksen gescheiden door spaties of punten
        combined_pattern = f'({pattern1}|{pattern2})'
        text = re.sub(combined_pattern, '', text)

        # Identificeer en verwijder opeenvolgende herhaalde voorkomens van tekens (bijvoorbeeld: - - - -)
        text = re.sub(r'([- ._])\1+', r'\1', text)
        patroon = r'(\s?-){2,}\s?'
        text = re.sub(patroon, '', text)
        text = ' '.join(text.split())
        text = re.sub(r'([.!?_ -])\1+', r'\1', text)
        return text

    def add_ocr(self):
        # TODO: add a thing that adds ocr with pytesseract to the pdfs so images and unselectable pdf can be loaded in
        pass
        # self.stringlist[pdfpath].append(pytesseract.image_to_string(
        #       pdfpath,
        #       lang=self.target_language,
        #       config='--psm 6')
        #       ) # TODO: this function is still broken

    def read_files(self):
        # this is supposed to read all files that have a sensible extension (currently: doc, (selectable) pdf)
        def gettext(filename):
            # gets text from a docx file
            doc = docx.Document(filename)
            fullText = []
            for para in doc.paragraphs:
                fullText.append(para.text)
            return '\n'.join(fullText)

        def convert_pdf_to_txt(path):
            print("Importing file: {}".format(path))
            processed_file = ['processed']
            path_list = path.split("\\")
            processed_file.append(path_list[-2])
            processed_file.append(path_list[-1].split('.')[0] + '.txt')
            processed_file = "\\".join(processed_file)

            try:
                with open(processed_file, 'r', encoding="utf-8") as f:
                    text = f.read()
                    print("Using pre-processed file.")
                    return text
            except FileNotFoundError:
                print("No pre-processed file found.")
            except Exception as e:
                print(f"Error while reading pre-processed file: {e}")

            resource_manager = PDFResourceManager()
            out_file = io.StringIO()
            # codec = 'utf-8'
            laparams = LAParams()
            device = TextConverter(resource_manager, out_file, laparams=laparams)
            fp = open(path, 'rb')
            interpreter = PDFPageInterpreter(resource_manager, device)
            pdf_size = sum(1 for _ in PDFPage.get_pages(fp, check_extractable=True))
            print("", sep='\n', end='')
            count_pages = 0
            for page in PDFPage.get_pages(fp, check_extractable=True):
                interpreter.process_page(page)
                count_pages += 1
                print("\rProgress: {} out of {} pages.\t".format(count_pages, pdf_size), sep='', end='')
            print("", sep='', end='\n')
            fp.close()
            device.close()
            text = out_file.getvalue()
            out_file.close()
            
            #create a folder for the txt document
            folder = processed_file.split('\\')
            folder = folder[:-1]
            folder = "\\".join(folder)
            if not os.path.exists(folder):
                try:
                    os.makedirs(folder)
                    print(f"Folder '{folder}' created successfully.")
                except OSError as e:
                    print(f"Error creating folder '{folder}': {e}")
            else:
                print(f"Folder '{folder}' already exists.")
            
            #write the pre-process to a txt
            text = self.scrubstring(text)
            with open(processed_file, 'w', encoding="utf-8") as f:
                f.write(text)

            return text

        doccount = 0
        charcount = 0
        for extension in self.doclist.keys():

            if  extension == '.pdf':
                for item in self.doclist[extension]:
                    name = item.split('\\', -1)[-1] # os.path.base(item) optional
                    text = convert_pdf_to_txt(item)
                    text = self.scrubstring(text)
                    self.stringdict.setdefault(name, [])
                    self.stringdict[name].append(text)

            if  extension == '.docx':
                for item in self.doclist[extension]:
                    # counts how many files are processed
                    doccount += 1
                    # gets the name of the file
                    name = item.split('\\', -1)[-1]
                    # extracts data
                    text = gettext(item)
                    # stores the string in the stringdict
                    text = self.scrubstring(text)

                    self.stringdict.setdefault(name, [])
                    self.stringdict[name].append(text)

            if extension == '.txt':
                #todo: test
                for item in self.doclist[extension]:

                    name = item.split('\\', -1)[-1]  # os.path.base(item) optional
                    with open(item) as doc:
                        text = doc.read(errors='ignore')

                    text = self.scrubstring(text)
                    self.stringdict.setdefault(name, [])
                    self.stringdict[name].append(text)

            if extension == '.xlsx':
                print('xlsx files are not (yet) supported')

            else:
                doccount += 1
            # print(self.stringdict)

    def num_tokens_from_messages(self, messages, model="gpt-3.5-turbo-0301"):
        """Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo":
            print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
            return self.num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
        elif model == "gpt-4":
            print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
            return self.num_tokens_from_messages(messages, model="gpt-4-0314")
        elif model == "gpt-3.5-turbo-0301":
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif model == "gpt-4-0314":
            tokens_per_message = 3
            tokens_per_name = 1
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens

    def estimate_costs(self):
        '''
        This function creates an estimate of the costs by examining the text loaded in.
        It counts the amount of text by breaking it up into chuncks of length 1000 tokens (self.max_query_length)
        Then it multiplies this length with the costs per 1000 tokens as of 02-2023
        TODO: limitation is that gpt4 has different costs for the 32.000 token model and 8.000 token model
        '''
        length = 0
        for key, value in self.stringdict.items():
            length += len(value)

        queries = length // self.AI.desired_output_length

        seconds = queries * self.process_speed / 60
        seconds = round(seconds, 2)

        # print(f'Estimated time needed for free version is {seconds}')

        tokencount = 0
        doccount = 0
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0301")
        for string in self.stringdict.values():
            # print(string[0])
            prompt_to_inspect = string[0]
            doccount +=1

            #tokencount += len(NLTK_Tokenizer(prompt_to_inspect, 1000))
            tokencount += len(encoding.encode(prompt_to_inspect))

        # update the user on costs and time
        iterations = tokencount//self.AI.desired_output_length + 1
        estimated_time = iterations * self.AI.min_time_between_calls
        minutes, seconds = divmod(estimated_time, 60)
        print(f'Number of documents: {doccount} with {tokencount} tokens')
        print(f'Estimated iterations needed are: {iterations}\n ')
              # f'Depending on speed) Min estimated time (~1s/it): {int(minutes)}:{int(seconds)}\n')

        # self.estim_costs['GPT4-8k'] = str(round(tokencount * 0.06, 2)) + ' EUR'
        # self.estim_costs['davinci'] = str(round(tokencount * 0.02,2)) +  ' EUR'
        # self.estim_costs['ada'] = str(round(tokencount * 0.0004, 2)) + ' EUR'
        self.estim_costs['GPT3.5 Turbo'] = str(round(tokencount * 0.008 / 1000, 2)) + ' EUR'
        print(f'Estimated costs are {self.estim_costs}\n')

        self.estimated_tokencount = tokencount

        return self.estim_costs

    # Functions and Objects
    def agree(self):
        if self.estimated_tokencount:
            print(f"Do you agree with the estimated costs: {self.estim_costs} for analysing the documents.")
            userinput = input("Return yes or no")
            if userinput.lower() == "yes":
                print("Input was yes, continuing the process")
                self.accord = True
            else:
                print("Input was not yes \n Terminating process...")
        else:
            print("No cost estimate has been done, please run self.estimate_costs()")


    def AI_interact(self):
        '''
        This section actually loads the text into openai
        :return:
        '''
        docprogress = 1
        for docname, text in self.stringdict.items():
            print(f"\n'{docname}' \n[{docprogress} out of {len(self.stringdict)} documents]")
            # generate_text_with_prompt splits the prompt into multiple sections if too long
            # then it gets new data from the chatGPT

            output = self.AI.generate_text_with_prompt(prompt=text, mode=str(self.mode), extra = f"Documentnaam: {docname}")

            self.outputdict.setdefault(docname, [])
            self.outputdict[docname].append(output)
            docprogress += 1
            print('\n')


    def write_to_file(self, dictionary, extra = '', formatting = True):
        #TODO: add a processor for the filename so it appears better (at least filter _ .pdf and ')

        ''' This writes the output to a formatted document '''

        # if 'bulletpoints' in self.mode or 'bullet points' in self.mode:
        #     # This loop splits the sections of the text for bulletpoints
        #     rows = []
        #     for document_name, string in dictionary.items():
        #         elements = string[0].split('\n- ')
        #         for element in elements:
        #             row = [document_name, element]
        #             rows.append(row)


        doc = docx.Document()
        name = uniquename(self.output_folder + '/' + self.name + extra + '_gpt.docx')
        if formatting:
            # This section defines the layout of the document
            doc.add_heading(str(self.name+extra),0) # adds the name of the document as title
            doc.add_heading([i + ' ' for i in dictionary.keys()], 5) # adds the list of used documents

            for document_name, string in dictionary.items(): # iterate throught the dictonary: {doc name: GPT output}
                header, extension = os.path.splitext(document_name)
                doc.add_heading(header, 1) # start with the header of the document name
                lines = string[0].split('\n')
                # doc.add_paragraph(f'Chunk: [{index + 1}/{len(lines)}]')
                for index, line in enumerate(lines): # Break each \n into a new line
                    doc.add_paragraph(line) # this adds a '[1/10]' section per paragraph
                    # doc.add_break(WD_BREAK.LINE)
                doc.add_paragraph('')
        else:
            for document_name, string in dictionary.items():
                lines = string[0].split('\n')
                for index, line in enumerate(lines): # Break each \n into a new line
                    doc.add_paragraph(line) # this adds a '[1/10]' section per paragraph
        doc.save(name)
        print(f'Saved as {name}')


    def table_to_csv(self, tabletext):
        # Remove leading/trailing whitespace and split the table into rows
        rows = [row.strip().split('|') for row in tabletext.strip().split('\n')]

        # Extract header and data rows
        header = [cell.strip() for cell in rows[0] if cell.strip()]
        data = [[cell.strip() for cell in row if cell.strip()] for row in rows[1:]]

        # Create a DataFrame using pandas
        df = pd.DataFrame(data, columns=header)

        # Convert DataFrame to CSV
        csv_data = df.to_csv(index=False)
        self.table_data.append(csv_data)
        # Print or save the CSV data
        print(csv_data)
        # You can save it to a file by writing to it:
        # with open('output.csv', 'w') as f:
        #     f.write(csv_data)
        # return csv_data
