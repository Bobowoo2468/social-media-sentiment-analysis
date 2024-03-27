from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
DEVELOPER_KEY = os.environ['YT_DEVELOPER_KEY']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def get_playlist_video_ids(service, **kwargs):
    video_ids = []
    results = service.playlistItems().list(**kwargs).execute()
    while results:
        for item in results['items']:
            video_ids.append(item['snippet']['resourceId']['videoId'])
            print(item['snippet']['resourceId']['videoId'])

        # # check if there are more videos
        # if 'nextPageToken' in results:
        #     kwargs['pageToken'] = results['nextPageToken']
        #     results = service.playlistItems().list(**kwargs).execute()
        # else:
        #     break

    return video_ids


def get_video_comments(service, **kwargs):
    comments, dates, likes, video_titles = [], [], [], []
    results = service.commentThreads().list(**kwargs).execute()

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            date = item['snippet']['topLevelComment']['snippet']['publishedAt']
            like = item['snippet']['topLevelComment']['snippet']['likeCount']
            video_title = service.videos().list(part='snippet', id=kwargs['videoId']).execute()['items'][0]['snippet'][
                'title']

            comments.append(comment)
            dates.append(date)
            likes.append(like)
            video_titles.append(video_title)

        # check if there are more comments
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break

    return pd.DataFrame({'Video Title': video_titles, 'Comments': comments, 'Date': dates, 'Likes': likes})


def main():
    # build the service
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # get playlist video ids
    playlist_id = 'PLJ-qODNIUEEtPdKZNLfbx7JOuRA_JjUxI'
    video_ids = get_playlist_video_ids(youtube, part='snippet', maxResults=50, playlistId=playlist_id)

    # get the comments from each video
    all_comments_df = pd.DataFrame()

    # for video_id in video_ids:
    #     try:
    #         comments_df = get_video_comments(youtube, part='snippet', videoId=video_id, textFormat='plainText')
    #         all_comments_df = pd.concat([all_comments_df, comments_df], ignore_index=True)
    #     except HttpError as e:
    #         print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")

    return all_comments_df  # return the DataFrame


if __name__ == '__main__':
    df = main()
    print(df)  # print the DataFrame here
