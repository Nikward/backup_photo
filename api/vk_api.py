import requests
from datetime import datetime

class VkUser:
    method_url = 'https://api.vk.com/method/photos.get'
    type_photo = ['w', 'z', 'y', 'x', 'r', 'q', 'p', 'o', 'm', 's']
    def __init__(self, token, user_id, version, album_type='profile',count=5):
        self.params = {
            'access_token':token,
            'owner_id': user_id,
            'album_id': album_type,
            'extended':True,
            'photo_sizes':True,
            'v': version,
            'count':count
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
            sorted_size = sorted(sizes,key= lambda size: self.type_photo.index(size['type']))
            yield count_like, sorted_size[0]['url'], date, sizes[0]['type']