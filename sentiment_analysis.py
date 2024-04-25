import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from comment_parser import CommentParser


class SentimentAndToxicityAnalyzer:

    def __init__(self, file, mode):
        df = pd.read_excel(file, index_col=0)

        # make sure the columns are correctly named, and the ground truth has been established for each row
        if "Comments" not in df.columns:
            print("ERROR: One of the columns must be named 'Comments'")
            return

        if "ground truth" not in df.columns:
            print("ERROR: One of the columns must be named 'ground truth', in small caps.")
            return

        if mode == "sentiment":
            if sorted(df['ground truth'].unique()) != ["neg", "neu", "pos"]:
                print("ERROR: The 'label' column can only contain the values 'neg','neu'','pos' in small caps." +
                      "\nIf 'no agreement' was found you need to resolve this through discussion "
                      "or by bringing in a new labeler.")
                return
        else:
            if sorted(df['ground truth'].unique()) != ["n", "y"]:
                print("ERROR: The 'is_toxic' column can only contain the values 'y' 'n' in small caps." +
                      "\nIf 'no agreement' was found you need to resolve this through discussion "
                      "or by bringing in a new labeler.")
                return

        errors = 0

        for k, v in df.iterrows():
            comment = v["Comments"]
            ground_truth = v["ground truth"]
            translated_comment = CommentParser.translate_comment(comment).text
            cleaned_comment = CommentParser.clean_comment(translated_comment, ["hi"])
            if cleaned_comment is None:
                if mode == "toxicity":
                    label = "n"
                else:
                    label = "neu"
            else:
                if mode == "toxicity":
                    label = CommentParser.comment_toxicity(translated_comment)
                    # if label == "y":
                    #     print(CommentParser.full_comment_toxicity(translated_comment))
                    #     print(comment)
                else:
                    label = CommentParser.comment_sentiment(cleaned_comment).output.lower()
            df.loc[k, "prediction"] = label

            if label != ground_truth:
                errors += 1

        # accuracy score
        accuracy = 100 - (errors * 100 / len(df))
        print(f"The accuracy score is {accuracy}")

        # sklearn treats the labels as numbers, but we still need to access the original names
        # so we create a copy here for the confusion matrix, and create a new LabelEncoder object
        df2 = df.copy()
        le = LabelEncoder()
        df2['ground truth'] = le.fit_transform(df2['ground truth'])
        df2['prediction'] = le.transform(df2['prediction'])

        # Compute the confusion matrix and convert into a dataframe for the plot
        cm = confusion_matrix(df2['ground truth'], df2['prediction'])
        self.cm_df = pd.DataFrame(cm, index=le.classes_, columns=le.classes_)
        self.df = df

    def confusion_matrix(self):
        """plots the confusion matrix using seaborn"""
        plt.figure(figsize=(7, 5))
        print(self.cm_df)
        sns.heatmap(self.cm_df, annot=True, cmap='PuBuGn')
        plt.title('Confusion Matrix')
        plt.ylabel('Actual label')
        plt.xlabel('Predicted label')
        plt.show()

    def examine_labels(self, actual, predicted):
        """examines the labels give an actual/predicted pair; prints the number of matches
        and returns the matches as a df"""
        pd.set_option('display.max_colwidth', None)
        df = self.df
        results = df[(df['ground truth'] == actual) & (df['prediction'] == predicted)]
        print(len(results))
        return results


def sentiment_analysis(file, mode):
    """give a file_location (an agreement.xlsx file), returns an Analyzer object"""
    return SentimentAndToxicityAnalyzer(file, mode)


if __name__ == "__main__":
    analyzer = sentiment_analysis("./manual_coding/toxicity_agreement_confirmed.xlsx", "toxicity")
    analyzer.confusion_matrix()
