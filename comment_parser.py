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


class CommentParser:
    @staticmethod
    def clean_comment(comment, words_to_filter):
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

        # remove stopwords and filter specific words
        comment = comment.split()

        words_to_filter = nltk.corpus.stopwords.words("english")
        words_to_filter += words_to_filter
        comment_filtered = [word for word in comment if not word in words_to_filter]

        cleaned_comment = nlp(' '.join(comment_filtered))
        final_cleaned_comment = preprocess_tweet(cleaned_comment.text, lang="en")
        return final_cleaned_comment

    @staticmethod
    def translate_comment(comment):
        translator = Translator()

        # if comment is empty, nothing to translate
        if len(comment) == 0:
            return ""

        translated_comment = translator.translate(comment)
        # if translated_comment.src != "en":
        #     print(
        #         f"{translated_comment.origin} ({translated_comment.src}) --> "
        #         f"{translated_comment.text} ({translated_comment.dest})")
        return translated_comment

    @staticmethod
    def comment_sentiment(comment):
        return sentiment_analyzer.predict(comment)

    @staticmethod
    def comment_toxicity(comment):
        output = toxicity_analyzer.predict(comment).output
        if len(output) > 0:
            return "y"
        else:
            return "n"

    @staticmethod
    def full_comment_toxicity(comment):
        return toxicity_analyzer.predict(comment)


if __name__ == "__main__":
    pass
    # comment = "hi I am @ boy"
    # FILTER_WORDS = ['hi', 'hihi', 'hihihi']
    # cleaned_comment = CommentParser.clean_comment(comment, FILTER_WORDS)
    # print(cleaned_comment)  # cleaned comment -> hi boy (filtered @ and hi)

    # ## ---------- Example Usage: -------------- ###
    # comment = "Boleh nampak sah jufri tengah berbual world kat podcast wellow"
    # comment = CommentParser.translate_comment(comment).text
    # print(comment)
    # FILTER_WORDS = ['hi', 'hihi', 'hihihi']
    # cleaned_comment = CommentParser.clean_comment(comment, FILTER_WORDS)
    # sentiment = CommentParser.comment_sentiment(cleaned_comment)
    # print(sentiment)
    #
    # ## ---------- Example Usage: -------------- ###
    #
    # comments = []
    # parsed_comments = []
    #
    # for comment in comments:
    #     # translate comment before cleaning comment
    #     translated_comment = CommentParser.translate_comment(comment).text
    #     parsed_comment = CommentParser.clean_comment(translated_comment)
    #     if parsed_comment is not None:
    #         parsed_comments.append(parsed_comment)
    #
    # for c in parsed_comments:
    #     emotion = emotion_analyzer.predict(c)
    #     sentiment = sentiment_analyzer.predict(c)
    #     toxicity = toxicity_analyzer.predict(c)
    #     print(c, sentiment.output, emotion.output)
    #     print(toxicity)
