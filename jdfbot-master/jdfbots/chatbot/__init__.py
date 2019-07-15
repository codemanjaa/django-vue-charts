# -*- coding: utf-8 -*-
"""Chatbot."""

import json

from enum import Enum
from importlib import import_module

from logzero import logger
from sqlalchemy.exc import SQLAlchemyError

from jdfbots.models import DB, Data


# pylint: disable=too-few-public-methods
class Storage():
    """Storage for a state."""

    def __init__(self, clz, user):
        self._clz = clz
        self._user = user
        self._data = None
        self._json = None

    def __enter__(self):
        data = Data.query.filter_by(user=self._user.id, clz=self._clz).first()
        if data:
            self._data = data
            self._json = json.loads(self._data.value)
        else:
            self._data = Data(user=self._user.id, clz=self._clz)
            self._json = json.loads("{}")
        return self._json

    def __exit__(self, *args):
        self._data.value = json.dumps(self._json)
        try:
            DB.session.add(self._data)
            DB.session.commit()
        except SQLAlchemyError as error:
            logger.error('Failed to write storage data to the database')
            logger.exception(error)


class State():
    """State of a finite state machine."""

    @classmethod
    def storage(cls, user):
        """Return a Storage object for a given class and user."""
        return Storage(modulename(cls), user)

    @classmethod
    def on_enter(cls, page, user, prev):
        """Run code when the state is entered."""
        pass

    @classmethod
    def on_event(cls, page, user, event):
        """Run code when an event occurs."""
        pass


class Transition(Enum):
    """State transition in a finite state machine."""
    STAY = 0
    MOVE = 1

    def __init__(self, _):
        super().__init__()
        if self.name == 'MOVE':
            self.state = None

    def __call__(self, *args):
        if self == Transition.MOVE:
            if len(args) != 1:
                raise RuntimeError('MOVE enum requires the next '
                                   'state as argument')
            self.state = args[0]
        return self


def fullname(clz):
    """Return the full name of a python class."""
    return clz.__module__ + "." + clz.__name__


def modulename(clz):
    """Return the module name of a python class."""
    return clz.__module__


def load(classname):
    """Load a class from its name."""
    mod, clz = classname.rsplit('.', 1)
    if not mod.startswith('jdfbots.'):
        mod = 'jdfbots.chatbot.' + mod
    module = import_module(mod)
    return getattr(module, clz)


class SurveyHook(State):
    """Hook for the survey."""

    @classmethod
    def hook(cls, user):
        """Hook for the survey."""
        with Storage("jdfbots.chatbot.survey", user) as s:
            # If survey already started, skip it
            if 'survey_started' in s and s['survey_started']:
                return
            # Else, survey not started, start it
            s['survey_started'] = True
            s['previous_state'] = user.state
            user.state = 'survey.Start'
            user.save()


def handle_event(page, user, event):
    """Handle an event comming from an user."""
    # SurveyHook.hook(user)
    if not user.state:
        return
    state = load(user.state)
    tran = state.on_event(page, user, event)
    while tran != Transition.STAY:
        if tran is None or tran.state is None:
            user.state = None
            break
        old = state
        state = load(tran.state)
        tran = state.on_enter(page, user, fullname(old))
        user.state = fullname(state)
    try:
        DB.session.add(user)
        DB.session.commit()
    except SQLAlchemyError as error:
        logger.error('Failed to write user state to the database')
        logger.exception(error)
