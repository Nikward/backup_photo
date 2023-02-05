from datetime import datetime

import requests


class VkUser:
    method_url = 'https://api.vk.com/method/photos.get'
    method_url_screen = 'https://api.vk.com/method/users.get'
    type_photo = ['w', 'z', 'y', 'x', 'r', 'q', 'p', 'o', 'm', 's']

    def __init__(self, token, user_id, version=5.131, album_type='profile', count=5):
        self.params_screen = {
            'access_token': token,
            'user_ids': user_id,
            'fields': 'screen_name',
            'v': version
        }
        response = requests.get(self.method_url_screen, params=self.params_screen)
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
        for photo in self._get_info_photo():
            count_like = photo['likes']['count']
            date = datetime.utcfromtimestamp(int(photo['date'])).strftime('%d.%m.%Y')
            sizes = photo['sizes']
            sorted_size = sorted(sizes, key=lambda size: self.type_photo.index(size['type']))
            yield count_like, sorted_size[0]['url'], date, sizes[0]['type']
