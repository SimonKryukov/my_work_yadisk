import requests
from tqdm import tqdm

from my_work import write_json

class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version="5.131", rev=True):
        self.token = token
        self.version = version
        self.rev = rev
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

    def download_photos(self, user_id, count):
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'extended': True,
            'album_id': 'profile',
            'owner_id': user_id,
            'count': count
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
        write_json('info_photos.json', info_photos)
        return info_photos

    def get_info_albums(self, user_id):
        get_albums_url = self.url + 'photos.getAlbums'
        albums_params = {
            'owner_id': user_id
            }
        req = requests.get(get_albums_url, params={**self.params, **albums_params}).json()
        if 'error' in req:
            print("Доступ к альбому запрещен пользователем ВК")
            raise SystemExit
        else:
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
            write_json('info_albums.json', info_albums)
            return info_albums
    
    def download_album_photos(self, user_id, id_alb, count):
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'extended': True,
            'owner_id': user_id,
            'album_id': id_alb,
            'count': count
            }
        req = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()
        if 'error' in req:
            print("Доступ к альбому запрещен пользователем ВК")
            raise SystemExit
        else:
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
            write_json('info_photos.json', info_photos)
            return info_photos
