from rest_framework import serializers
from .models import Group
from .models import User, Data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        #fields = ('first_name', 'last_name','gender','facebook_id','last_interaction','state','gid')


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'

class GroupStatSerializer(serializers.ModelSerializer):
    gid = serializers.CharField(max_length=32)
    gender = serializers.CharField(max_length=255)
    total_user = serializers.IntegerField()


    class Meta:
        model = Group
        fields = ('gid','total_user','gender')


class GroupTestSerializer(serializers.ModelSerializer):
  #gid = serializers.CharField(max_length=32)
  total_user = serializers.IntegerField()
  total_men = serializers.IntegerField()
  total_women = serializers.IntegerField()

  class Meta:
    model = Group
    fields = ('total_user', 'total_men', 'total_women')

# class GroupTestSerializer(serializers.ModelSerializer):
# #     """Group stat data for the widget"""
#     gid = serializers.CharField(max_length=32)
#     total = serializers.IntegerField()
#     #total_males  = serializers.IntegerField()
#     #total_females = serializers.IntegerField()
#
#     class Meta:
#         model = Group
#         fields = ('gid','total')
#
# #
#

class GroupGadgetSerializer(serializers.Serializer):
    gid = serializers.CharField(max_length=32)
    total_user = serializers.IntegerField()
    total_men = serializers.IntegerField()
    total_women = serializers.IntegerField()

    def __int__(self, gid, total_user, total_men, total_women):
        self.gid = gid
        self.total_user = total_user
        self.total_men = total_men
        self.total_women = total_women

