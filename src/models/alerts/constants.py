import os

MAILGUN_URL = os.environ.get('MAILGUN_URL')
# need to hide this
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')


ALERT_TIMEOUT = 10  # minutes
COLLECTION = "alerts"

# SMPT
SMPT_URL = 'smtp.mailgun.org'
SMPT_PORT = 587
# need to hide this also
MAILGUN_SMPT_KEY = os.environ.get('MAILGUN_SMPT_KEY')
FROM = "postmaster@sandbox91bd6a354579468a831004f9df273bcf.mailgun.org"

TEST_EMAIL = 'atomicpenguines@gmail.com'
