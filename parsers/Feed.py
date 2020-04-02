from bs4 import BeautifulSoup
from classes.Feed import Feed
from datetime import datetime
import logging
from parsers.Post import Parse_Post
from pprint import pprint
import json

class Parse_Feed:
    def __init__(self, url='', posts_count=13):
        self.feed = Feed()
        self.feed.set_url(url)
        self.feed.set_posts_count(posts_count)
        self.logger = logging.getLogger("Pikabu-api.parsers.Feed")

    def parse_feed_info(self, soup):
        if soup.findAll("h2", {"class": "thematic-header__heading"}):
            self.feed.set_name(soup.findAll("h2", {"class": "thematic-header__heading"})[0].text)
        else:
            self.feed.set_name(soup.findAll("title")[0].text.split("|")[0].strip())
        self.feed.set_date(str(datetime.now().strftime("%Y-%m-%d")).replace('-', '/'))
        if soup.findAll("p", {"class": "thematic-header__content"}):
            self.feed.set_has_about(True)
            self.feed.set_about(soup.findAll("p", {"class": "thematic-header__content"})[0].text)
        return

    def parse(self):
        return

    def parse_from_json(self, content):
        content = json.loads(self._clean_content(content))
        for post in content['data']['stories']:
            if len(self.feed.get_posts()) == self.feed.posts_count:
                return True
            wrapper = Parse_Post(True)
            self.feed.add_post(wrapper.parse(BeautifulSoup(post['html'], 'html.parser')))
        return True

    def get_feed(self):
        return self.feed

    def _clean_content(self, content):
        clean_words = ['\n', '\r', '\t']
        for clean_word in clean_words:
            content = content.replace(clean_word, '')
        return content
