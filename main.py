from time import sleep
import json
import configparser

from tqdm import tqdm

from api.vk_api import VkUser
from api.ya_disk_api import YandexApi


def count_photo(obj):
    count = 0
    for i in obj.get_data():
        count += 1
    return count


def get_tokens():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    vk_token = config['vk_api']['vk_token']
    ya_token = config['yandex_api']['ya_token']
    return vk_token, ya_token


if __name__ == '__main__':
    user_id = input('Введите id или screen_name пользователя Вконтакте: ')
    amount_photo = int(input('Укажите количество загружаемых фото: '))

    user = VkUser(get_tokens()[0], user_id=user_id, count=amount_photo)

    fin_list = []
    ya_disk = YandexApi(get_tokens()[1], f'id_{user_id}')
    for photo in tqdm(user.get_data(), total=count_photo(user)):
        ya_disk.upload_photo(photo[0], photo[1])
        sleep(0.1)
        photo_info = {'file_name': f'{photo[0]}.jpg', 'size': photo[-1]}
        fin_list.append(photo_info)

    with open('information.json', "a") as file:
        json.dump(fin_list, file, indent=2)
