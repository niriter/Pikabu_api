from classes.Post import Post
from parsers.Comment import Parse_Comment

class Parse_Post():
    def __init__(self, from_feed=False, debug=False):
        self.debug = debug
        self.from_feed = from_feed
        self.main_url = 'https://pikabu.ru'
        self.post = Post()

    def parse(self, soup):
        self.post.set_title(self._clean_text(soup.findAll("header", {"class": "story__header"})[0].text))
        self.post.set_rating(soup.findAll("div", {"class": "story__rating-count"})[0].text)
        self.post.set_user_url(self.main_url + soup.findAll("a", {"class": "user__nick"})[0]['href'])
        self.post.set_datetime(soup.findAll("time", {"class": "story__datetime"})[0]['datetime'])
        self.post.set_url(soup.findAll("a", {"class": "story__comments-link"})[0]['href'].split("#")[0])

        if soup.findAll("div", {"class": "story__content-inner"}):
            self.post.set_content(self._clean_text(soup.findAll("div", {"class": "story__content-inner"})[0].text))
            self.post.set_content_html(soup.findAll("div", {"class": "story__content-inner"})[0].prettify())
            if soup.findAll("div", {"class": "story__content-inner"})[0].findAll("img"):
                for img in soup.findAll("div", {"class": "story__content-inner"})[0].findAll("img"):
                    self.post.add_media(img['data-large-image'])
            if soup.findAll("div", {"class": "story__content-inner"})[0].findAll("a"):
                for img in soup.findAll("div", {"class": "story__content-inner"})[0].findAll("a"):
                    if img['href'].split('.')[-1] != 'png':
                        self.post.add_link(img['href'])
            if soup.findAll("div", {"class": "story-block"}):
                for block in soup.findAll("div", {"class": "story-block"}):
                    if block.findAll('img'):
                        self.post.add_content_block(block.findAll('img')[0]['data-large-image'])
                    else:
                        self.post.add_content_block(self._clean_text(block.text))

        for tag in soup.findAll("div", {"class": "story__tags"})[0].findChildren():
            self.post.add_tag({'name': tag.text, 'url': self.main_url + tag['href']})

        if not self.from_feed:
            self.post.set_pluses(soup.findAll("div", {"class": "page-story__rating"})[0]['data-pluses'])
            self.post.set_minuses(soup.findAll("div", {"class": "page-story__rating"})[0]['data-minuses'])
            self.post.set_post_id(soup.findAll("section", {"class": "comments_show"})[0]['data-story-id'])
            self.post.set_username(soup.findAll("section", {"class": "comments_show"})[0]['data-story-username'])
            self.post.set_comments_count(soup.findAll("section", {"class": "comments_show"})[0]['data-total'])
            self.post.set_save(soup.findAll("span", {"class": "story__save-count"})[0].text)
            self.post.set_share(soup.findAll("span", {"class": "story__share-count"})[0].text)
            parent_comment = Parse_Comment()
            self.post.set_comments(parent_comment.parse(soup))
        else:
            self.post.set_post_id(soup.findAll("div", {"class": "story__rating-block"})[0]['data-story-id'])
            self.post.set_username(soup.findAll("a", {"class": "user__nick"})[0].text)
            self.post.set_comments_count(soup.findAll("span", {"class": "story__comments-link-count"})[0].text)
        if self.debug:
            self.post.print_values()
        return self.post

    def _clean_text(self, text):
        clean_words = ['\n', '\r', '\t']
        for clean_word in clean_words:
            text = text.replace(clean_word, '')
        return text
