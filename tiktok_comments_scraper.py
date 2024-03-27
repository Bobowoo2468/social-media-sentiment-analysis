from TikTokApi import TikTokApi
import asyncio
import os
from dotenv import load_dotenv

video_id = 7319905964587584801
load_dotenv()
ms_token = os.environ.get("MS_TOKEN", None)


async def get_comments():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
        video = api.video(id=video_id)
        count = 0
        async for comment in video.comments(count=100):
            print(comment.text)
            # print(comment.as_dict)


if __name__ == "__main__":
    asyncio.run(get_comments())
