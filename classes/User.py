class User:
    def __init__(self):
        self.nickname = ''
        self.url = ''
        self.about = ''
        self.avatar = ''
        self.reg_date = ''
        self.pluses = 0
        self.minuses = 0
        self.edited_posts = 0
        self.vote_edited_posts = 0
        self.communities = []
        self.rating = ''
        self.subscribers = 0
        self.comments = 0
        self.posts_count = 0
        self.posts = []
        self.posts_in_hot = 0

    def get_nickname(self):
        return self.nickname

    def get_url(self):
        return self.url

    def get_about(self):
        return self.about

    def get_avatar(self):
        return self.avatar

    def get_reg_date(self):
        return self.reg_date

    def get_pluses(self):
        return self.pluses

    def get_minuses(self):
        return self.minuses

    def get_edited_posts(self):
        return self.edited_posts

    def get_vote_edited_posts(self):
        return self.vote_edited_posts

    def get_communities(self):
        return self.communities

    def get_rating(self):
        return self.rating

    def get_subscribers(self):
        return self.subscribers

    def get_comments(self):
        return self.comments

    def get_posts_count(self):
        return self.posts_count

    def get_posts(self):
        return self.posts

    def get_posts_in_hot(self):
        return self.posts_in_hot

    def nickname(self):
        return self.get_nickname()

    def url(self):
        return self.get_url()

    def about(self):
        return self.get_about()

    def avatar(self):
        return self.get_avatar()

    def reg_date(self):
        return self.get_reg_date()

    def pluses(self):
        return self.get_pluses()

    def minuses(self):
        return self.get_minuses()

    def edited_posts(self):
        return self.get_edited_posts()

    def vote_edited_posts(self):
        return self.get_vote_edited_posts()

    def communities(self):
        return self.get_communities()

    def rating(self):
        return self.get_rating()

    def subscribers(self):
        return self.get_subscribers()

    def comments(self):
        return self.get_comments()

    def posts_count(self):
        return self.get_posts_count()

    def posts(self):
        return self.get_posts()

    def posts_in_hot(self):
        return self.get_posts_in_hot()

    def set_nickname(self, nickname):
        self.nickname = nickname
        return True

    def set_url(self, url):
        self.url = url
        return True

    def set_about(self, about):
        self.about = about
        return True

    def set_avatar(self, avatar):
        self.avatar = avatar
        return True

    def set_reg_date(self, reg_date):
        self.reg_date = reg_date
        return True

    def set_pluses(self, pluses):
        self.pluses = pluses
        return True

    def set_minuses(self, minuses):
        self.minuses = minuses
        return True

    def set_edited_posts(self, edited_posts):
        self.edited_posts = edited_posts
        return True

    def set_vote_edited_posts(self, vote_edited_posts):
        self.vote_edited_posts = vote_edited_posts
        return True

    def set_communities(self, communities):
        self.communities = communities
        return True

    def set_rating(self, rating):
        self.rating = rating
        return True

    def set_subscribers(self, subscribers):
        self.subscribers = subscribers
        return True

    def set_comments(self, comments):
        self.comments = comments
        return True

    def set_posts_count(self, posts_count):
        self.posts_count = posts_count
        return True

    def set_posts(self, posts):
        self.posts = posts
        return True

    def set_posts_in_hot(self, posts_in_hot):
        self.posts_in_hot = posts_in_hot
        return True

    def append_community(self, community):
        self.communities.append(community)
        return True

    def add_community(self, community):
        return self.append_community(community)

    def append_post(self, post):
        self.posts.append(post)
        return True

    def add_post(self, post):
        return self.append_post(post)

    def print_values(self):
        from pprint import pprint
        print("Nickname: "+self.nickname)
        print("Url: "+self.url)
        print("About: "+self.about)
        print("Avatar: "+self.avatar)
        print("Reg_date: "+self.reg_date)
        print("Plueses: "+str(self.pluses))
        print("Minuses: "+str(self.minuses))
        print("Edited_posts: " + str(self.edited_posts))
        print("Vote_edited_posts: " + str(self.vote_edited_posts))
        print("Communities: ")
        pprint(self.communities)
        print("Rating: " + self.rating)
        print("Subscribers: " + str(self.subscribers))
        print("Comments: " + str(self.comments))
        print("Posts_count: " + str(self.posts_count))
        print("Posts: ")
        pprint(self.posts)
        print("Posts_in_hot: " + str(self.posts_in_hot))