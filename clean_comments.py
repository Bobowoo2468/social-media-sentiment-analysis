import pandas as pd
import spacy
import re
import string
import nltk
from googletrans import Translator, constants

data = pd.read_csv('./comments/youtube_thebackstagebunch.csv')
nlp = spacy.load("en_core_web_sm")

FILTER_WORDS = ['hi', 'im']


def clean_comment(comment):
    comment = comment.lower()

    # remove line breaks
    comment = re.sub(r'\n', '', comment)

    # remove punctuation with regex
    translator = str.maketrans('', '', string.punctuation)
    comment = comment.translate(translator)

    # remove stop words
    comment = comment.split()
    words_to_filter = nltk.corpus.stopwords.words("english")
    words_to_filter += FILTER_WORDS

    # filter comments
    comment_filtered = [word for word in comment if not word in words_to_filter]

    if len(comment_filtered) < 3:
        return None

    else:
        cleaned_comment = nlp(' '.join(comment_filtered))
        # comment_stemmed = [y.lemma_ for y in cleaned_comment]
        # comment_stemmed = ' '.join(comment_stemmed)
        # print(comment_stemmed)
        return cleaned_comment


def translate_comment(comment):
    translator = Translator()
    translated_comment = translator.translate(comment)
    if translated_comment.src != "en":
        print(
            f"{translated_comment.origin} ({translated_comment.src}) --> {translated_comment.text} ({translated_comment.dest})")
    return translated_comment


if __name__ == "__main__":
    for comment in data['Comment']:
        cleaned_comment = clean_comment(comment)
        translate_comment(cleaned_comment)
