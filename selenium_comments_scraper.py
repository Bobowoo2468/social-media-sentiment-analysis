import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import pandas as pd

comments = []

# enable the headless mode
options = Options()
options.add_argument("--headless=new")


def scrape(youtube_video_url):
    with Chrome(options=options) as driver:
        wait = WebDriverWait(driver, 15)
        driver.get(youtube_video_url)
        driver.maximize_window()

        # wait for YouTube to load the page data
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.ytd-watch-metadata'))
        )

        # wait = WebDriverWait(driver, 30)

        video = {}
        channel = {}

        # title = driver \
        #     .find_element(By.CSS_SELECTOR, 'h1.style-scope.ytd-watch-metadata') \
        #     .text
        #
        # # scrape the channel info attributes
        # channel_element = driver \
        #     .find_element(By.ID, 'owner')
        # channel_url = channel_element \
        #     .find_element(By.CSS_SELECTOR, 'a.yt-simple-endpoint') \
        #     .get_attribute('href')
        # channel_name = channel_element \
        #     .find_element(By.ID, 'channel-name') \
        #     .text
        # channel_image = channel_element \
        #     .find_element(By.ID, 'img') \
        #     .get_attribute('src')
        # channel_subs = channel_element \
        #     .find_element(By.ID, 'owner-sub-count') \
        #     .text \
        #     .replace(' subscribers', '')
        #
        # channel["channel_url"] = channel_url
        # channel["channel_name"] = channel_name
        # channel["channel_subs"] = channel_subs
        #
        # # click the description section to expand it
        # driver.find_element(By.ID, 'description-inline-expander').click()
        #
        # info_container_elements = driver \
        #     .find_elements(By.CSS_SELECTOR, '#info-container span')
        #
        # views = info_container_elements[0] \
        #     .text \
        #     .replace(' views', '')
        #
        # publication_date = info_container_elements[2] \
        #     .text
        #
        # description = driver \
        #     .find_element(By.CSS_SELECTOR, '#description-inline-expander .ytd-text-inline-expander span') \
        #     .text
        #
        # likes = driver \
        #     .find_elements(By.CSS_SELECTOR, '.yt-spec-button-shape-next__button-text-content')[4]\
        #     .text
        #
        #
        # video['url'] = youtube_video_url
        # video['title'] = title
        # video['channel'] = channel
        # video['views'] = views
        # video['publication_date'] = publication_date
        # video['description'] = description
        # video['likes'] = likes
        #
        # for key, value in video.items():
        #     print(key, value)
        #
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='more-replies']"))
        )
        more_replies = driver.find_elements(By.XPATH, "//*[@id='more-replies']")
        print(len(more_replies))

        for more_reply in more_replies:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(more_reply)).click()

        # Scroll all the way down to the bottom in order to get all the
        # elements loaded (since Youtube dynamically loads them).
        last_height = driver.execute_script("return document.documentElement.scrollHeight")

        while True:
            # Scroll down until "next load"
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

            # Wait to load everything thus far.
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                print("No more comments required to render!")
                break
            last_height = new_height

        # reply_elements = driver.find_elements(By.CSS_SELECTOR, 'button[class*="yt-spec-button-shape-next"]')
        # reply_elements = driver.find_elements(By.ID, 'more-replies')

        # elem = (By.XPATH, "//*[@class='more-button' and @id='more-replies']")


        try:
            # Extract the element that refers to the comments
            comment_section = driver.find_elements(By.XPATH, '//*[@id="comments"]')

        except exceptions.NoSuchElementException:
            # in case Youtube changes their HTML layouts
            error = "Element not found: HTML layout changed"
            print(error)

        try:
            comment_html_elements = driver.find_elements(By.XPATH, '//*[@id="content-text"]')
            is_looped = False

            while True:
                # Extract the elements storing the usernames and comments
                username_html_elements = driver.find_elements(By.XPATH, '//*[@id="author-text"]')
                comment_html_elements = driver.find_elements(By.XPATH, '//*[@id="content-text"]')

                for comment_index, comment_element in enumerate(comment_html_elements):
                    if comment_index == 0 and is_looped:
                        return comments

                    if comment_index == 0:
                        is_looped = True

                    comment_text = comment_element.text
                    print(comment_text)
                    comments.append(comment_text)

        except exceptions.NoSuchElementException:
            # in case Youtube changes their HTML layouts
            error = "Element not found: HTML layout changed"
            print(error)


if __name__ == "__main__":
    YOUTUBE_URL = "https://www.youtube.com/watch?v=ehSr-HIKVMw"
    comments = scrape(YOUTUBE_URL)
    print("Number of comments: ", len(comments))
    df_comments = pd.DataFrame(comments)
    df_comments.to_csv('comments_selenium.csv', index=False)
