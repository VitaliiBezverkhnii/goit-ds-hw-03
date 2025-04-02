from pymongo.errors import ServerSelectionTimeoutError
from db_helper import DBHelper

db_helper = DBHelper(
    host='localhost',
    port=27017,
    user='root',
    password='123456'
)
try:
    db_helper.connect_to_db()
except ServerSelectionTimeoutError:
    print("Помилка підключення до бази даних")
    exit(1)
    

def show_all_cats():
    try:
        for el in db_helper.read_cats():
            print(el)
    except Exception as e:
        print(e)


def show_cat(name):
    try:
        print(db_helper.read_cat(name))
    except Exception as e:
        print(e)


def add_cat(name, age, features):
    try:
        db_helper.insert_cat(name, age, features)
    except Exception as e:
        print(e)


def update_age_cat(name, age):
    try:
        db_helper.update_age_cat(name, age)
    except Exception as e:
        print(e)


def add_feature_cat(name, feature):
    try:
        db_helper.add_one_feature_cat(name, feature)
    except Exception as e:
        print(e)


def delete_cat(name):
    try:
        db_helper.delete_cat(name)
    except Exception as e:
        print(e)


def delete_all_cats():
    try:
        db_helper.delete_all_cats()
    except Exception as e:
        print(e)


def main():
    add_cat('Луна', 3, ['грає з мишами', 'любить молоко'])
    add_cat('Tom', 3, ['грає з мишами', 'любить молоко'])
    add_cat('Barsik', 3, ['грає з мишами', 'любить молоко'])
    show_all_cats()
    update_age_cat('Луна', 4)
    add_feature_cat('Tom', 'любить спати')
    show_cat('Barsik')
    delete_cat('Луна')
    delete_all_cats()
    show_all_cats()


if __name__ == '__main__':
    main()
