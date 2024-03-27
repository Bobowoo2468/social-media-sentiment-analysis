from googleapiclient.discovery import build
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
DEVELOPER_KEY = os.environ['YT_DEVELOPER_KEY']
comments = []


def video_comments(video_id):
    youtube = build('youtube', 'v3',
                    developerKey=DEVELOPER_KEY)

    # retrieve youtube video results
    video_response = youtube.commentThreads().list(
        part='snippet,replies',
        videoId=video_id
    ).execute()

    while video_response:
        for item in video_response['items']:

            # Extracting comments
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']

            # counting number of reply of comment
            reply_count = item['snippet']['totalReplyCount']

            if reply_count > 0:
                for reply in item['replies']['comments']:
                    reply = reply['snippet']['textDisplay']
                    comments.append(reply)

            comments.append(comment)

        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                pageToken=video_response['nextPageToken']
            ).execute()
        else:
            break


if __name__ == "__main__":
    VIDEO_ID = "ehSr-HIKVMw"

    # video_comments(VIDEO_ID)
    # df_comments = pd.DataFrame(comments)
    # df_comments.to_csv('comments.csv')
