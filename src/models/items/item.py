import requests
from bs4 import BeautifulSoup
import re
import src.models.items.constants as ItemConstants
from src.common.database import Database
from src.models.stores.store import Store
import uuid


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        # none because otherwise you would be fetching it from the internet each time
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    # , tag_name, query
    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)

        # i suspect heroku doens't support unicode and that's why i'm getting a none type error
        print(u"Unicode test: £ ’ …")

        # getting an error on heroku with this line, i think it's not finding the right element
        string_price = element.text.strip()

        # finds the 115.00 from something like 115.00
        # in brackets for the matching group
        pattern = re.compile("(\d+\.\d+)")

        match = pattern.search(string_price)
        # print(match)
        self.price = match.group()
        # print('self.price', self.price)
        return self.price

    def save_to_mongo(self):
        # Database.insert(ItemConstants.COLLECTION, self.json())
        # changed so that the price can be kept upto date
        Database.update(ItemConstants.COLLECTION, {"_id": self._id}, self.json())


    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price

        }

    @classmethod
    def from_mongo(cls, name):
        price_data = Database.find_one(ItemConstants.COLLECTION, {"name": name})
        return cls(**price_data)

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))




if __name__ == '__main__':
    Database.initialize()
    # meh = Store("John Lewis", "http://www.johnlewis.com", "span", {"id": "price"})
    # Procfile = Item("herman miller aeron office chair", "http://www.johnlewis.com/herman-miller-aeron-office-chair/p230630306",
    #             Store("John Lewis", "http://www.johnlewis.com", "p", {"class": "price"}))

    # print("price is: ", Procfile.price)

    # def __init__(self, name, url, _id=None):
    meh = Item("John Lewis", "http://www.johnlewis.com/herman-miller-aeron-office-chair/p230630306", "e3f9b504a1fe478898fb797083cc9adc")
    meh.load_price()
    meh.save_to_mongo()