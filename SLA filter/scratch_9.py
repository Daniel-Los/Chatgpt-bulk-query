import nltk
from collections import Counter
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt




def get_common_nouns(text):
    # Tokenize the text into words
    tokens = nltk.word_tokenize(text)

    # Get the part-of-speech tags for each word
    pos_tags = nltk.pos_tag(tokens)

    # Filter out all non-noun words
    stop_words = set(stopwords.words('dutch'))

    nouns = [word.lower() for word, pos in pos_tags if pos.startswith('NN') and word.lower() not in stop_words]

    # Count the frequency of each noun
    noun_counts = Counter(nouns)

    return noun_counts

with open(r'C:\Users\d.los\PycharmProjects\documentsearch\SLA filter\SLA Beschrijving van de maatregel lijst.txt', 'r', encoding = 'utf8') as f:
    text = f.read()

common_nouns = get_common_nouns(text)
print(common_nouns)

wordcloud = WordCloud()
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='tab20')
wordcloud.generate_from_frequencies(common_nouns)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()