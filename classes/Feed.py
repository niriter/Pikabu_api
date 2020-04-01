class Feed:
    def __init__(self):
        self.url = ''
        self.name = ''
        self.posts_count = 0
        self.has_about = False
        self.about = ''
        self.date = ''
        self.posts = []

    def __iter__(self):
        return self.posts

    def __next__(self):
        if not hasattr(self, 'current_post_number'):
            self.current_post_number = 1
        if self.current_post_number > len(self.posts):
            raise StopIteration
        else:
            self.current_post_number += 1
            return self.posts[self.current_post_number]

    def get_url(self):
        return self.url

    def get_name(self):
        return self.name

    def get_posts_count(self):
        return self.posts_count

    def get_has_about(self):
        return self.has_about

    def get_about(self):
        return self.about

    def get_date(self):
        return self.date

    def get_posts(self):
        return self.posts

    def url(self):
        return self.get_url()

    def name(self):
        return self.get_name()

    def posts_count(self):
        return self.get_posts_count()

    def has_about(self):
        return self.get_has_about()

    def about(self):
        return self.get_about()

    def date(self):
        return self.get_date()

    def posts(self):
        return self.get_posts()

    def set_url(self, url):
        self.url = url
        return True

    def set_name(self, name):
        self.name = name
        return True

    def set_posts_count(self, posts_count):
        self.posts_count = posts_count
        return True

    def set_has_about(self, has_about):
        self.has_about = has_about
        return True

    def set_about(self, about):
        self.about = about
        return True

    def set_date(self, date):
        self.date = date
        return True

    def set_posts(self, posts):
        self.posts = posts
        return True

    def append_post(self, post):
        self.posts.append(post)
        return True

    def add_post(self, post):
        return self.append_post(post)