class Post:
    def __init__(self):
        self.title = ''
        self.content = ''
        self.content_html = ''
        self.content_blocks = []
        self.media = []
        self.links = []
        self.rating = ''
        self.pluses = 0
        self.minuses = 0
        self.post_id = 0
        self.username = ''
        self.user_url = ''
        self.comments_count = 0
        self.saves = 0
        self.shares = 0
        self.datetime = ''
        self.url = ''
        self.tags = []
        self.comments = []

    # Start functions to get object data

    def get_title(self):
        return self.title

    def get_content(self):
        return self.content

    def get_content_html(self):
        return self.content_html

    def get_content_blocks(self):
        return self.content_blocks

    def get_media(self):
        return self.media

    def get_links(self):
        return self.links

    def get_rating(self):
        return self.rating

    def get_pluses(self):
        return self.pluses

    def get_minuses(self):
        return self.minuses

    def get_post_id(self):
        return self.post_id

    def get_username(self):
        return self.username

    def get_user_url(self):
        return self.user_url

    def get_comments_count(self):
        return self.comments_count

    def get_saves(self):
        return self.saves

    def get_shares(self):
        return self.shares

    def get_datetime(self):
        return self.datetime

    def get_url(self):
        return self.url

    def get_tags(self):
        return self.tags

    def get_comments(self):
        return self.comments

    def title(self):
        return self.get_title()

    def content(self):
        return self.get_content()

    def content_html(self):
        return self.get_content_html()

    def content_blocks(self):
        return self.get_content_blocks()

    def media(self):
        return self.get_media()

    def links(self):
        return self.get_media()

    def rating(self):
        return self.get_rating()

    def pluses(self):
        return self.get_pluses()

    def minuses(self):
        return self.get_minuses()

    def post_id(self):
        return self.get_post_id()

    def username(self):
        return self.get_username()

    def user_url(self):
        return self.get_user_url()

    def comments_count(self):
        return self.get_comments_count()

    def saves(self):
        return self.get_saves()

    def shares(self):
        return self.get_shares()

    def datetime(self):
        return self.get_datetime()

    def url(self):
        return self.get_url()

    def tags(self):
        return self.get_tags()

    def comments(self):
        return self.get_comments()

    #End functions to get object data

    #Start functions to set object data

    def set_title(self, title):
        self.title = title
        return True

    def set_content(self, content):
        self.content = content
        return True

    def set_content_html(self, content_html):
        self.content_html = content_html
        return True

    def set_content_blocks(self, content_blocks):
        self.content_blocks = content_blocks
        return True

    def set_media(self, media):
        self.media = media
        return True

    def set_links(self, links):
        self.links = links
        return True

    def set_rating(self, rating):
        self.rating = rating
        return True

    def set_pluses(self, pluses):
        self.pluses = pluses
        return True

    def set_minuses(self, minuses):
        self.minuses = minuses
        return True

    def set_post_id(self, post_id):
        self.post_id = post_id
        return True

    def set_username(self, username):
        self.username = username
        return True

    def set_user_url(self, user_url):
        self.user_url = user_url
        return True

    def set_comments_count(self, comments_count):
        self.comments_count = comments_count
        return True

    def set_saves(self, saves):
        self.saves = saves
        return True

    def set_shares(self, shares):
        self.shares = shares
        return True

    def set_datetime(self, datetime):
        self.datetime = datetime
        return True

    def set_url(self, url):
        self.url = url
        return True

    def set_tags(self, tags):
        self.tags = tags
        return True

    def set_comments(self, comments):
        self.comments = comments
        return True

    def append_content_block(self, content_block):
        self.content_blocks.append(content_block)
        return True

    def append_media(self, media):
        self.media.append(media)
        return True

    def append_link(self, link):
        self.links.append(link)
        return True

    def append_tag(self, tag):
        self.tags.append(tag)
        return True

    def append_comment(self, comment):
        self.comments.append(comment)
        return True

    def add_content_block(self, content_block):
        return self.append_content_block(content_block)

    def add_media(self, media):
        return self.append_media(media)

    def add_link(self, link):
        return self.append_link(link)

    def add_tag(self, tag):
        return self.append_tag(tag)

    def add_comment(self, comment):
        return self.append_comment(comment)

    #End functions to set object data

    def print_values(self):
        from pprint import pprint
        print("Title: " + self.get_title())
        print("Content: " + self.get_content())
        print("Content_html: " + self.get_content_html())
        print("Content_blocks: ")
        pprint(self.get_content_blocks())
        print("Media: ")
        pprint(self.get_media())
        print("Links: ")
        pprint(self.get_links())
        print("Rating: " + self.get_rating())
        print("Pluses: " + str(self.get_pluses()))
        print("Minuses: " + str(self.get_minuses()))
        print("Post_id: " + str(self.get_post_id()))
        print("Username: " + self.get_username())
        print("User_url: " + self.get_user_url())
        print("Comments_count: " + str(self.get_comments_count()))
        print("Saves: " + str(self.get_saves()))
        print("Shares: " + str(self.get_shares()))
        print("Datetime: " + self.get_datetime())
        print("Url: " + self.get_url())
        print("Tags: ")
        pprint(self.get_tags())
        print("Comments: ")
        pprint(self.get_comments())