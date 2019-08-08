import uuid
from django.db import models
from datetime import datetime


# Create your models here.

#
# # class Group(models.Model):
# #     """Group model """
# #
# #     id = models.CharField(max_length=32, null=False, primary_key=True)
# #     name = models.CharField(max_length=255, null=True)
# #     state = models.CharField(max_length=255, null=False, default="recruitment")
# #     created_date = models.DateTimeField(default=datetime.utcnow)
# #
# #     class Meta:
# #       db_table = 'group'
#
#     def __str__(self):
#         return self.name
from rest_framework.fields import JSONField


class Group(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(null= True)

    class Meta:
        app_label = 'app'
        managed = True
        db_table = 'group'


class User(models.Model):
    """User model for the bots"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    gender = models.CharField(max_length=255, null=False)
    facebook_id = models.BigIntegerField(unique=True, null=False)
    last_interaction = models.DateTimeField(null=False, default=datetime.utcnow)
    state = models.CharField(max_length=255, default="language.Start")
    language = models.CharField(max_length=3, null=True)
    gid = models.ForeignKey(Group, models.DO_NOTHING, db_column='gid')

    class Meta:
      app_label = 'app'
      managed = False
      db_table = 'user'

    def __str__(self):
        return self.first_name


class Data(models.Model):
    #user = models.ForeignKey('User', models.DO_NOTHING, db_column='user')
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User',models.DO_NOTHING, db_column='user')
    clz = models.CharField(max_length=255)
    value = models.TextField(blank=True, null=True)
    #value = JSONField()

    class Meta:
      app_label = 'app'
      managed = False
      db_table = 'data'
      unique_together = (('user', 'clz'), )


class AuthRouter:
  """
  A router to control all database operations on models in the
  auth application.
  """

  def db_for_read(self, model, **hints):
    """
    Attempts to read auth models go to auth_db.
    """
    if model._meta.app_label == 'auth':
      return 'default'
    return None

  def db_for_write(self, model, **hints):
    """
    Attempts to write auth models go to auth_db.
    """
    if model._meta.app_label == 'auth':
      return 'default'
    return None

  def allow_relation(self, obj1, obj2, **hints):
    """
    Allow relations if a model in the auth app is involved.
    """
    if obj1._meta.app_label == 'auth' or \
      obj2._meta.app_label == 'auth':
      return True
    return None

  def allow_migrate(self, db, app_label, model_name=None, **hints):
    """
    Make sure the auth app only appears in the 'auth_db'
    database.
    """
    if app_label == 'auth':
      return db == 'default'
    return None

class PrimaryRouter():
  """
  A router to control all database operations on models in the
  auth application.
  """

  def db_for_read(self, model, **hints):
    """
    Attempts to read auth models go to auth_db.
    """
    if model._meta.app_label == 'app':
      return 'jdf_db'
    return None

  def db_for_write(self, model, **hints):
    """
    Attempts to write auth models go to auth_db.
    """
    if model._meta.app_label == 'app':
      return 'jdf_db'
    return None

  def allow_relation(self, obj1, obj2, **hints):
    """
    Allow relations if a model in the auth app is involved.
    """
    if obj1._meta.app_label == 'app' or \
      obj2._meta.app_label == 'app':
      return True
    return None

  def allow_migrate(self, db, app_label, model_name=None, **hints):
    """
    Make sure the auth app only appears in the 'auth_db'
    database.
    """

    if app_label == 'app':
      return db == 'jdf_db'
    return None



