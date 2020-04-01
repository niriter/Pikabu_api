from classes.User import User

class Parse_User():
    def __init__(self, debug=False):
        self.debug = debug
        self.user = User()

    def parse(self, soup, url=''):
        self.user.set_nickname(soup.findAll("span", {"itemprop": "additionalName"})[0].text)
        self.user.set_url(url)
        if soup.findAll("span", {"class": "profile__user-about-content"}):
            self.user.set_about(self._clean_text(soup.findAll("span", {"class": "profile__user-about-content"})[0].text))
        if soup.findAll("div", {"class": "avatar_large"})[0].findAll("img"):
            self.user.set_avatar(soup.findAll("div", {"class": "avatar_large"})[0].findAll("img")[0]['data-src'])
        for post in soup.findAll("a", {"class": "story__title-link"}):
            self.user.add_post(post['href'])
        self.user.set_reg_date(soup.findAll("time", {"class": "hint"})[1]['datetime'])
        self.user.set_pluses(soup.findAll("span", {"class": "profile__pluses"})[0].text)
        self.user.set_minuses(soup.findAll("span", {"class": "profile__minuses"})[0].text)
        self.user.set_edited_posts(soup.findAll("div", {"class": "profile__cedit-info"})[0]
                                   .findAll("span", {"class": "profile__pluses"})[0].text)
        self.user.set_vote_edited_posts(soup.findAll("div", {"class": "profile__cedit-info"})[1].findAll("span", {"class": "profile__pluses"})[0].text)
        self.user.set_rating(soup.findAll("div", {"class": "profile__section"})[1].findAll("span", {"class": "profile__digital"})[0]['aria-label'].replace("\u2005", ""))
        self.user.set_subscribers(soup.findAll("div", {"class": "profile__section"})[1].findAll("span", {"class": "profile__digital"})[1].findAll("b")[0].text)
        self.user.set_comments(soup.findAll("div", {"class": "profile__section"})[1].findAll("span", {"class": "profile__digital"})[2].findAll("b")[0].text)
        self.user.set_posts_count(soup.findAll("div", {"class": "profile__section"})[1].findAll("span", {"class": "profile__digital"})[3].findAll("b")[0].text)
        self.user.set_posts_in_hot(soup.findAll("div", {"class": "profile__section"})[1].findAll("span", {"class": "profile__digital"})[4].findAll("b")[0].text)
        self._get_communities(soup)
        if self.debug:
            self.user.print_values()
        return self.user

    def _get_communities(self, soup):
        for community in soup.findAll("div", {"class": "communities-list_inline"})[0].findAll("span", {"class": "community_inline"}):
            tmp_data = {}
            tmp_data['title'] = community.findAll("a")[0].text
            tmp_data['url'] = 'https://pikabu.ru' + community.findAll("a")[0]['href']
            tmp_data['img'] = community.findAll("img")[0]['data-src']
            self.user.add_community(tmp_data)
        return True

    def _clean_text(self, content):
        clean_words = ['\n', '\r', '\t']
        for clean_word in clean_words:
            content = content.replace(clean_word, '')
        return content
