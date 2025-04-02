from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.server_api import ServerApi


class DBHelper:

    def __init__(self, host: str, port: int, user: str, password: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_animal = None

    def connect_to_db(self):
        try:
            client = MongoClient(
                f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}',
                server_api=ServerApi('1'),
                serverSelectionTimeoutMS=500
            )
            self.db_animal = client.animal
            client.server_info()
        except ServerSelectionTimeoutError:
            raise
        return self.db_animal

    def insert_cat(self, name: str, age: int, features: list):
        """
         Створює нового кота в базі даних
        :param name:
        :param age:
        :param features:
        :return:
        """
        self.db_animal.cats.insert_one(
            {
                "name": name,
                "age": age,
                "features": features,
            }
        )

    def read_cats(self) -> list:
        """
        Повертає всіх котів з бази даних
        :return list:
        """
        return self.db_animal.cats.find({})

    def read_cat(self, name) -> dict:
        """
        Повертає кота з бази даних по імені
        :param name:
        :return:
        """
        return self.db_animal.cats.find_one({"name": name})

    def update_age_cat(self, name, age):
        """
        Оновлює вік кота в базі даних
        :param name:
        :param age:
        :return:
        """
        self.db_animal.cats.update_one(
            {"name": name},
            {"$set": {"age": age}}
        )

    def add_one_feature_cat(self, name, feature):
        """
        Додає одну особливість коту в базі даних
        :param name:
        :param feature:
        :return:
        """
        self.db_animal.cats.update_one(
            {"name": name},
            {"$push": {"features": feature}}
        )

    def delete_cat(self, name):
        """
        Видаляє кота з бази даних по імені
        :param name:
        :return:
        """
        self.db_animal.cats.delete_one({"name": name})

    def delete_all_cats(self):
        """
        Видаляє всіх котів з бази даних
        :return:
        """
        self.db_animal.cats.delete_many({})