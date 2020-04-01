class Comment:
    def __init__(self):
        self.author_name = ''
        self.author_url = ''
        self.datetime = ''
        self.link = ''
        self.rating = ''
        self.formatted_text = ''
        self.pluses = 0
        self.minuses = 0
        self.subcomments = []
        self.comment_level = 0

    def get_author_name(self):
        return self.author_name

    def get_author_url(self):
        return self.author_url

    def get_datetime(self):
        return self.datetime

    def get_link(self):
        return self.link

    def get_rating(self):
        return self.rating

    def get_formatted_text(self):
        return self.formatted_text

    def get_pluses(self):
        return self.pluses

    def get_minuses(self):
        return self.minuses

    def get_subcomments(self):
        return self.subcomments

    def get_comment_level(self):
        return self.comment_level

    def author_name(self):
        return self.get_author_name()

    def author_url(self):
        return self.get_author_url()

    def datetime(self):
        return self.get_datetime()

    def link(self):
        return self.get_link()

    def rating(self):
        return self.get_rating()

    def formatted_text(self):
        return self.get_formatted_text()

    def pluses(self):
        return self.get_pluses()

    def minuses(self):
        return self.get_minuses()

    def subcomments(self):
        return self.get_subcomments()

    def comment_level(self):
        return self.get_comment_level()

    def set_author_name(self, author_name):
        self.author_name = author_name
        return True

    def set_author_url(self, author_url):
        self.author_url = author_url
        return True

    def set_datetime(self, datetime):
        self.datetime = datetime
        return True

    def set_link(self, link):
        self.link = link
        return True

    def set_rating(self, rating):
        self.rating = rating
        return True

    def set_formatted_text(self, formatted_text):
        self.formatted_text = formatted_text
        return True

    def set_pluses(self, pluses):
        self.pluses = pluses
        return True

    def set_minuses(self, minuses):
        self.minuses = minuses
        return True

    def set_subcomments(self, subcomments):
        self.subcomments = subcomments
        return True

    def set_comment_level(self, comment_level):
        self.comment_level = comment_level
        return True

    def append_subcomment(self, comment):
        self.subcomments.append(comment)
        return True

    def add_subcomment(self, comment):
        return self.append_subcomment(comment)