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
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
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
        managed = False
        db_table = 'data'
        unique_together = (('user', 'clz'), )


