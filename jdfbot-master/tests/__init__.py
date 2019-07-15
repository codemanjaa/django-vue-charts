# -*- coding: utf-8 -*-
"""«J'arrête de Fumer» bots tests."""

import unittest

from logzero import logger

from jdfbots import APP

logger.disabled = True


class AppTestCase(unittest.TestCase):

    """Test case for the JDF Flask application."""

    def setUp(self):
        self.app = APP.test_client()
        self.app.testing = True
