from classes.Comment import Comment

class Parse_Comment:
    def __init__(self):
        self.main_url = 'https://pikabu.ru'

    def parse(self, soup, indent=0):
        comments = []
        for comment_obj in soup.findAll("div", {"class": "comment", "data-indent": indent}):
            comment = Comment()
            comment.set_author_name(comment_obj.findAll("div", {"class": "comment__user"})[0]['data-name'])
            comment.set_author_url(self.main_url + comment_obj.findAll("a", {"class": "user"})[0]['href'])
            comment.set_datetime(comment_obj.findAll("time", {"class": "comment__datetime"})[0]['datetime'])
            comment.set_link(comment_obj.findAll("a", {"class": "comment__tool", "data-role": "link"})[0]['href'])
            comment.set_rating(comment_obj.findAll("div", {"class": "comment__rating-count"})[0].text)
            comment.set_formatted_text(self._clean_text(comment_obj.findAll("div", {"class": "comment__content"})[0].text))
            comment.set_pluses([int(s) for s in comment_obj.findAll("div", {"class": "comment__rating-count"})[0]['aria-label'].split() if s.isdigit()][0])
            comment.set_minuses([int(s) for s in comment_obj.findAll("div", {"class": "comment__rating-count"})[0]['aria-label'].split() if s.isdigit()][1])
            comment.set_subcomments(self.parse(comment_obj.findAll("div", {"class": "comment__children"})[0], indent + 1) if self._has_subcomments(comment_obj) else [])
            comment.set_comment_level(indent)
            comments.append(comment)
        return comments

    def _has_subcomments(self, soup):
        return True if soup.findAll("div", {"class": "comment__children"}) else False

    def _clean_text(self, text):
        clean_words = ['\n', '\r', '\t']
        for clean_word in clean_words:
            text = text.replace(clean_word, '')
        return text
