import uuid
import requests
import src.models.alerts.constants as AlertConstants
import datetime
from src.common.database import Database
from src.models.items.item import Item

# email stuff
import smtplib
from email.mime.text import MIMEText


class Alert(object):
    def __init__(self, user_email, price_limit, item_id=None, last_checked=None, _id=None, active=True):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item_id = item_id
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow(
        ) if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id

        # why doesn't this work? well it works if you put it last
        self.active = active

    def __repr__(self):
        return "<alert for {} on item {} with price {}".format(self.user_email, self.item.name, self.price_limit)

    # def send(self):
    #     return requests.post(
    #         AlertConstants.URL,
    #         auth = ("api", AlertConstants.API_KEY),
    #         data = {
    #             "from": AlertConstants.FROM,
    #             "to": self.user_email,
    #             "subject": "Price limit reached for {}".format(self.item.name),
    #             "text": "Found a deal (link here)"
    #         }
    #     )

    def send(self):
        # print('SEND HAS BEEN CALLED')
        msg = MIMEText(
            'Hi {} we have found a price alert for you.'.format(self.user_email))
        msg['Subject'] = "Price alert"
        msg['From'] = AlertConstants.FROM

        # assert self.user_email is None
        # msg['To'] = AlertConstants.TEST_EMAIL if self.user_email is None else self.user_email
        msg['To'] = AlertConstants.TEST_EMAIL

        s = smtplib.SMTP(AlertConstants.SMPT_URL, AlertConstants.SMPT_PORT)

        s.login(AlertConstants.FROM, AlertConstants.SMPT_KEY)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()

    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        # gives a datetime object then subtracts ten minutes to give a time ten minutes ago
        # DATE BEFORE TEN MINUTES AGO
        last_updated_limit = datetime.datetime.utcnow(
        ) - datetime.timedelta(minutes=minutes_since_update)
        # returns objects where the update time is greater than 10 minutes ago
        # the cls gives the object with is an alert object
        # so it's reading from the database and creating alert objects then checking their properties
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {"last_checked":
                                                       {"$lte": last_updated_limit},
                                                       "active": True
                                                       })]

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {
                        "_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item_id": self.item_id,
            "active": self.active
        }

    def load_item_price(self):
        # check the item price via item class?
        # TypeError: load_price() missing 2 required positional arguments: 'tag_name' and 'query'
        self.item.load_price()
        # update last checked
        self.last_checked = datetime.datetime.utcnow()
        # save the item price in the item database
        self.item.save_to_mongo()
        # save updated time value to the database
        self.save_to_mongo()

        # this was missing
        # self.send_email_if_price_reached()

        return self.item.price

    def send_email_if_price_reached(self):
        # print('send email if price reached called')
        if float(self.item.price) < float(self.price_limit):
            self.send()

    # had to change this to a class method because it wasn't getting the variable user_email
    @classmethod
    def find_by_user_email(cls, user_email):
        # print('hello from find_by_user_email')
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {'user_email': user_email})]

    @classmethod
    def find_by_id(cls, alert_id):
        # cls** upacks the object properties in the database and returns the object using the constructor
        # so an object is returned withe the pr
        return cls(**Database.find_one(AlertConstants.COLLECTION, {'_id': alert_id}))

    def deactivate(self):
        self.active = False
        self.save_to_mongo()
        # print('deactive called')

    def activate(self):
        self.active = True
        self.save_to_mongo()
        # print('activate called, self.active == ', self.active)

    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {'_id': self._id})


if __name__ == '__main__':
    Database.initialize()

    # def __init__(self, user_email, price_limit, active=True, item_id=None, last_checked=None, _id=None):
    # alert_one = Alert("atomicpenguines@gmail.com", 900, True, "e3f9b504a1fe478898fb797083cc9adc")
    alert_one = Alert("atomicpenguines@gmail.com", 900,
                      "e3f9b504a1fe478898fb797083cc9adc")
    # print(alert_one.item)
    # alert object has no attribute item_id
    # print( Item.get_by_id("e3f9b504a1fe478898fb797083cc9adc") )

    alert_one.save_to_mongo()

    blah = alert_one.load_item_price()
    print(blah)
