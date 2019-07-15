# -*- coding: utf-8 -*-
"""Test Facebook integration of jdfbots."""

import os

from tests import AppTestCase


class FacebookTests(AppTestCase):

    """Test Facebook integration."""

    def test_correct_subscription(self):
        """Test Facebook correct subscription."""
        # Set a temporary JDF_VERIFY_TOKEN
        token = "XXXABCDEXXX"
        challenge = "XXXZYWXXXX"
        os.environ['JDF_VERIFY_TOKEN'] = token
        # Create a correct subscription URL
        url = ("facebook?hub.mode=subscribe&"
               "hub.verify_token={}&"
               "hub.challenge={}".format(token, challenge))
        # Try to subscribe
        result = self.app.get(url)
        assert result.data.decode('ASCII') == challenge

    def test_wrong_subscription(self):
        """Test Facebook wrong subscription."""
        # Set a temporary JDF_VERIFY_TOKEN
        token = "XXXABCDEXXX"
        challenge = "XXXZYWXXXX"
        os.environ['JDF_VERIFY_TOKEN'] = token
        # Create a wrong subscription URL
        url = ("facebook?hub.mode=subscribe&"
               "hub.verify_token=WRONG_{}&"
               "hub.challenge={}".format(token, challenge))
        # Try to subscribe
        result = self.app.get(url)
        assert result.data.decode('ASCII') != challenge
        assert result.data.decode('ASCII') == "failed"
