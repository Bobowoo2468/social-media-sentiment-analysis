import pandas as pd
import spacy
import re
import string
import nltk
import os
from googletrans import Translator
from pysentimiento import create_analyzer
from pysentimiento.preprocessing import preprocess_tweet

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = 'python'

emotion_analyzer = create_analyzer(task="emotion", lang="en")
sentiment_analyzer = create_analyzer(task="sentiment", lang="en")
toxicity_analyzer = create_analyzer(task="hate_speech", lang="en")

data = pd.read_csv('./comments/youtube_thebackstagebunch.csv')
nlp = spacy.load("en_core_web_sm")

FILTER_WORDS = ['hi', 'im']


def clean_comment(comment):
    comment = comment.lower()

    # remove line breaks
    comment = re.sub(r'\n', '', comment)

    # remove any tags
    comment = comment.split()
    comment = [w for w in comment if not w.startswith("@")]
    comment = ' '.join(comment)

    # remove punctuation with regex
    translator = str.maketrans('', '', string.punctuation)
    comment = comment.translate(translator)

    # remove stop words
    comment = comment.split()

    words_to_filter = nltk.corpus.stopwords.words("english")
    words_to_filter += FILTER_WORDS

    # filter comments
    comment_filtered = [word for word in comment if not word in words_to_filter]

    # clean
    # if len(comment_filtered) < 3:
    #     return None
    #
    # else:
    cleaned_comment = nlp(' '.join(comment_filtered))
    final_cleaned_comment = preprocess_tweet(cleaned_comment.text, lang="en")
    # comment_stemmed = [y.lemma_ for y in cleaned_comment]
    # comment_stemmed = ' '.join(comment_stemmed)
    return final_cleaned_comment


def translate_comment(comment):
    translator = Translator()

    if len(comment) == 0:
        return ""

    translated_comment = translator.translate(comment)
    # if translated_comment.src != "en":
    #     print(
    #         f"{translated_comment.origin} ({translated_comment.src}) --> "
    #         f"{translated_comment.text} ({translated_comment.dest})")
    return translated_comment


def comment_sentiment(comment):
    return sentiment_analyzer.predict(comment)


def comment_toxicity(comment):
    output = toxicity_analyzer.predict(comment).output
    if len(output) > 0:
        return "y"
    else:
        return "n"


def full_comment_toxicity(comment):
    return toxicity_analyzer.predict(comment)


if __name__ == "__main__":
    print("")

    ### ---------- Example Usage: -------------- ###
    # comment = "Boleh nampak sah jufri tengah berbual world kat podcast wellow"
    # comment = translate_comment(comment).text
    # print(comment)
    # cleaned = clean_comment(comment)
    # sentiment = comment_sentiment(cleaned)
    # print(sentiment)

    ### ---------- Example Usage: -------------- ###

    # parsed_comments = []
    # comment_count = 0
    #
    # for comment in data['Comment']:
    #     if comment_count == 20:
    #         break
    #
    #     # translate comment before cleaning comment
    #     translated_comment = translate_comment(comment).text
    #     parsed_comment = clean_comment(translated_comment)
    #     if parsed_comment is not None:
    #         parsed_comments.append(parsed_comment)
    #         comment_count += 1
    #
    # for c in parsed_comments:
    #     emotion = emotion_analyzer.predict(c)
    #     sentiment = sentiment_analyzer.predict(c)
    #     toxicity = toxicity_analyzer.predict(c)
    #     print(c, sentiment.output, emotion.output)
    #     print(toxicity)
