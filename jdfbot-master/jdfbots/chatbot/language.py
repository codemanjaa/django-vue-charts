# -*- coding: utf-8 -*-
"""Configuration chatbot."""

from logzero import logger
from sqlalchemy.exc import SQLAlchemyError

from jdfbots.chatbot import State, Transition
from jdfbots.models import DB, User


class Start(State):
    """Start state."""

    @classmethod
    def on_enter(cls, page, user, prev):
        return cls.on_event(page, user, None)

    @classmethod
    def on_event(cls, page, user, event):
        return Transition.MOVE("language.Language")


class Language(State):
    """Start state."""

    buttons = [
        {"title": "Français", "payload": "LANG_FRENCH"},
        {"title": "Deutsch", "payload": "LANG_GERMAN"},
    ]

    @classmethod
    def on_enter(cls, page, user, prev):
        page.send(
            user.facebook_id,
            "Quelle langue parlez-vous?\nWelche Sprache sprichst du?",
            quick_replies=cls.buttons,
        )
        return Transition.STAY

    @classmethod
    def on_event(cls, page, user, event):
        # Get the response
        response = event.quick_reply_payload
        # If the answer is not valid
        if response not in [b["payload"] for b in cls.buttons]:
            page.send(
                user.facebook_id,
                "Merci de répondre en utilisant les boutons.\nBitte antworte mithilfe der Buttons.",
                quick_replies=cls.buttons,
            )
            return Transition.STAY
        user = User.get_or_create_facebook_user(page, user.facebook_id)
        if response == "LANG_FRENCH":
            user.language = "fr"
        elif response == "LANG_GERMAN":
            user.language = "de"
        try:
            DB.session.add(user)
            DB.session.commit()
        except SQLAlchemyError as error:
            logger.error("Failed to write user state to the database")
            logger.exception(error)
        return Transition.MOVE("recruitment.Start")
