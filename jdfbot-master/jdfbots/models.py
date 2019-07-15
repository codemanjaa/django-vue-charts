# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""Models."""

import uuid

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from logzero import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.types import TypeDecorator, TypeEngine, CHAR
from sqlalchemy.dialects.postgresql import UUID


DB = SQLAlchemy()
MIGRATE = Migrate(db=DB)


# pylint: disable=abstract-method
class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """

    impl = TypeEngine

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        elif not isinstance(value, uuid.UUID):
            return "{:32x}".format(uuid.UUID(value).int)  # pylint: disable=no-member
        return "{:32x}".format(value.int)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(value)


class Config(DB.Model):
    """Configurations parameters."""

    key = DB.Column(DB.String(255), primary_key=True)
    value = DB.Column(DB.String(255))

    @staticmethod
    def get(key, default=None):
        """Return the configuration value associated to a key."""
        conf = Config.query.get(key)
        if conf:
            return conf.value
        return default

    @staticmethod
    def set(key, value):
        """Set a configuration key-value pair."""
        conf = Config.query.get(key)
        if conf:
            conf.value = value
        else:
            conf = Config(key=key, value=value)
            DB.session.add(conf)
        DB.session.commit()


class User(DB.Model):
    """An user of the bots."""

    id = DB.Column(GUID(), default=uuid.uuid4, primary_key=True, autoincrement=False)
    first_name = DB.Column(DB.String(255), nullable=False)
    last_name = DB.Column(DB.String(255), nullable=False)
    gender = DB.Column(DB.String(255), nullable=False)
    locale = DB.Column(DB.String(255), nullable=False)
    timezone = DB.Column(DB.String(255), nullable=False)
    facebook_id = DB.Column(DB.BigInteger, unique=True, nullable=False)
    last_interaction = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)
    state = DB.Column(DB.String(255), nullable=True, default="language.Start")
    language = DB.Column(DB.String(3))
    gid = DB.Column(
        GUID(), DB.ForeignKey("group.id"), nullable=False)

    @staticmethod
    def get_or_create_facebook_user(page, facebook_id):
        """
        Get or create the user.

        Create the user in the database if it does not exist yet.
        """
        user = User.query.filter_by(facebook_id=facebook_id).first()
        if user is None:
            # Get user information
            profile = page.get_user_profile(facebook_id)
            # Create user
            user = User(
                first_name=profile.get("first_name", ""),
                last_name=profile.get("last_name", ""),
                gender=profile.get("gender", "NA"),
                locale=profile.get("locale", ""),
                timezone=profile.get("timezone", ""),
                facebook_id=profile.get("id", ""),
            )
            # Save user in database
            try:
                DB.session.add(user)
                DB.session.commit()
                logger.info(f"User created: {user.id}")
            except SQLAlchemyError as error:
                logger.info(f"Failed to create user in the database")
                logger.exception(error)
        return user

    def save(self):
        """Save the user to the database."""
        try:
            DB.session.add(self)
            DB.session.commit()
        except SQLAlchemyError as error:
            logger.error("Failed to write user to the database")
            logger.exception(error)


class Log(DB.Model):
    """A log entry of an interaction with the bot."""

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    user = DB.Column(
        GUID(), DB.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    direction = DB.Column(DB.String(1))
    message = DB.Column(DB.Text, nullable=True)
    time = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)

    @staticmethod
    def log_message(user, message, direction="F"):
        """Log a message to the database."""
        time = datetime.utcnow()
        log = Log(user=user.id, direction=direction, message=message, time=time)
        try:
            DB.session.add(log)
            DB.session.query(User).get(user.id).last_interaction = time
            DB.session.commit()
        except SQLAlchemyError as error:
            logger.error("Failed to write the message log to the database")
            logger.exception(error)


class Data(DB.Model):
    """The data stored by the bots."""

    user = DB.Column(
        GUID(), DB.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    clz = DB.Column(DB.String(255), primary_key=True)
    value = DB.Column(DB.Text)


class Group(DB.Model):
    """The group data to the database."""

    id = DB.Column(GUID(), default=uuid.uuid4, primary_key=True, autoincrement=False)
    name = DB.Column(DB.String(255), nullable=False)
    state = DB.Column(DB.String(255), nullable=True, default="recruitment.Start")
    created_at = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)

