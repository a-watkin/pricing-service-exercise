import src.models.users.errors as UserError
from src.common.database import Database
from src.common.utils import Utils
# pycharm is not great with imports it seems, it removes the import below when you use the hotkey for import
# optermisation
import uuid
from src.models.alerts.alert import Alert

from src.models.users import constants as UserConstants

class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        # the dot hex makes it a string
        self._id = uuid.uuid4().hex if _id is None else _id


    # string representation of the class? that doens't make much sense
    def __repr__(self):
        return "<User {}>".format(self.email)



    @staticmethod
    def is_login_valid(email, password):
        """
        This method varifies an e-mail/password combo (as sent by the site forms) is valid or not.
        Checks that the e-mail exists, and that the passwrod asscoaited to that email is correct.

        :param email: the user's email
        :param password: a sha512 hashed password, obscures the password
        :return: True if valid, false otherwise
        """
        user_data = Database.find_one("users", {"email": email}) # password in sha512 -> pbkdf2_sha512

        if user_data is None:
            # Tell the user that their e-mail doesn't exist
            raise UserError.UserNotExistsError("Your username does not exist.")

        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell the user their password is wrong
            raise UserError.IncorrectPasswordError("Your password is incorrect.")

        return True


    @staticmethod
    def register_user(email, password):
        """
        Registers a user using email and password
        Password is already hashed as sha-512
        :param email: user's email might be invalid
        :param password: sha512-hashed password
        :return: True if registered successfully or false otherwise (exceptions can also be raised)
        """

        # if the user already exists, then you can't register them
        # display some message to that effect?

        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        # if they don't currently exist then add them to them to the database

        if user_data is not None:
            # tell user they are already registered
            raise UserError.UserAlreadyRegisteredError("The e-mail is already registered.")

        # check the email is valid
        if not Utils.email_is_valid(email):
            # tell the user their email is invalid
            raise UserError.InvalidEmailError("The e-mail address is not valid.")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    # had to alter this so that it used the right collection
    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())


    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email': email}))

    def get_alerts(self):
        print('hello from get_alerts, email value is: ', self.email)
        return Alert.find_by_user_email(self.email)


if __name__ == '__main__':
    Database.initialize()
    # def __init__(self, email, password, _id=None):
    user_one = User("test5@test.com", "$pbkdf2-sha256$7665$WKs1ZkwJ4ZxT6t07R0iplQ$ZKfMMAMzKxH64g.3XwaFONAlVwoZf76dWdqW6uSlQtE")
    # user_one.json()
    user_one.save_to_db()

