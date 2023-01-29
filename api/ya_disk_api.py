import requests
from data import ya_token

class ya_disk_api:
    url = 'https://cloud-api.yandex.net'
    def __init__(self, token, name_folder):
        self.name_folder = name_folder
        self.token = token
        self.create_new_folder()
    def create_new_folder(self):
        specific_url = '/v1/disk/resources'
        metod_url = self.url + specific_url
        params = {'path': self.name_folder}
        headers = {'Content-Type': 'application/json',
                   'Authorization': self.token
                   }
        create_folder = requests.put(metod_url, params=params, headers=headers)
        print(f'Папка "{self.name_folder}" успешно создана.')

    def upload_photo(self,name_file, url):
        specific_url = '/v1/disk/resources/upload'
        metod_url = self.url + specific_url
        params = {'path': f'{self.name_folder}/{name_file}',
                  'url': url
                  }

        headers = {'Content-Type': 'application/json',
                   'Authorization': self.token
                   }

        save_file = requests.post(metod_url, params=params,headers=headers)


