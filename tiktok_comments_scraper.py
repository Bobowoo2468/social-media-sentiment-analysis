from TikTokApi import TikTokApi
import asyncio
import os
import pandas as pd
from dotenv import load_dotenv
from cleantext import clean

load_dotenv()
ms_token = os.environ.get("MS_TOKEN", None)
SPLICE_START = 22
SPLICE_END = -1


async def get_comments(video_id):
    video_comments = []
    empty_comment_count = 0
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
        video = api.video(id=video_id)
        async for comment in video.comments(count=200):
            # print(parse_comment(comment.text))
            parsed_comment = parse_comment(comment.text)
            if len(parsed_comment.strip()) != 0:
                video_comments.append(parse_comment(comment.text))
            else:
                empty_comment_count += 1
    return video_comments, empty_comment_count


def reinitialise():
    return [], 0


# 1 - Normalising text
# 2 - Remove Unicode Characters i.e. Emojis
# 3 - Remove Stopwords

def parse_comment(comment):
    parsed_comment = clean(comment, no_emoji=True)
    return parsed_comment


if __name__ == "__main__":
    CREATOR_NAMES = ["itsclarityco", "thebackstagebunch", "welloshow"]

    for creator in CREATOR_NAMES:
        url_file_name = "./data/tiktok_" + creator + ".txt"
        url_file = open(url_file_name, "r")

        video_ids, total_num_comments = reinitialise()

        for video_id in url_file.readlines():
            video_ids.append(video_id.strip())
            # try:
            #     video_id = video_id.strip().split("video/")[1]
            #     video_ids.append(video_id)
            # except IndexError:
            #     print("Parsing video id error")

        for video_id in video_ids:
            video_comments, empty_comment_count = asyncio.run(get_comments(video_id))
            print("Number of empty comments: ", empty_comment_count)
            csv_file_name = './comments/tiktok_' + creator + '.csv'
            df_comments = pd.DataFrame(video_comments)
            df_comments.to_csv(csv_file_name, mode='a', index=True)
