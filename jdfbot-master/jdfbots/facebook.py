# -*- coding: utf-8 -*-
"""Server for facebook."""

import json
import os
from functools import partial

from fbmq import Page
from flask import Blueprint, request
from logzero import logger

from jdfbots.chatbot import handle_event
from jdfbots.models import Config, Log, User

# Flask blueprint
BP = Blueprint("jdfbots", __name__)

# FB pages
PAGES = dict()


def load_pages():
    """Load facebook pages objects."""
    credentials_env = os.environ.get("JDF_PAGE_TOKENS", "")
    credentials = credentials_env.split(";")
    for credential in credentials:
        page_id, token = credential.split(":", 1)
        load_page(page_id, token)


def load_page(page_id, token):
    """Load a facebook page object."""
    PAGES[page_id] = Page(token, message=facebook_message_handler)


@BP.route("", methods=["GET"])
def facebook_validate():
    """Validate facebook subscription."""
    if (
        request.args.get("hub.mode", "") == "subscribe"
        and request.args.get("hub.verify_token", "") == os.environ["JDF_VERIFY_TOKEN"]
    ):
        logger.info("Facebook validation succeed")
        return request.args.get("hub.challenge", "")
    logger.warning("Facebook validation failed")
    return "failed"


@BP.route("", methods=["POST"])
def facebook_webhook():
    """Facebook webhook."""
    logger.info("Facebook webhook called")
    data = json.loads(request.get_data())
    page_id = data["entry"][0]["id"]
    page = PAGES[page_id]
    message_handler = partial(facebook_message_handler, page=page)
    postback_handler = partial(facebook_message_handler, page=page)
    page.handle_webhook(
        request.get_data(as_text=True),
        message=message_handler,
        postback=postback_handler,
    )
    return "ok"


def facebook_handle_maintenance(page, event):
    """Handle maintenance mode by answering a message if needed.

    Return True if the server is in maintenance mode, False otherwise.
    """
    # If the platform is in maintenance mode, inform the user about this
    if Config.get("MAINTENANCE", "False").lower() == "true":
        page.send(
            event.sender_id,
            "Le bot est en maintenance, merci " "de réessayer plus tard.",
        )
        return True
    return False


def facebook_message_handler(event, page=None):
    """Handle facebook messages."""
    user = User.get_or_create_facebook_user(page, event.sender_id)
    if "message_text" in dir(event):
        Log.log_message(user, event.message_text)
        logger.info(f"Message received from facebook user {user.id}")
    elif "postback" in dir(event):
        Log.log_message(user, f"POSTBACK: {event.postback['payload']}")
        logger.info(f"Postback received from facebook user {user.id}")
    if not facebook_handle_maintenance(page, event):
        handle_event(page, user, event)


def facebook_postback_handler(event, page=None):
    """Handle facebook postbacks."""
    # For now only deal with GET_STARTED postback
    if event.postback["payload"] != "GET_STARTED":
        # pylint: disable=deprecated-method
        logger.warn(f"Postback {event.postback['payload']} not supported")
        return
    user = User.get_or_create_facebook_user(page, event.sender_id)
    Log.log_message(user, f"POSTBACK: {event.postback['payload']}")
    logger.info(
        f"Postback {event.postback['payload']} received " f"from user {user.id}"
    )
    if not facebook_handle_maintenance(page, event):
        handle_event(page, user, event)


# Load pages
load_pages()
