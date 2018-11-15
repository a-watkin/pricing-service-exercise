from passlib.hash import pbkdf2_sha512
import re


class Utils(object):

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512

        :param password: The sha512 passwrod from the login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """

        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks the password the user sent matches that of the database.
        The database password is encrypted more than the user's password at this stage.

        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if the passwords match, false otherwise
        """

        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def email_is_valid(email):
        # pycharm has a build in regular expression checker, pretty cool (click the light bulb)
        # using a regular expression check the email is valid
        email_address_matcher = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        return True if email_address_matcher else False


if __name__ == '__main__':
    blah = Utils()
    print(blah.hash_password("hello"))
