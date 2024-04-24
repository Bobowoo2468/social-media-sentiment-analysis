import comment_parser as cparse
import pandas as pd


def parse_output_file_name(file_name):
    fn = file_name.split(".csv")[0]
    return f"{fn}_coded.csv"


if __name__ == "__main__":
    file = "./comments/youtube_welloshow.csv"
    output_file = parse_output_file_name(file)
    df = pd.read_csv(file, index_col=0)

    for k, v in df.iterrows():
        comment = v["Comment"]
        translated_comment = cparse.translate_comment(comment).text
        cleaned_comment = cparse.clean_comment(translated_comment)

        if cleaned_comment is not None:
            label = cparse.comment_sentiment(cleaned_comment).output.lower()
            toxicity_label = cparse.comment_toxicity(cleaned_comment)
        else:
            label = "neu"
            toxicity_label = "n"
        df.loc[k, "Sentiment"] = label
        df.loc[k, "Toxicity"] = toxicity_label

    df.to_csv(output_file)
