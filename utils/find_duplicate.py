import pandas as pd

FILE_NAME = 'test.csv'
df = pd.read_csv('test.csv')
duplicated_comments = []
duplicated_comments_indexes = []

for index, is_duplicated in enumerate(df.Comments.duplicated()):
    if is_duplicated:
        duplicated_comments_indexes.append(index)
        print(index)
        duplicated_comments.append(df.Comments[index])
        print(df.Comments[index])
