from time import sleep
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import langdetect
import re

class Tweet:
    def __init__(
        self,
        card: WebDriver,
        driver: WebDriver,
        actions: ActionChains,
        scrape_poster_details=False,
        target_language='hi'
    ) -> None:
        self.card = card
        self.error = False
        self.tweet = None
        self.target_language = target_language

        try:
            self.user = card.find_element(
                "xpath", './/div[@data-testid="User-Name"]//span'
            ).text
        except NoSuchElementException:
            self.error = True
            self.user = "skip"

        try:
            self.handle = card.find_element(
                "xpath", './/span[contains(text(), "@")]'
            ).text
        except NoSuchElementException:
            self.error = True
            self.handle = "skip"

        try:
            self.date_time = card.find_element("xpath", ".//time").get_attribute(
                "datetime"
            )

            if self.date_time is not None:
                self.is_ad = False
        except NoSuchElementException:
            self.is_ad = True
            self.error = True
            self.date_time = "skip"

        if self.error:
            return

        try:
            card.find_element(
                "xpath", './/*[local-name()="svg" and @data-testid="icon-verified"]'
            )

            self.verified = True
        except NoSuchElementException:
            self.verified = False

        # First check for emojis
        try:
            raw_emojis = card.find_elements(
                "xpath",
                '(.//div[@data-testid="tweetText"])[1]/img[contains(@src, "emoji")]',
            )

            self.emojis = [
                emoji.get_attribute("alt").encode("unicode-escape").decode("ASCII")
                for emoji in raw_emojis
            ]
            
            # If no emojis found, mark as error and return
            if not self.emojis:
                self.error = True
                return
                
        except NoSuchElementException:
            self.error = True
            self.emojis = []
            return

        self.content = ""
        contents = card.find_elements(
            "xpath",
            '(.//div[@data-testid="tweetText"])[1]/span | (.//div[@data-testid="tweetText"])[1]/a',
        )

        for index, content in enumerate(contents):
            self.content += content.text

        # Check for English characters and language detection
        try:
            # Skip empty content
            if self.content.strip():
                # Check for English characters using regex
                if re.search('[a-zA-Z]', self.content):
                    self.error = True
                    return
                
                # Additional language detection check
                detected_language = langdetect.detect(self.content)
                if detected_language != self.target_language:
                    self.error = True
                    return
        except (langdetect.LangDetectException, Exception):
            # If language detection fails, we'll still keep checking for English characters
            if re.search('[a-zA-Z]', self.content):
                self.error = True
                return

        try:
            self.reply_cnt = card.find_element(
                "xpath", './/button[@data-testid="reply"]//span'
            ).text

            if self.reply_cnt == "":
                self.reply_cnt = "0"
        except NoSuchElementException:
            self.reply_cnt = "0"

        try:
            self.retweet_cnt = card.find_element(
                "xpath", './/button[@data-testid="retweet"]//span'
            ).text

            if self.retweet_cnt == "":
                self.retweet_cnt = "0"
        except NoSuchElementException:
            self.retweet_cnt = "0"

        try:
            self.like_cnt = card.find_element(
                "xpath", './/button[@data-testid="like"]//span'
            ).text

            if self.like_cnt == "":
                self.like_cnt = "0"
        except NoSuchElementException:
            self.like_cnt = "0"

        try:
            self.analytics_cnt = card.find_element(
                "xpath", './/a[contains(@href, "/analytics")]//span'
            ).text

            if self.analytics_cnt == "":
                self.analytics_cnt = "0"
        except NoSuchElementException:
            self.analytics_cnt = "0"

        try:
            self.tags = card.find_elements(
                "xpath",
                './/a[contains(@href, "src=hashtag_click")]',
            )

            self.tags = [tag.text for tag in self.tags]
        except NoSuchElementException:
            self.tags = []

        try:
            self.mentions = card.find_elements(
                "xpath",
                '(.//div[@data-testid="tweetText"])[1]//a[contains(text(), "@")]',
            )

            self.mentions = [mention.text for mention in self.mentions]
        except NoSuchElementException:
            self.mentions = []

        try:
            self.profile_img = card.find_element(
                "xpath", './/div[@data-testid="Tweet-User-Avatar"]//img'
            ).get_attribute("src")
        except NoSuchElementException:
            self.profile_img = ""

        try:
            self.tweet_link = self.card.find_element(
                "xpath",
                ".//a[contains(@href, '/status/')]",
            ).get_attribute("href")
            self.tweet_id = str(self.tweet_link.split("/")[-1])
        except NoSuchElementException:
            self.tweet_link = ""
            self.tweet_id = ""

        self.following_cnt = "0"
        self.followers_cnt = "0"
        self.user_id = None

        self.tweet = (
            self.user,
            self.handle,
            self.date_time,
            self.verified,
            self.content,
            self.reply_cnt,
            self.retweet_cnt,
            self.like_cnt,
            self.analytics_cnt,
            self.tags,
            self.mentions,
            self.emojis,
            self.profile_img,
            self.tweet_link,
            self.tweet_id,
            self.user_id,
            self.following_cnt,
            self.followers_cnt,
        )