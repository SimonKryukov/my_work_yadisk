import json
import requests
from pprint import pprint
import datetime
import time
from tqdm import tqdm

class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version="5.131", rev=True, count=7):
        self.token = token
        self.version = version
        self.rev = rev
        self.count = count
        self.params = {
            'access_token': token, 
            "v": version, 
            }

    def get_id_person(self, user):
        get_id = self.url + "users.get"
        params = {
            "access_token": self.token,
            "v": "5.131",
            "user_ids": user
            }
        responce = requests.get(get_id, params=params)
        result = responce.json()['response']
        for info in result:
            return str(info['id'])

    def download_photos(self, user_id):
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'extended': True,
            'album_id': 'profile',
            'owner_id': user_id,
            'count': 7
        }
        req = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()
        result = req['response']['items']
        info_photos = []
        for photo in result:
            info_photos.append(
                {
                    "file_name": str(photo['likes']['count']) + '.jpg',
                    "size": photo["sizes"][-1]["type"],
                    "date": photo["date"],
                    "url": photo["sizes"][-1]["url"]
                }
            )
        with open('info_photos.json', 'w') as file:
            json.dump(info_photos, file, ensure_ascii=False, indent=2)
        return info_photos

    def get_info_albums(self, user_id):
        get_albums_url = self.url + 'photos.getAlbums'
        albums_params = {
            'owner_id': user_id
        }
        req = requests.get(get_albums_url, params={**self.params, **albums_params}).json()
        result = req['response']['items']
        info_albums = []
        for album in result:
            info_albums.append(
                {
                    "id_album": album['id'],
                    "photos": album["size"],
                    "album_name": album["title"]
                }
            )
        with open('info_albums.json', 'w', encoding='utf-8') as file:
            json.dump(info_albums, file, ensure_ascii=False, indent=2)
        return info_albums
    
    def download_album_photos(self, user_id, id_alb):
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'extended': True,
            'owner_id': user_id,
            'album_id': id_alb,
        }
        req = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()
        result = req['response']['items']
        info_photos = []
        for photo in result:
            info_photos.append(
                {
                    "file_name": str(photo['likes']['count']) + '.jpg',
                    "size": photo["sizes"][-1]["type"],
                    "date": photo["date"],
                    "url": photo["sizes"][-1]["url"]
                }
            )
        with open('info_photos.json', 'w') as file:
            json.dump(info_photos, file, ensure_ascii=False, indent=2)
        return info_photos

class YaDisk:
    host = 'https://cloud-api.yandex.net/'
    def __init__(self, token, download_link):
        self.token = token
        self.download_link = download_link

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def create_folder(self, folder_name):
        uri = 'v1/disk/resources/'
        url = self.host + uri
        params = {'path': f'/{folder_name}/'}
        response = requests.put(url, headers=self.get_headers(), params=params)
        return folder_name

    def upload_from_internet(self, folder_name):
        uri = 'v1/disk/resources/upload/'
        url = self.host + uri
        likes_list = []
        for urls in tqdm(self.download_link, desc='Загружается на Яндекс Диск. Пожалуйста, подождите...'):
            if urls['file_name'] not in likes_list:
                likes_list.append(urls['file_name'])
                path = f"/{folder_name}/{urls['file_name']}"
            else:
                value = datetime.datetime.fromtimestamp(urls['date'])
                path = f"/{folder_name}/{value:%d-%m-%Y}.jpg"
            params = {'path': path, 'url': urls['url']}
            time.sleep(1)
            response = requests.post(url, headers=self.get_headers(), params=params)
        print("Выполнено")

if __name__ == "__main__":
    token_vk = ''
    token_ya = ''
    vk_client = VkUser(token_vk)
    def start_program():
        while True:
            start = int(input("Для ввода id(Нажмите '1'), Для ввода имя профиля(Нажмите '2'): " )) 
            if start == 1:
                id = input("Пожалуйста введите id Пользователя ВК: ")
                return id
            elif start == 2:
                user = input("Пожалуйста введите имя Пользователя ВК: ")
                return vk_client.get_id_person(user)
            else:
                print("Попробуйте ввести нужную команду")

    vk_id = start_program()
    
    ## Загрузка фото из профиля

    ya_client = YaDisk(token_ya, vk_client.download_photos(vk_id))
    folder = ya_client.create_folder(input("Введите новое название папки, которую хотите создать в Яндекс Диске: "))
    ya_client.upload_from_internet(folder)

    ## Загрузка фото из альбома

    vk_client.get_info_albums(vk_id)
    id_album = input("Введите id нужного альбома: ")
    ya_client_album = YaDisk(token_ya, vk_client.download_album_photos(vk_id, id_album))
    folder_album = ya_client_album.create_folder(input("Введите новое название папки, которую хотите создать в Яндекс Диске: "))
    ya_client_album.upload_from_internet(folder_album)