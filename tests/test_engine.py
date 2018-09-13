from unittest import main

from opyncorporates import create_engine
from opyncorporates.versions import Version04
from .base import BaseTestCase


class TestEngine(BaseTestCase):

    def test_engine(self):
        engine = create_engine(api_version=self.api_version,
                               api_token=self.api_token)
        self.assertIsInstance(engine, Version04)