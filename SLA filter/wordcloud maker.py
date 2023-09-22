import nltk
from collections import Counter
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import base64


def get_common_nouns(text):
    # Tokenize the text into words
    tokens = nltk.word_tokenize(text)

    # Get the part-of-speech tags for each word
    pos_tags = nltk.pos_tag(tokens)

    # Filter out all non-noun words
    stop_words = set(stopwords.words('dutch'))

    nouns = [word.lower() for word, pos in pos_tags if pos.startswith('NN') and word.lower() not in stop_words]

    # Count the frequency of each noun
    print(nouns)
    noun_counts = Counter(nouns)

    return noun_counts

def make_vector(text):
    # Tokenize the text into words
    tokens = nltk.word_tokenize(text)

    # Get the part-of-speech tags for each word
    pos_tags = nltk.pos_tag(tokens)

    # Filter out all non-noun words
    stop_words = set(stopwords.words('dutch'))

    nouns = [word.lower() for word, pos in pos_tags if pos.startswith('NN') and word.lower() not in stop_words]

    ## module not installed yet
    # model1 = Word2Vec(text, min_count=3,
    #                   size=100, window=3, workers=8)

import docx
def gettext(filename):
    # gets text from a docx file
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
import os
text = str()
pathlist = [path for path in os.walk(r'C:\Users\d.los\PycharmProjects\documentsearch\processed\Deurne - Deelnemer')]
for path in pathlist[0][2][0:3]:
    string = rf'C:\Users\d.los\PycharmProjects\documentsearch\processed\Deurne - Deelnemer\{path}'
    try:
        with open(string, 'r', encoding = 'utf8') as f:
            text += f.read()
    except:
        pass

print(len(text))

# text = gettext(r'C:\Users\d.los\PycharmProjects\documentsearch\output\Deurne - Deelnemer_samengevoegd_gpt.docx')

# with open(r'SLA Beschrijving van de maatregel lijst.txt', 'r', encoding = 'cp437') as f:
#     text = f.read()

common_nouns = get_common_nouns(text)
# print(common_nouns)

wordcloud = WordCloud()
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Blues')
wordcloud.generate_from_frequencies(common_nouns)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')

plt.savefig('wordcloud.png')
print('done')