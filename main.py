import requests
from bs4 import BeautifulSoup
from pprint import pprint

class Pikabu_api():
    def __init__(self):
        self._login = False
        self._password = False
        self.session = requests.Session()
        self.session_file = 'session.cookie'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
            'ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'ACCEPT-LANGUAGE': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        self.debug = True

    def login(self):
        #login
        return False

    def get_post(self, url):
        content = self._get_page(url)
        soup = BeautifulSoup(content, 'html.parser')
        data = {}
        data['title'] = soup.findAll("span", {"class": "story__title-link"})[0].text
        data['content'] = self._clean_content(soup.findAll("div", {"class": "story__content-inner"})[0].text)
        data['rating'] = soup.findAll("div", {"class": "story__rating-count"})[0].text
        data['pluses'] = soup.findAll("div", {"class": "page-story__rating"})[0]['data-pluses']
        data['minuses'] = soup.findAll("div", {"class": "page-story__rating"})[0]['data-minuses']
        data['post_id'] = soup.findAll("section", {"class": "comments_show"})[0]['data-story-id']
        data['post_url'] = url
        data['username'] = soup.findAll("section", {"class": "comments_show"})[0]['data-story-username']
        data['user_url'] = "https://pikabu.ru"+soup.findAll("a", {"class": "user__nick"})[0]['href']
        data['comments_count'] = soup.findAll("section", {"class": "comments_show"})[0]['data-total']
        data['datetime'] = soup.findAll("time", {"class": "story__datetime"})[0]['datetime']
        data['save'] = soup.findAll("span", {"class": "story__save-count"})[0].text
        data['share'] = soup.findAll("span", {"class": "story__share-count"})[0].text
        data['tags'] = []
        for tag in soup.findAll("div", {"class": "story__tags"})[0].findChildren():
            data['tags'].append({'name': tag.text, 'url': 'https://pikabu.ru'+tag['href']})
        data['comments'] = self._get_comments(soup)
        pprint(data['comments'])
        exit()

        if self.debug:
            pprint(data)
        return content

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

    def _get_page(self, url):
        try:
            answear = self.session.get(url, headers=self.headers)
        except Exception as error:
            print("Server aborted connection")
            pprint(error)
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

        clean_words = ['\n', '\r']

        for clean_word in clean_words:
            content = content.replace(clean_word, '')
        return content

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
