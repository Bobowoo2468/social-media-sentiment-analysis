import random
import pandas as pd
from sklearn.utils import shuffle


class RandomisedSampler:
    def __init__(self, creators, sample_size, input_dir, output_dir, output_filename):
        self.creators = creators
        self.sample_size = sample_size
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.output_filename = output_filename

    def random_sample(self):
        metadata_creator_list = []
        metadata_source_list = []
        random_sample_list = []

        for source in ["tiktok", "youtube"]:
            for creator in self.creators:
                file_to_sample = f"./{self.input_dir}/{source}_{creator}.csv"
                df_comments = pd.read_csv(file_to_sample)
                comment_list = df_comments['Comment'].values.tolist()

                # concat all lists
                random_sample_list += random.sample(comment_list, self.sample_size)
                metadata_creator_list += [creator] * self.sample_size
                metadata_source_list += [source] * self.sample_size

        master_data = {"Creator": metadata_creator_list, "Source": metadata_source_list, "Comments": random_sample_list}
        df_master = pd.DataFrame(data=master_data)
        df_master_shuffled = shuffle(df_master)

        csv_file_name = f'./{self.output_dir}/{self.output_filename}.csv'
        df_master_shuffled.to_csv(csv_file_name, index=True)
        print(f"You can find your sampled file as {csv_file_name}")


# ensure you input_dir has file names with format "./{input_dir}/{source}_{creator}.csv"
# input_dir -> directory name
# source -> youtube or tiktok
# creator -> within list of creators

# do ensure that that your column containing the comments is named 'Comment'
def create_sample(creators, sample_size, input_dir, output_dir, output_filename):
    rs = RandomisedSampler(creators, sample_size, input_dir, output_dir, output_filename)
    rs.random_sample()


if __name__ == "__main__":
    CREATOR_NAMES = ["itsclarityco", "thebackstagebunch", "welloshow"]
    create_sample(CREATOR_NAMES, 20, "comments", "test", "sample")
