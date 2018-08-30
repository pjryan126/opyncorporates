import os
from unittest import main, TestCase


class BaseTestCase(TestCase):

    def setUp(self):
        self.api_token = os.environ.get('OC_API_TOKEN', None)
        self.api_version = os.environ.get('OC_API_VERSION', '0.4')

    def tearDown(self):
        self.api_token = None
        self.api_version = None

if __name__ == '__main__':
    main()