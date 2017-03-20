import pymongo


class Database(object):
    # class static variables
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None
    # there's no evidence that this class is working at all

    print('Database here: database called')
    # def __init__(self):
    #     self.uri = ""
    #     self.database = None

    # the decorator tells python that self will not be used and that this
    # belongs to the database class as a whole
    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)


    @staticmethod
    def find(collection, query):
        print('Database here: find called', collection, query)
        return Database.DATABASE[collection].find(query)


    @staticmethod
    def find_one(collection, query):
        print('Database here: find_one called with', collection, query)
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
    # result2 = db.find("users", {"email": "blah@blah.com"})
    # result3 = db.count('users')
    # print('why?', result2)

    print('users')
    result = db.find_one("users", "test5@test.com")
    print(result)
    print('/n')