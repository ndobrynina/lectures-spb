import requests

from configuration import TOKEN, VERSION

from datetime import datetime, timedelta


class VkGroup:

    def __init__(self, domain):
        self._domain = domain

    @staticmethod
    def get_current_time():
        return datetime.now().strftime("%d/%m")

    @staticmethod
    def time_limits():
        required_date = (datetime.now() - timedelta(days=7)).strftime("%d/%m/%y")
        unix_required_date = datetime.strptime(required_date, "%d/%m/%y").timestamp()
        return int(unix_required_date)

    def get_posts(self):
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': TOKEN,
                                    'v': VERSION,
                                    'domain': self._domain
                                })
        data = response.json()['response']['items']
        start = VkGroup.time_limits()
        post_dict = {}
        for i in data:
            if start <= i['date'] and 'Лекц' in i['text']:
                post_dict[i['date']] = i['text']
        return post_dict

    @staticmethod
    def clear_text(post):
        for s in post:
            if s == '[':
                ch_index = post.index(s)
                end_point = post.find('|', ch_index)
                post = post.replace(post[ch_index:end_point + 1], '')
            elif s == ']':
                number = post.count(s, 0)
                post = post.replace(s, '', number)
        return post
