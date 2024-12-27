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
        target_language='hien'
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
        if (target_language=='hi'):

            try:
                # Skip empty content
                if self.content.strip():
                    # Define regex patterns for various languages
                    language_patterns = {
                        'ur': r'[\u0600-\u06FF]',  # Urdu (Arabic script)
                        'es': r'[a-zA-Zñáéíóúü¡¿]',  # Spanish (basic Latin characters + specific accents)
                        'fr': r'[a-zA-Zàâçéèêëîïôûùüÿœæ]',  # French (basic Latin + accents)
                        'en': r'[a-zA-Z]',  # English (basic Latin characters)
                        'pt': r'[a-zA-ZáàãâéêíóôõúçÁÀÃÂÉÊÍÓÔÕÚÇ]'
                        # Add more languages as needed here
                    }

                    # Check if the target language has a specific regex pattern
                    if self.target_language in language_patterns:
                        pattern = language_patterns[self.target_language]
                        if not re.search(pattern, self.content):  # If no match for the target language
                            self.error = True
                            return

                    # Additional language detection check using langdetect
                    detected_language = langdetect.detect(self.content)
                    if detected_language != self.target_language:  # Ensure it matches the target language
                        self.error = True
                        return

            except (langdetect.LangDetectException, Exception):
                # If language detection fails, fallback to regex check for the target language
                if self.target_language in language_patterns:
                    pattern = language_patterns[self.target_language]
                    if not re.search(pattern, self.content):  # Skip if no match for the target language
                        self.error = True
                        return


        if (target_language=='en'):
            try:
                # Skip empty content
                if self.content.strip():
                    # Define regex patterns for various languages
                    language_patterns = {
                        'hi': r'[\u0900-\u097F]',  # Hindi (Devanagari script)
                        'ur': r'[\u0600-\u06FF]',  # Urdu (Arabic script)
                        'es': r'[a-zA-Zñáéíóúü¡¿]',  # Spanish (basic Latin characters + specific accents)
                        'fr': r'[a-zA-Zàâçéèêëîïôûùüÿœæ]',  # French (basic Latin + accents)
                        'pt': r'[a-zA-ZáàãâéêíóôõúçÁÀÃÂÉÊÍÓÔÕÚÇ]'
                        # Add more languages as needed here
                    }

                    # Check if the target language has a specific regex pattern
                    if self.target_language in language_patterns:
                        pattern = language_patterns[self.target_language]
                        if not re.search(pattern, self.content):  # If no match for the target language
                            self.error = True
                            return

                    # Additional language detection check using langdetect
                    detected_language = langdetect.detect(self.content)
                    if detected_language != self.target_language:  # Ensure it matches the target language
                        self.error = True
                        return

            except (langdetect.LangDetectException, Exception):
                # If language detection fails, fallback to regex check for the target language
                if self.target_language in language_patterns:
                    pattern = language_patterns[self.target_language]
                    if not re.search(pattern, self.content):  # Skip if no match for the target language
                        self.error = True
                        return



        if target_language == 'hien':  # Hinglish logic
            try:
                # Skip empty content
                if self.content.strip():
                    # Check for any non-English characters using regex
                    # This regex will match any character that is not a letter or space
                    if re.search(r'[^a-zA-Z\s]', self.content):  # If any non-English character is found
                        self.error = True
                        return

                    words_list = re.findall(r'\b\w+\b', self.content.lower())

                    # Hinglish dictionary
                    hinglish_dict = {
                        'a' : [
                            "aaya", "apna", "arre", "arey", "aisa", "aik", "aaiye", "aaye", "aaiyiye", 
                            "aaja", "abhi", "aap", "aapse", "aapko", "aapke", "aata", "ajeeb", "ajib", 
                            "aankhon", "aankhein", "aankh", "aaj", "ajj", "aasmaan", "asman", "aasman", 
                            "aur", "aawashyakta", "awashyakta", "adhik", "aaraam", "aram", "aaram", 
                            "araam", "accha", "acha", "achha", "acchi", "achhi", "achi", "achanak", 
                            "aasaan", "asaan", "asan", "aasan", "aapki", "ab", "adbhut"
                            ],
                        'b': [
                            "bahut", "beta", "bina", "bhai", "bolo", "bolna", "bohot", "baatein", 
                            "bharosa", "buniyaad", "buniyad", "behtar", "behtareen", "bewkoof", 
                            "bewkoofi", "bewakoof", "bewakoofi", "bewajah", "baaton", "baato", 
                            "bhi", "barbaad", "barbad", "baarish", "baarishein", "barish", 
                            "barishein", "barishon", "bhaag", "bhaago", "bhaagna", "badi", "bhim", "bheem", 
                            "badal", "baadal", "badlaav", "badlav", "badla", "behta", "bemisaal", "besharam"
                            "beshumar", "beshumaar"
                            ],
                        'c': [
                            "chal", "chalo", "chand", "chaand", "chandni", "chandi", "chori", 
                            "chhod", "chod", "chodo", "chhodo", "chalte", "chalti", "chalta", "chalna",
                            "chupa", "chhupa"
                            ],
                        'd': [
                            "dekha", "din", "dhoop", "dost", "dil", "dino", "dopahar", "dopaher", 
                            "dhyaan", "dhyan", "dilli", "dafa", "dekhi", "dikhi", "dikhayi", "dikhai", 
                            "dekho", "dekhna", "dastan", "daastan", "daastaan", "darmiyaan", "darr", 
                            "dastak", "diya", "doobe", "doobna", "doob", "dhoop", "dosti", "dikkat", "der"
                            ],
                        'e': ['ek'],
                        'f': ['farz', 'fikr', 'fikar', 'faltu', 'farsh'],
                        'g': [
                            "gaya", "gayi", "gadha", "gaadi", "ghadi", "ghum", "gehra", "gehraiyaan", 
                            "ghaata", "ghoomne", "ghumna", "ghumo", "ghoomo", "ghar", "gumnaam", 
                            "gawar", "gawaar", "gulab", "gulaabi", "gulabi", "gulaab", "gunguna", 
                            "gungunati", "garmi", "galti", "gumnaam"
                        ],
                        'h': [
                            "haan", "han", "hai", "hum", "humein", "hume", "humko", "hoti", "hota", 
                            "hona", "humesha", "humaara", "humara", "humaari", "humari", "humse", 
                            "humne", "haar", "husn", "hua", "hun", "hoon", "h", "hain", "haari", 
                            "hi", "hasna", "has", "hans", "hansi", "hasi", "har", "hari"
                        ],
                        'i': ["ishq", "idhar", "izzat", "ijjat", "ijazat", "ijaazat"],
                        'j': [
                            "jisse", "jawab", "jaise", "jidhar", "jeet", "janwar", "jaanwar", 
                            "janvar", "jaanvar", "jaan", "janam", "jaisa", "judayi", "judaayi", 
                            "judai", "judaai", "jaadu", "jagah", "jaane", "jaana", "jo", "jal", 
                            "jalana", "jalaana", "jab", "jawan", "jawaan", "jaon", "jao", "jaun", 
                            "jispe", "jispar", "jaisi", "jagah", "jodi", "jaake", "jai", "jay"
                            "jaag", "jaga", "jaldi", "jalti", "jag", "jaahir", "jaahil", "janaab", "janab", 
                            "jinke", "jahan", "jahaan"
                        ],
                        'k': [
                            "kabhi", "kaise", "kidhar", "khud", "khayal", "khayalon", "khwab", "khwaab", 
                            "kya", "kyun", "kyu", "kab", "kaash", "kash", "kagaz", "kabhie", "kis", 
                            "kahani", "kahaani", "kissa", "kisse", "khushi", "kinaare", "kinare", 
                            "khaali", "khali", "kahin", "kahi", "kahan", "kaha", "kaho", "khushbu", 
                            "khushboo", "khatam", "kinare", "kinaare", "kasam", "keh", "kehna", 
                            "khidki", "kapde", "kapdon", "ki", "kam", "kaam", "koi", "koyi", "kuch", 
                            "kuchh", "karo", "kar", "karna", "kr", "ka", "khuda"
                        ],
                        'l': [
                            "lagta", "liye", "laaye", "laana", "lelo", "lafzon", "laut", "lega", 
                            "legi", "lena", "lao", "log"
                        ],
                        'm': [
                            "magar", "mai", "main", "matlab", "mujhe", "mujhse", "mohabbat", "mohabat", 
                            "mein", "maze", "mazze", "maje", "mauj", "masti", "mahaul", "maahaul", 
                            "mera", "mere", "merre", "maine", "mene", "meine", "meri", "milan", 
                            "mehek", "mehak", "madhur", "maafi", "maaf", "maan", "mana", "meherbaan", 
                            "meherbaani", "meherbani", "maalum", "malum", "mushkil", "musafir", 
                            "mahila", "mitron", "masoom", "masum", "mausam", "mahadev", "mar", "maar",
                            "marke", "maarke", "maarna", "marna", "museebat", "musibat"
                        ],
                        'n': ["nahi", "nahana", "nahaana", "namak", "na", "naseeb", "nazar", "nazariya", "naam", 
                              "namah", "nazrein"
                              ],
                        'p': [
                            "pati", "patni", "pata", "pawan", "paisa", "paise", "pyar", "pyaar", 
                            "prayas", "puraani", "purani", "pukaare", "pukaar", "pukar", "pukare", 
                            "pakore", "phool", "pehle", "pehli", "pehla", "phir", "prem", "par", 
                            "pe", "parvat", "paani"
                        ],
                        'o': ["om"],
                        'r': [
                            "raat", "raha", "raah", "rehna", "rehne", "rahogi", "rahoge", "ruko", 
                            "rukna", "raasta", "rasta", "rabba", "rehti", "roko", "rona", "ro", 
                            "rakh", "rakhi", "rakhna", "ram"
                        ],
                        's': [
                            "sab", "sabhi", "sapna", "samajh", "shayad", "shakal", "shaam", "sham", 
                            "savera", "shuddh", "sawali", "silsila", "sawal", "sawaal", "suno", 
                            "suna", "soona", "safar", "subah", "subha", "saathi", "sathi", "saath", 
                            "shukr", "shukriya", "shukrana", "shukraana", "shukar", "shakkar", 
                            "saari", "surile", "sureele", "swapna", "sagar", "sajna", "shuru", 
                            "samne", "saamne", "soch", "socha", "sochna", "sakhi", "shayar", 
                            "shaayar", "shayari", "shaayari", "sardi", "se", "sahi", "shree", "shri", "shivaay", 
                            "shivay", "sampurana", "sampurna", "shyam", "shyaam", "socho", "suhana", "suhaana", 
                            "sawaalon", "sabr"
                        ],
                        't': [
                            "thoda", "thodi", "tujhe", "tum", "tumhein", "tumhe", "tumko", "tarah", 
                            "tere", "tera", "terre", "tanhayi", "tanhaayi", "tanhayee", "toofan", 
                            "toofani", "tumhari", "tumhaari", "tumse", "tumhare", "tumhaari", 
                            "teri", "tayyar", "tayyaar", "tayyari", "tayyaari", "tamasha", 
                            "tamaasha", "todo", "todna", "tabhi", "tadap", "tha", "thi", 
                            "tasveer", "tujh", "tujhpe", "tujhko", "tabah"
                        ],
                        'v': ["vaayu", "varna", "vaise", "vo"],
                        'w': ["waqt", "waise", "waisa", "waisi", "warna", "wahi", "wohi", "wo", "wahan", "waha", "wah"],
                        'y': ["yr", "yar", "yaar", "yaraana", "yarana", "yaad", "yaadein", "yaadon", 
                              "yaari", "yaariyan", "yaado", "yeh", "yahi", "yahin", "ya", "yun"
                              ],
                        'z': ["zindagi", "zeher", "zara", "zarra", "zanjeer", "zehnaseeb", "zarurat", "zaroorat", 
                              "zariya", "zyada", "zyaada", "zid", "zidd"
                              ],
                    }

                    # Flatten the dictionary into a single list of Hinglish words
                    hinglish_words = [word for sublist in hinglish_dict.values() for word in sublist]

                    # Count the number of matching Hinglish words in the tweet
                    matching_words = [word for word in words_list if word in hinglish_words]

                    if len(matching_words) < 1:  # Require at least 1 Hinglish words
                        self.error = True
                        return

            except Exception as e:
                self.error = True
                print(f"Error processing Hinglish tweet: {e}")
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