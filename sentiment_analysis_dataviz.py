import pandas as pd

if __name__ == "__main__":
    creators = ["itsclarityco", "thebackstagebunch", "welloshow"]

    is_toxic_count = 0
    num_comments = 0
    pos_count = 0
    neu_count = 0
    neg_count = 0

    for creator in creators:
        file = f"./comments/tiktok_{creator}_coded.csv"
        df = pd.read_csv(file, index_col=0)

        is_toxic_count += (df["Toxicity"] == "y").sum()
        pos_count += (df["Sentiment"] == "pos").sum()
        neu_count += (df["Sentiment"] == "neu").sum()
        neg_count += (df["Sentiment"] == "neg").sum()
        num_comments += len(df)
        # print(df[df["Toxicity"] == "y"]["Comment"])

    pos_perc = round((pos_count / num_comments) * 100, 2)
    neu_perc = round((neu_count / num_comments) * 100, 2)
    neg_perc = round((neg_count / num_comments) * 100, 2)

    print(f"Sentiment of comments for Tiktok: "
          f"POS -> {pos_count}( {pos_perc}% ) "
          f"NEU -> {neu_count}( {neu_perc}% ) "
          f"NEG -> {neg_count}( {neg_perc}% )")
    print(f"Number of toxic comments for Tiktok: {is_toxic_count}")
    print(f"Total number of comments for Tiktok: {num_comments}")

    percentage_toxicity = round((is_toxic_count / num_comments) * 100, 2)
    print(f"Percentage of toxic comments for Tiktok: {percentage_toxicity}%")

    is_toxic_count = 0
    num_comments = 0
    pos_count = 0
    neu_count = 0
    neg_count = 0

    for creator in creators:
        file = f"./comments/youtube_{creator}_coded.csv"
        df = pd.read_csv(file, index_col=0)

        is_toxic_count += (df["Toxicity"] == "y").sum()
        pos_count += (df["Sentiment"] == "pos").sum()
        neu_count += (df["Sentiment"] == "neu").sum()
        neg_count += (df["Sentiment"] == "neg").sum()
        num_comments += len(df)
        # print(df[df["Toxicity"] == "y"]["Comment"])

    pos_perc = round((pos_count / num_comments) * 100, 2)
    neu_perc = round((neu_count / num_comments) * 100, 2)
    neg_perc = round((neg_count / num_comments) * 100, 2)

    print(f"Sentiment of comments for Youtube: "
          f"POS -> {pos_count}( {pos_perc}% ) "
          f"NEU -> {neu_count}( {neu_perc}% ) "
          f"NEG -> {neg_count}( {neg_perc}% )")

    print(f"Number of toxic comments for Youtube: {is_toxic_count}")
    print(f"Total number of comments for Youtube: {num_comments}")

    percentage_toxicity = round((is_toxic_count / num_comments) * 100, 2)
    print(f"Percentage of toxic comments for Youtube: {percentage_toxicity}%")
