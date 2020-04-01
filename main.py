from bs4 import BeautifulSoup
from datetime import datetime
from parsers.Post import Parse_Post
from parsers.User import Parse_User
from pprint import pprint
import random
import requests
import string
import json
import time
import logging


### Created by Nikita Kasianenko
### project#101

class Pikabu_api():
    def __init__(self, debug=False):
        self.logging_level = logging.INFO
        self._set_logger()
        self.logger.info("Start init")
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
        self.logger.info("End init")

    def login(self):
        #login
        return False

    def get_communities_feed_posts(self, count=13):
        return self.get_special_posts('communities/feed', count)

    def get_disputed_posts(self, count=13):
        return self.get_special_posts('disputed', count)

    def get_most_saved_posts(self, count=13):
        return self.get_special_posts('most-saved', count)

    def get_new_posts(self, count=13):
        return self.get_special_posts('new', count)

    def get_best_posts(self, count=13):
        return self.get_special_posts('best', count)

    def get_popular_posts(self, count=13):
        return self.get_special_posts('', count)

    def get_special_posts(self, type_of_posts='', count=13):
        ### https://pikabu.ru/@moderator и https://pikabu.ru/@SupportTech, если вы это читаете - передайте программистам что бы как минимум 'x-csrf-token' и 'PHPSESS' не были пустыми
        self.logger.info(f'get_special_posts(type_of_posts:{type_of_posts}')
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
                wrapper = Parse_Post(True, self.debug)
                posts.append(wrapper.parse(BeautifulSoup(post['html'], 'html.parser')))
                del wrapper
            if math.ceil(count / 13) > 1:
                time.sleep(5)
        if self.debug:
            pprint(posts)
        self.logger.info('get_special_posts - execution time: ' + str(datetime.now() - execution_time_start))
        return posts

    def get_post(self, url):
        self.logger.info(f'get_post(url:{url}')

        execution_time_start = datetime.now()
        soup = BeautifulSoup(self._get_page(url), 'html.parser')
        wrapper = Parse_Post(False, self.debug)
        data = wrapper.parse(soup)

        self.logger.info('get_post - execution time: ' + str(datetime.now() - execution_time_start))
        return data

    def get_user(self, url):
        self.logger.info(f'get_user(url:{url}')

        execution_time_start = datetime.now()
        content = self._get_page(url)
        parse_user = Parse_User(self.debug)
        data = parse_user.parse(BeautifulSoup(content, 'html.parser'), url)

        self.logger.info('get_user - execution time: ' + str(datetime.now() - execution_time_start))
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
            answer = self.session.get(url, headers=headers)
        except Exception as error:
            self.logger.error(f"Server aborted connection (Error: {error})")
            exit()

        if answer:
            self.logger.info("Server returned answer")
        else:
            self.logger.error("Server not returned answer")
            exit()

        if answer.status_code == 200:
            self.logger.info("Page status_code: 200")
        else:
            self.logger.error(f"Page status_code: {str(answer.status_code)}")
            exit()
        return answer.text

    def _clean_content(self, content):
        clean_words = ['\n', '\r', '\t']
        for clean_word in clean_words:
            content = content.replace(clean_word, '')
        return content

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
        c = random.choice(user_agent_list)
        self.logger.info(f"User-agent: {c}")
        return c

    def _generate_token(self, length=30):
        letters = string.ascii_lowercase
        t = ''.join(random.choice(letters) for i in range(length))
        self.logger.info(f"Generated token ({t})")
        return t

    def _set_logger(self):
        self.logger = logging.getLogger('Pikabu-api')
        self.logger.setLevel(self.logging_level)
        del self.logging_level
        fh = logging.FileHandler('logs.txt', mode='w')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def save_session(self):
        try:
            import pickle
            with open(self.session_file, 'wb') as f:
                pickle.dump(self.session.cookies, f)
            self.logger.info(f"Session saved to {self.session_file}")
            return True
        except Exception as error:
            self.logger.error(f"Session not saved to {self.session_file}; Error: {error}")
            return False

    def load_session(self):
        try:
            import pickle
            with open(self.session_file, 'rb') as f:
                self.session.cookies.update(pickle.load(f))
            self.logger.info(f"Session loaded from {self.session_file}")
            return True
        except Exception as error:
            self.logger.error(f"Session not loaded from {self.session_file}; Error: {error}")
            return False

    '''class Pikabu_app_api:
        def get_page(self):
            #NOT WORKING
            test = self.PikabuPostRequest()
            attributes = []
            page_id = 7138233
            test.PikabuPostRequest("page", attributes)

        class PikabuPostRequest:
            def PikabuPostRequest(self, request_url, attributes):
                requester = self.PikabuRequest()
                requester.PikabuRequest("https://api.pikabu.ru/v1/", request_url, attributes)
                page_id = 7138233
                requester.buildParams(["page_id", page_id])
                # setHttpMethod(HttpHelper.METHOD_POST);

            class PikabuRequest():
                def __init__(self):
                    self.f42435a = ''
                    self.url = ''
                    self.method = ''
                    self.headers = {}

                def nativeBuildHash(self, context, data_array, str1, str2):
                    from ctypes import *
                    pprint(context, data_array, str1, str2)
                    libc = CDLL("libnative-lib.so")
                    Java_ru_pikabu_android_server_PikabuRequest_nativeBuildHash = libc.Java_ru_pikabu_android_server_PikabuRequest_nativeBuildHash
                    pprint(Java_ru_pikabu_android_server_PikabuRequest_nativeBuildHash(context, data_array, str1, str2))
                    return ''

                def PikabuRequest(self, str1, str2, attributes):
                    url = str1 + str2
                    if (not attributes) and (len(attributes) == 0):
                        url = url + ""
                    else:
                        # add attributes to url
                        url = url
                    self.url = url
                    self.method = 'POST'
                    self.headers['Content-Type'] = 'application/json'
                    self.headers['DeviceId'] = ''  # get device-id
                    self.f42435a = str2
                    return

                def parseResponse(self, ResponseInfo):
                    if ResponseInfo.status_code == 500:
                        return False
                    else:
                        return True

                def buildParams(self, data):
                    return self.mo36477a(data)

                def mo36477a(self, data):
                    return self.build_data(data, self.f42435a, [])

                def build_data(self, data, url, var):
                    valueOf = str(time.time()).replace('.', '')[:13]
                    a = self.combine_list(data, ["new_sort", 1, "id", "iws"])
                    a = self.combine_list(a, ["hash", self.some_func(a, valueOf, url, var), "token", valueOf])
                    return a

                def combine_list(self, array, array2):
                    array3 = []
                    for elem in array:
                        array3.append(elem)
                    for elem in array2:
                        array3.append(elem)
                    return array3

                def some_func(self, data, time, url, var):
                    arrayList = {}
                    arrayList2 = []
                    i = 1
                    for i in range(0, len(data), 2):
                        pprint(i)
                        arrayList[data[i]] = data[(i + 1)]
                        i = i + 1
                    # m52551a(arrayList, arrayList2, var)
                    nativeBuildHash = self.nativeBuildHash('', arrayList, time, url)
                    if nativeBuildHash:
                        return nativeBuildHash.strip()
                    else:
                        return ""
'''

if __name__ == "__main__":
    test = Pikabu_api(debug=True)
    # test.get_post('https://pikabu.ru/story/podvodim_itogi_2019_goda_7138233')
    # test.get_user('https://pikabu.ru/@moderator')
    # test.get_popular_posts()
    # test.get_best_posts()
    # test.get_new_posts()
    # test.get_most_saved_posts()
    # test.get_disputed_posts()
    # test.get_communities_feed_posts()