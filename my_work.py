import vk
import yandex

token_ya = ''
token_vk = ''


def start_program():
    vk_id = input("Введите id пользователя: ")
    num_photos = int(input("Введите нужное количество фото для сохранения: "))
    vk_client = vk.VkUser(token_vk)
    ya_client = yandex.YaDisk(token_ya, vk_client.download_photos(vk_id, num_photos))
    folder = ya_client.create_folder(input("Введите новое название папки, которую хотите создать в Яндекс Диске: "))
    ya_client.upload_from_internet(folder)
    return


        # while True:
        #     start = int(input("Для ввода id(Нажмите '1'), Для ввода имя профиля(Нажмите '2'): " )) 
        #     if start == 1:
        #         id = input("Пожалуйста введите id Пользователя ВК: ")
        #         return id
        #     elif start == 2:
        #         user = input("Пожалуйста введите имя Пользователя ВК: ")
        #         return vk_client.get_id_person(user)
        #     else:
        #         print("Попробуйте ввести нужную команду")

if __name__ == "__main__":
    start_program()
    
    
    ## Загрузка фото из альбома

    # vk_client.get_info_albums(vk_id)
    # id_album = input("Введите id нужного альбома: ")
    # ya_client_album = YaDisk(token_ya, vk_client.download_album_photos(vk_id, id_album, num_photos))
    # folder_album = ya_client_album.create_folder(input("Введите новое название папки, которую хотите создать в Яндекс Диске: "))
    # ya_client_album.upload_from_internet(folder_album)