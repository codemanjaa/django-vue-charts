from django.db.models import Count
from rest_framework import viewsets
from .models import Group
from .models import User
from .serializers import GroupSerializer
from .serializers import UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def GroupListViewSet(self):

    return self.User.objects.objects.values('gender').annotate(Count('id')).filter(gid=1)
       # queryset =  User.objects.values('gender').annotate(Count('id')).filter(gid=1)

