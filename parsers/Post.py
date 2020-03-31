from ..classes.Post import Post
import pickle
import requests

class Parse_Post():
    def __init__(self, from_feed=False):
        self.from_feed = from_feed

    def parse(self, soup):
        post = Post()
        post.set_title(soup.findAll("header", {"class": "story__header"})[0].text)
        if soup.findAll("div", {"class": "story__content-inner"}):
            post.set_content(self._clean_text(soup.findAll("div", {"class": "story__content-inner"})[0].text))
            post.set_content_html(soup.findAll("div", {"class": "story__content-inner"})[0].prettify())
            if soup.findAll("div", {"class": "story__content-inner"})[0].findAll("img"):
                for img in soup.findAll("div", {"class": "story__content-inner"})[0].findAll("img"):
                    post.add_media(img['data-large-image'])
            if soup.findAll("div", {"class": "story__content-inner"})[0].findAll("a"):
                for img in soup.findAll("div", {"class": "story__content-inner"})[0].findAll("a"):
                    if img['href'].split('.')[-1] != 'png':
                        post.add_link(img['href'])
            if soup.findAll("div", {"class": "story-block"}):
                for block in soup.findAll("div", {"class": "story-block"}):
                    if block.findAll('img'):
                        post.add_content_block(block.findAll('img')[0]['data-large-image'])
                    else:
                        post.add_content_block(self._clean_text(block.text))
        post.set_rating(soup.findAll("div", {"class": "story__rating-count"})[0].text)
        if not self.from_feed:
            post.set_pluses(soup.findAll("div", {"class": "page-story__rating"})[0]['data-pluses'])
            post.set_minuses(soup.findAll("div", {"class": "page-story__rating"})[0]['data-minuses'])
            post.set_post_id(soup.findAll("section", {"class": "comments_show"})[0]['data-story-id'])
            post.set_username(soup.findAll("section", {"class": "comments_show"})[0]['data-story-username'])
            post.set_comments_count(soup.findAll("section", {"class": "comments_show"})[0]['data-total'])
            post.set_save(soup.findAll("span", {"class": "story__save-count"})[0].text)
            post.set_share(soup.findAll("span", {"class": "story__share-count"})[0].text)
        else:
            post.set_post_id(soup.findAll("div", {"class": "story__rating-block"})[0]['data-story-id'])
            post.set_username(soup.findAll("a", {"class": "user__nick"})[0].text)
            post.set_comments_count(soup.findAll("span", {"class": "story__comments-link-count"})[0].text)
        post.set_user_url("https://pikabu.ru" + soup.findAll("a", {"class": "user__nick"})[0]['href'])
        post.set_datetime(soup.findAll("time", {"class": "story__datetime"})[0]['datetime'])
        post.set_url(soup.findAll("a", {"class": "story__comments-link"})[0]['href'].split("#")[0])
        for tag in soup.findAll("div", {"class": "story__tags"})[0].findChildren():
            post.add_tag({'name': tag.text, 'url': 'https://pikabu.ru' + tag['href']})
        if not self.from_feed:
            post.set_comments(self._get_comments(soup))
        return post

    def _clean_text(self, text):
        clean_words = ['\n', '\r', '\t']
        for clean_word in clean_words:
            text = text.replace(clean_word, '')
        return text

    def _get_comments(self, soup, indent=0):
        comments = []
        for comment in soup.findAll("div", {"class": "comment", "data-indent": indent}):
            tmp_comment = {}
            tmp_comment['author_name'] = comment.findAll("div", {"class": "comment__user"})[0]['data-name']
            tmp_comment['author_url'] = 'https://pikabu.ru' + comment.findAll("a", {"class": "user"})[0]['href']
            tmp_comment['datetime'] = comment.findAll("time", {"class": "comment__datetime"})[0]['datetime']
            tmp_comment['link'] = comment.findAll("a", {"class": "comment__tool", "data-role": "link"})[0]['href']
            tmp_comment['rating'] = comment.findAll("div", {"class": "comment__rating-count"})[0].text
            tmp_comment['formatted_text'] = self._clean_content(
                comment.findAll("div", {"class": "comment__content"})[0].text)
            tmp = comment.findAll("div", {"class": "comment__rating-count"})[0]['aria-label']
            tmp_comment['pluses'] = [int(s) for s in tmp.split() if s.isdigit()][0]
            tmp_comment['minuses'] = [int(s) for s in tmp.split() if s.isdigit()][1]
            tmp_comment['subcomments'] = self._get_comments(comment.findAll("div", {"class": "comment__children"})[0], indent + 1) if self._has_subcomments(comment) else []
            comments.append(tmp_comment)
            del tmp_comment
        return comments

    def _has_subcomments(self, soup):
        return True if soup.findAll("div", {"class": "comment__children"}) else False