from comment_parser import CommentParser
import pandas as pd


class SentimentToxicityLabeler:
    def __init__(self, file, output_file):
        words_to_filter = ["hi"]
        df = pd.read_csv(file, index_col=0)

        for k, v in df.iterrows():
            comment = v["Comment"]
            translated_comment = CommentParser.translate_comment(comment).text
            cleaned_comment = CommentParser.clean_comment(translated_comment, words_to_filter)

            if cleaned_comment is not None:
                label = CommentParser.comment_sentiment(cleaned_comment).output.lower()
                toxicity_label = CommentParser.comment_toxicity(translated_comment)
            else:
                label = "neu"
                toxicity_label = "n"
            df.loc[k, "Sentiment"] = label
            df.loc[k, "Toxicity"] = toxicity_label
        df.to_csv(output_file)
        print(f"You can find your labeled file as: {output_file}")


def parse_output_file_name(self, file_name):
    fn = file_name.split(".csv")[0]
    return f"{fn}_coded.csv"


if __name__ == "__main__":
    file = "./comments/youtube_itsclarityco.csv"
    output_file = "./test/youtube_itsclarityco.csv"
    stl = SentimentToxicityLabeler(file, output_file)
