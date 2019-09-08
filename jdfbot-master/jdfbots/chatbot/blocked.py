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
