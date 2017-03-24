import pymongo
import platform
import os

# £
class Database(object):

    if platform.system() == "Windows":
        URI = "mongodb://127.0.0.1:27017"

    else:
        URI = os.environ.get("MONGOLAB_URI")

    # class static variables

    # FOR TESTING
    # URI = "mongodb://127.0.0.1:27017"


    # mongo lab adds this URI by default
    URI = os.environ.get("MONGOLAB_URI")
    DATABASE = None

    # print('Database here: database called')
    # def __init__(self):
    #     self.uri = ""
    #     self.database = None

    # the decorator tells python that self will not be used and that this
    # belongs to the database class as a whole
    @staticmethod
    def initialize():

        if platform.system() == "Windows":
            client = pymongo.MongoClient(Database.URI)
            Database.DATABASE = client['fullstack']

        else:
            client = pymongo.MongoClient(Database.URI)
            Database.DATABASE = client.get_default_database()




    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)


    @staticmethod
    def find(collection, query):
        # print('Database here: find called', collection, query)
        return Database.DATABASE[collection].find(query)


    @staticmethod
    def find_one(collection, query):
        # print('Database here: find_one called with', collection, query)
        # so why isn't it working when being called?
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)

if __name__ == '__main__':
    db = Database()
    db.initialize()

    # ok so it works
    # result = db.find_one("users", {"email": "test@test.com"})
    # result2 = db.find("users", {"email": "Procfile@Procfile.com"})
    # result3 = db.count('users')
    # print('why?', result2)


    result = db.find( "users", {} )
    print( [elem for elem in Database.find("users", {})] )
    # print('/n')

    result2 = db.find_one("users", {"email": 'test5@test.com'})
    print(result2)
