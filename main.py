from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint
import random
import requests
import string
import json
import time


### Created by Nikita Kasianenko
### project#101

class Pikabu_api():
    def __init__(self, debug=False):
        self._login = False
        self._password = False
        self.session = requests.Session()
        self.session_file = 'session.cookie'
        self.headers = {
            'User-Agent': self._rotate_useragent(),
            'ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'ACCEPT-LANGUAGE': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        self.debug = debug

    def login(self):
        #login
        return False

    def get_best_posts(self, count=13):
        return self.get_special_posts('best', count)

    def get_popular_posts(self, count=13):
        return self.get_special_posts('', count)

    def get_special_posts(self, type_of_posts='', count=13):
        ### https://pikabu.ru/@moderator и https://pikabu.ru/@SupportTech, если вы это читаете - передайте программистам что бы как минимум 'x-csrf-token' и 'PHPSESS' не были пустыми
        if self.debug:
            execution_time_start = datetime.now()
        token = self._generate_token()
        basic_url = 'https://pikabu.ru/'+str(type_of_posts)+'?twitmode=1&of=v2&page='
        tmp_headers = {**self.headers, 'x-csrf-token': token, 'cookie': f'PHPSESS={token};'}
        posts = []
        import math
        for page in range(1, math.ceil(count / 13)+1):
            content = self._get_page(basic_url+str(page), tmp_headers)
            content = json.loads(self._clean_content(content))
            for post in content['data']['stories']:
                if len(posts) == count:
                    break
                soup = BeautifulSoup(post['html'], 'html.parser')
                posts.append(self._parse_post_content(soup, True))
            if math.ceil(count / 13) > 1:
                time.sleep(5)
        if self.debug:
            pprint(posts)
            print('execution time: ' + str(datetime.now() - execution_time_start))
        return posts

    def get_post(self, url):
        if self.debug:
            execution_time_start = datetime.now()
        content = self._get_page(url)
        soup = BeautifulSoup(content, 'html.parser')
        data = self._parse_post_content(soup, True)
        if self.debug:
            pprint(data)
            print('execution time: ' + str(datetime.now() - execution_time_start))
        return content

    def get_user(self, url):
        if self.debug:
            execution_time_start = datetime.now()
        content = self._get_page(url)
        soup = BeautifulSoup(content, 'html.parser')
        data = {}
        data['nickname'] = soup.findAll("span", {"itemprop": "additionalName"})[0].text
        data['url'] = url
        data['about'] = ''
        if soup.findAll("span", {"class": "profile__user-about-content"}):
            data['about'] = self._clean_content(soup.findAll("span", {"class": "profile__user-about-content"})[0].text)
        data['avatar'] = ''
        if soup.findAll("div", {"class": "avatar_large"})[0].findAll("img"):
            data['avatar'] = soup.findAll("div", {"class": "avatar_large"})[0].findAll("img")[0]['data-src']
        data['reg_date'] = soup.findAll("time", {"class": "hint"})[1]['datetime']
        data['pluses'] = soup.findAll("span", {"class": "profile__pluses"})[0].text
        data['minuses'] = soup.findAll("span", {"class": "profile__minuses"})[0].text
        data['edited_posts'] = soup.findAll("div", {"class": "profile__cedit-info"})[0].findAll("span", {"class": "profile__pluses"})[0].text
        data['vote_edited_posts'] = soup.findAll("div", {"class": "profile__cedit-info"})[1].findAll("span", {"class": "profile__pluses"})[0].text
        data['communities'] = self._get_communities(soup)
        data['rating'] = soup.findAll("div", {"class": "profile__section"})[1].findAll("span", {"class": "profile__digital"})[0]['aria-label'].replace("\u2005", "")
        data['subscribers'] = soup.findAll("div", {"class": "profile__section"})[1].findAll("span", {"class": "profile__digital"})[1].findAll("b")[0].text
        data['comments'] = soup.findAll("div", {"class": "profile__section"})[1].findAll("span", {"class": "profile__digital"})[2].findAll("b")[0].text
        data['posts_count'] = soup.findAll("div", {"class": "profile__section"})[1].findAll("span", {"class": "profile__digital"})[3].findAll("b")[0].text
        data['posts'] = []
        for post in soup.findAll("a", {"class": "story__title-link"}):
            data['posts'].append(post['href'])
        data['posts_in_hot'] = soup.findAll("div", {"class": "profile__section"})[1].findAll("span", {"class": "profile__digital"})[4].findAll("b")[0].text
        if self.debug:
            pprint(data)
            print('execution time: ' + str(datetime.now() - execution_time_start))
        return data

    def save_page(self, file_name, data):
        try:
            file = open(file_name, 'w')
            file.write(data)
            file.close()
            del file
            return True
        except Exception as error:
            print('Some error with save file')
            pprint(error)

    def _get_page(self, url, headers={}):
        try:
            if not headers:
                headers = self.headers
            answear = self.session.get(url, headers=headers)
        except Exception as error:
            print("Server aborted connection")
            pprint(error)
            exit()

        if answear:
            print('Success!')
        else:
            print('An error has occurred.')
            return False

        if answear.status_code == 200:
            print("Success parsed page")
        else:
            print("Some error excepted. Server returned "+str(answear.status_code)+" code")
            return False

        return answear.text

    def _get_comments(self, soup, indent=0):
        comments=[]
        for comment in soup.findAll("div", {"class": "comment", "data-indent": indent}):
            tmp_comment = {}
            tmp_comment['author_name'] = comment.findAll("div", {"class": "comment__user"})[0]['data-name']
            tmp_comment['author_url'] = 'https://pikabu.ru'+comment.findAll("a", {"class": "user"})[0]['href']
            tmp_comment['datetime'] = comment.findAll("time", {"class": "comment__datetime"})[0]['datetime']
            tmp_comment['link'] = comment.findAll("a", {"class": "comment__tool", "data-role": "link"})[0]['href']
            tmp_comment['rating'] = comment.findAll("div", {"class": "comment__rating-count"})[0].text
            tmp_comment['formatted_text'] = self._clean_content(comment.findAll("div", {"class": "comment__content"})[0].text)
            tmp = comment.findAll("div", {"class": "comment__rating-count"})[0]['aria-label']
            tmp_comment['pluses'] = [int(s) for s in tmp.split() if s.isdigit()][0]
            tmp_comment['minuses'] = [int(s) for s in tmp.split() if s.isdigit()][1]
            tmp_comment['subcomments'] = self._get_comments(comment.findAll("div", {"class": "comment__children"})[0], indent+1) if self._has_subcomments(comment) else []
            comments.append(tmp_comment)
            del tmp_comment
        return comments

    def _has_subcomments(self, soup):
        return True if soup.findAll("div", {"class": "comment__children"}) else False

    def _clean_content(self, content):
        clean_words = ['\n', '\r', '\t']
        for clean_word in clean_words:
            content = content.replace(clean_word, '')
        return content

    def _get_communities(self, soup):
        communities = []
        for community in soup.findAll("div", {"class": "communities-list_inline"})[0].findAll("span", {"class": "community_inline"}):
            tmp_data = {}
            tmp_data['title'] = community.findAll("a")[0].text
            tmp_data['url'] = 'https://pikabu.ru' + community.findAll("a")[0]['href']
            tmp_data['img'] = community.findAll("img")[0]['data-src']
            communities.append(tmp_data)
        return communities

    def _rotate_useragent(self):
        user_agent_list = [
            # Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            # Firefox
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
        ]
        return random.choice(user_agent_list)

    def _generate_token(self, length=30):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def _parse_post_content(self, soup, parse_from_feed=False):
        data = {}
        data['title'] = soup.findAll("header", {"class": "story__header"})[0].text
        data['content'] = ''
        data['content_html'] = ''
        data['content_blocks'] = []
        data['media'] = []
        data['links'] = []
        if soup.findAll("div", {"class": "story__content-inner"}):
            data['content'] = self._clean_content(soup.findAll("div", {"class": "story__content-inner"})[0].text)
            data['content_html'] = soup.findAll("div", {"class": "story__content-inner"})[0].prettify()
            if soup.findAll("div", {"class": "story__content-inner"})[0].findAll("img"):
                for img in soup.findAll("div", {"class": "story__content-inner"})[0].findAll("img"):
                    data['media'].append(img['data-large-image'])
            if soup.findAll("div", {"class": "story__content-inner"})[0].findAll("a"):
                for img in soup.findAll("div", {"class": "story__content-inner"})[0].findAll("a"):
                    if img['href'].split('.')[-1] != 'png':
                        data['links'].append(img['href'])
            if soup.findAll("div", {"class": "story-block"}):
                for block in soup.findAll("div", {"class": "story-block"}):
                    if block.findAll('img'):
                        data['content_blocks'].append(block.findAll('img')[0]['data-large-image'])
                    else:
                        data['content_blocks'].append(self._clean_content(block.text))
        data['rating'] = soup.findAll("div", {"class": "story__rating-count"})[0].text
        if not parse_from_feed:
            data['pluses'] = soup.findAll("div", {"class": "page-story__rating"})[0]['data-pluses']
            data['minuses'] = soup.findAll("div", {"class": "page-story__rating"})[0]['data-minuses']
            data['post_id'] = soup.findAll("section", {"class": "comments_show"})[0]['data-story-id']
            data['username'] = soup.findAll("section", {"class": "comments_show"})[0]['data-story-username']
            data['comments_count'] = soup.findAll("section", {"class": "comments_show"})[0]['data-total']
            data['save'] = soup.findAll("span", {"class": "story__save-count"})[0].text
            data['share'] = soup.findAll("span", {"class": "story__share-count"})[0].text
        else:
            data['post_id'] = soup.findAll("div", {"class": "story__rating-block"})[0]['data-story-id']
            data['username'] = soup.findAll("a", {"class": "user__nick"})[0].text
            data['comments_count'] = soup.findAll("span", {"class": "story__comments-link-count"})[0].text
        data['user_url'] = "https://pikabu.ru" + soup.findAll("a", {"class": "user__nick"})[0]['href']
        data['datetime'] = soup.findAll("time", {"class": "story__datetime"})[0]['datetime']
        data['url'] = soup.findAll("a", {"class": "story__comments-link"})[0]['href'].split("#")[0]
        data['tags'] = []
        for tag in soup.findAll("div", {"class": "story__tags"})[0].findChildren():
            data['tags'].append({'name': tag.text, 'url': 'https://pikabu.ru' + tag['href']})
        if not parse_from_feed:
            data['comments'] = self._get_comments(soup)
        return data

    def save_session(self):
        try:
            import pickle
            with open(self.session_file, 'wb') as f:
                pickle.dump(self.session.cookies, f)
            return True
        except Exception as error:
            pprint(error)
            return False

    def load_session(self):
        try:
            import pickle
            with open(self.session_file, 'rb') as f:
                self.session.cookies.update(pickle.load(f))
            return True
        except Exception as error:
            pprint(error)
            return False

if __name__ == "__main__":
    test = Pikabu_api(debug=True)
    # test.get_post('https://pikabu.ru/story/podvodim_itogi_2019_goda_7138233')
    # test.get_user('https://pikabu.ru/@moderator')
    # test.get_popular_posts()
    test.get_best_posts()