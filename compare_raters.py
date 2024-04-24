import pandas as pd
from collections import Counter
from statsmodels.stats import inter_rater as irr

RATER_NAMES = ["bt", "jl", "jz", "yasmeen"]


def field_check(file_names, mode):
    for file in file_names:
        temp_df = pd.read_excel(file)

        if mode == "sentiment":
            # each file must have columns with "label" and "sentence"
            if "Comments" not in temp_df.columns or "label" not in temp_df.columns:
                print(f"ERROR in {file}: The columns must be named 'label' and 'Comments'")
                return False

            # values should only be pos, neg and neu
            if sorted(temp_df['label'].unique()) != ["neg", "neu", "pos"]:
                print(
                    f"ERROR in {file}: The 'label' column can only contain the values 'neg','neu'','pos' in smal caps.")
                return False

        elif mode == "toxicity":
            if "Comments" not in temp_df.columns or "is_toxic(y/n)" not in temp_df.columns:
                print(f"ERROR in {file}: The columns must be named 'is_toxic(y/n)' and 'Comments'")
                return False

            # values should only be y, n
            if sorted(temp_df['is_toxic(y/n)'].unique()) != ["n", "y"]:
                print(
                    f"ERROR in {file}: The 'is_toxic(y/n)' column can only contain the values 'y' or 'n' in smal caps.")
                return False
    return True


def combine_ratings(rater_names, mode):
    is_init = True
    for rater in rater_names:
        corr_file_name = f"./manual_coding/{rater}_sample_comments.xlsx"
        temp_df = pd.read_excel(corr_file_name)

        if mode == "sentiment":
            col_to_rename = "label"
        else:
            col_to_rename = "is_toxic(y/n)"
        temp_df.rename(columns={col_to_rename: rater}, inplace=True)

        if is_init:
            df = temp_df
            if mode == "sentiment":
                df = df.drop(['Unnamed: 0', 'is_toxic(y/n)'], axis=1)
            else:
                df = df.drop(['Unnamed: 0', 'label'], axis=1)
            is_init = False
        else:
            temp_df = temp_df.drop(['Unnamed: 0', 'Comments', 'Creator', 'Source'], axis=1)
            if mode == "sentiment":
                temp_df = temp_df.drop(['is_toxic(y/n)'], axis=1)
            else:
                temp_df = temp_df.drop(['label'], axis=1)

            df = pd.concat([df, temp_df], axis=1)
    return df


def no_agreement_check(df):
    no_agreement_count = 0

    for k, v in df.iterrows():
        top_two_sentiments = Counter(v[3:]).most_common(2)
        no_agreement = False

        if len(top_two_sentiments) > 1:
            no_agreement = (top_two_sentiments[0][1] == top_two_sentiments[1][1])

        if no_agreement:
            df.loc[k, "ground truth"] = "No agreement!"
            no_agreement_count += 1
        else:
            df.loc[k, "ground truth"] = top_two_sentiments[0][0]

    print(f"Number of no agreements: {no_agreement_count}")
    return df


def calculate_fleiss_kappa(df):
    # to calculate Fleiss' Kappa, first we get the values from the labelers as an array
    values = df.iloc[:, 3:-1].values

    # then we aggregate them in the format required by statsmodels and then calculate Kappa
    agg = irr.aggregate_raters(values)
    kappa = irr.fleiss_kappa(agg[0])
    print(f"Fliess Kappa is {kappa}")
    return


def write_agreement_file(df, file_name):
    # create output dir, and save the agreement file
    df.to_excel(f"manual_coding/{file_name}.xlsx")
    print(f"\nAgreement file saved at manual_coding/agreement.xlsx")


if __name__ == "__main__":
    MODE = "toxicity"
    files = []

    for n in RATER_NAMES:
        files.append(f"./manual_coding/{n}_sample_comments.xlsx")

    field_check(files, mode=MODE)
    combined_df = combine_ratings(RATER_NAMES, mode=MODE)
    combined_df_parsed = no_agreement_check(combined_df)
    calculate_fleiss_kappa(combined_df_parsed)
    # write_agreement_file(combined_df_parsed, "toxicity_agreement")
