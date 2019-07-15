# -*- coding: utf-8 -*-
"""Helper classes for chatbot."""

from jdfbots.chatbot import State, Transition
from jdfbots.i18n import translate, translate_buttons


class MultipleChoice(State):
    """Multiple choice question."""

    name = None
    question = None
    buttons = None
    next = None

    @classmethod
    def on_enter(cls, page, user, prev):
        page.send(
            user.facebook_id,
            translate(cls.question, lang=user.language),
            quick_replies=translate_buttons(cls.buttons, lang=user.language),
        )
        return Transition.STAY

    @classmethod
    def on_event(cls, page, user, event):
        """Run code when an event occurs."""
        # Get the response
        response = event.quick_reply_payload
        # If the answer is not valid
        if response not in [b["payload"] for b in cls.buttons]:
            page.send(
                user.facebook_id,
                translate(
                    "Merci de répondre en utilisant les boutons", lang=user.language
                ),
                quick_replies=translate_buttons(cls.buttons, lang=user.language),
            )
            return Transition.STAY
        # Save it
        with cls.storage(user) as s:
            s[cls.name] = response
        # Move to next question
        # pylint: disable=not-callable
        move_to = cls.next(response) if callable(cls.next) else cls.next
        return Transition.MOVE(move_to)


class MultipleChoiceAccumulate(State):
    """Multiple choice question that are accumulated."""

    group = None
    name = None
    question = None
    buttons = None
    next = None

    @classmethod
    def on_enter(cls, page, user, prev):
        page.send(
            user.facebook_id,
            translate(cls.question, lang=user.language),
            quick_replies=translate_buttons(cls.buttons, lang=user.language),
        )
        return Transition.STAY

    @classmethod
    def on_event(cls, page, user, event):
        """Run code when an event occurs."""
        # Get the response
        response = event.quick_reply_payload
        # If the answer is not valid
        if response not in [b["payload"] for b in cls.buttons]:
            page.send(
                user.facebook_id,
                translate(
                    "Merci de répondre en utilisant les boutons", lang=user.language
                ),
                quick_replies=translate_buttons(cls.buttons, lang=user.language),
            )
            return Transition.STAY
        # Save it
        with cls.storage(user) as s:
            s[cls.group][-1][cls.name] = response
        # Move to next question
        # pylint: disable=not-callable
        move_to = cls.next(response) if callable(cls.next) else cls.next
        return Transition.MOVE(move_to)
