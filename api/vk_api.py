from datetime import datetime

import requests


class VkUser:
    method_url = 'https://api.vk.com/method/photos.get'
    method_users_get = 'https://api.vk.com/method/users.get'
    type_photo = ['w', 'z', 'y', 'x', 'r', 'q', 'p', 'o', 'm', 's']

    def __init__(self, token, user_id, version=5.131, album_type='profile', count=5):
        self.params_users_get = {
            'access_token': token,
            'user_ids': user_id,
            'fields': 'screen_name',
            'v': version
        }
        response = requests.get(self.method_users_get, params=self.params_users_get)
        users = response.json()
        user_id = users['response'][0]['id']

        self.params = {
            'access_token': token,
            'owner_id': user_id,
            'album_id': album_type,
            'extended': True,
            'photo_sizes': True,
            'v': version,
            'count': count
        }

    def _get_info_photo(self):
        response = requests.get(self.method_url, self.params)
        photos = response.json()
        return photos['response']['items']

    def get_data(self):
        list_all_count = []
        for photo in self._get_info_photo():
            list_all_count.append(photo['likes']['count'])
        list_dupl = [x for x in list_all_count if list_all_count.count(x) >= 2]
        for photo in self._get_info_photo():
            count_like = photo['likes']['count']
            date = datetime.utcfromtimestamp(int(photo['date'])).strftime('%d.%m.%Y')
            sizes = photo['sizes']
            sorted_size = sorted(sizes, key=lambda size: self.type_photo.index(size['type']))
            if count_like not in set(list_dupl):
                yield count_like, sorted_size[0]['url'], sorted_size[0]['type']
            else:
                yield str(count_like) + '_' + date, sorted_size[0]['url'], sorted_size[0]['type']
