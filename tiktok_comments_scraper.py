from TikTokApi import TikTokApi
import asyncio
import os
import pandas as pd
from dotenv import load_dotenv
from cleantext import clean

load_dotenv()
ms_token = os.environ.get("MS_TOKEN", None)


class TikTokCommentScraper:

    def __init__(self, creators, data_dir, output_dir):
        for creator in creators:
            url_file_name = f"./{data_dir}/tiktok_{creator}.txt"
            url_file = open(url_file_name, "r")

            video_ids, total_num_comments = self.reinitialise()

            for video_id in url_file.readlines():
                video_ids.append(video_id.strip())

            for video_id in video_ids:
                video_comments, empty_comment_count = asyncio.run(self.get_comments(video_id))
                print(f"Number of comments scraped: {len(video_comments)}")
                print(f"Number of empty comments: {empty_comment_count}")
                csv_file_name = f'./{output_dir}/tiktok_{creator}.csv'
                df_comments = pd.DataFrame(video_comments)
                df_comments.to_csv(csv_file_name, mode='a', index=True)
                print(f"Comments scraped can be found as {csv_file_name}")

    def parse_comment(self, comment):
        parsed_comment = clean(comment, no_emoji=True)
        return parsed_comment

    def reinitialise(self):
        return [], 0

    async def get_comments(self, video_id):
        video_comments = []
        empty_comment_count = 0
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
            video = api.video(id=video_id)
            async for comment in video.comments(count=200):
                parsed_comment = self.parse_comment(comment.text)
                if len(parsed_comment.strip()) != 0:
                    video_comments.append(self.parse_comment(comment.text))
                else:
                    empty_comment_count += 1
        return video_comments, empty_comment_count


def scrape_tiktok(creators, data_dir, output_dir):
    return TikTokCommentScraper(creators, data_dir, output_dir)


if __name__ == "__main__":
    CREATOR_NAMES = ["itsclarityco", "thebackstagebunch", "welloshow"]
    scrape_tiktok(CREATOR_NAMES, "data", "test")
