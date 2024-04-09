import random
import pandas as pd
from sklearn.utils import shuffle

if __name__ == "__main__":
    CREATOR_NAMES = ["itsclarityco", "thebackstagebunch", "welloshow"]
    SOURCES = ["tiktok", "youtube"]
    SAMPLE_SIZE = 15
    metadata_creator_list = []
    metadata_source_list = []
    random_sample_list = []

    for source in SOURCES:
        for creator in CREATOR_NAMES:
            file_to_sample = f"./comments/{source}_{creator}.csv"
            df_comments = pd.read_csv(file_to_sample)
            comment_list = df_comments['Comment'].values.tolist()

            # concat all lists
            random_sample_list += random.sample(comment_list, SAMPLE_SIZE)
            metadata_creator_list += [creator] * SAMPLE_SIZE
            metadata_source_list += [source] * SAMPLE_SIZE

    master_data = {"Creator": metadata_creator_list, "Source": metadata_source_list, "Comments": random_sample_list}
    df_master = pd.DataFrame(data=master_data)
    df_master_shuffled = shuffle(df_master)

    csv_file_name = './data/sample_comments.csv'
    df_master_shuffled.to_csv(csv_file_name, index=True)
