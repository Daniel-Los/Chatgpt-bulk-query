import os

import tiktoken

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

print(num_tokens_from_string("tiktoken is great!", "cl100k_base"))

path = r'C:\Users\d.los\Berenschot\Ministerie van Infrastructuur en Waterstaat = vol - 70800 Periodieke rapportage Luchtvaart 16-22 Sodr\2. Beleidsdocumenten, evaluaties en onderzoeken'
pdfs=[]
for pdf in os.listdir(path):
    if not "begroting" in pdf.lower():
        pdfs.append(path+'\\'+pdf)

from text_miner import Text_Miner

tm = Text_Miner(api_key_path=r'C:\Users\d.los\PycharmProjects\documentsearch\api_key.txt')
tm.doclist = {'.pdf': pdfs}
tm.read_files()


