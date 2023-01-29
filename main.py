from api.vk_api import vk_user
from data import vk_token
from api.ya_disk_api import ya_disk_api
from data import ya_token
from time import sleep
import json
from tqdm import tqdm

def count_photo(obj):
    count = 0
    for i in obj.get_data():
        count += 1
    return count


if __name__ == '__main__':
    user_id = int(input('Введите id пользователя Вконтакте: '))
    ver_api = float(input('Введите версию api: '))
    user = vk_user(vk_token,user_id,ver_api, count=5)
    fin_list = []
    ya_disk = ya_disk_api(ya_token, f'id_{user_id}')
    for photo in tqdm(user.get_data(), total=count_photo(user)):
        ya_disk.upload_photo(photo[0],photo[1])
        sleep(0.1)
        photo_info = {'file_name': f'{photo[0]}.jpg', 'size': photo[-1]}
        fin_list.append(photo_info)
    with open('information.json', "a") as file:
        json.dump(fin_list, file, indent=2)