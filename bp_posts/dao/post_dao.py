import json
from json import JSONDecodeError


from bp_posts.dao.post import Post
from exceptions.data_exceptions import DataSourceError


class PostDAO:
    """ Менеджер ууу постов """

    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """ Загружает данные из JSON файла и возвращает список словарей ([],[])"""

        try:
            with open(self.path, 'r', encoding='utf-8') as file:
               posts_data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f'Не удается получить данные из файла {self.path}')

        return posts_data

    def _load_posts(self):
        """ Возвращает список  экземпляров(примеров) POST-а """

        posts_data = self._load_data()
        list_of_posts = [Post(**post_data) for post_data in posts_data]
        return list_of_posts

    def get_all(self):
        """получает все посты"""

        posts = self._load_posts()
        return posts

    def get_by_pk(self, pk):
        """Получает пост по его PK номеру """

        if type(pk) != int:
            raise TypeError("pk must be an integer")

        posts = self._load_posts()
        for post in posts:
            if post.pk == pk:
                return post

    def search_in_content(self, substring):
        """ Ищет пост где есть substring трока"""

        if type(substring) != str:
            raise TypeError("substring must be an string")

        substring = substring.lower()
        posts = self._load_posts()

        matching_posts = [post for post in posts if substring in post.content.lower()]

        return matching_posts

    def get_by_poster(self, user_name):
        """ Ищет посты с 1 автором"""

        if type(user_name) != str:
            raise TypeError("user_name must be an string")

        user_name = user_name.lower()
        posts = self._load_posts()

        matching_posts = [post for post in posts if post.poster_name.lower() == user_name]

        return matching_posts
