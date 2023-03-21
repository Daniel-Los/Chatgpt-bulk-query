import nltk

def NLTK_Tokenizer(text, max_tokens):
    """
    Splits up a text based on a maximum amount of tokens using the nltk library.
    """
    tokenizer = nltk.tokenize.word_tokenize
    tokens = tokenizer(text)
    num_tokens = len(tokens)
    if num_tokens <= max_tokens:
        return [text]
    else:
        num_splits = num_tokens // max_tokens + 1
        split_size = num_tokens // num_splits + 1
        splits = [tokens[i:i+split_size] for i in range(0, num_tokens, split_size)]
        return [' '.join(split) for split in splits]

if __name__ == '__main__':
    # Example usage
    text = "This is a sample text to demonstrate splitting based on a maximum number of tokens."
    max_tokens = 1000
    splits = NLTK_Tokenizer(text, max_tokens)
    print(splits)

    # https://www.nltk.org/data.html