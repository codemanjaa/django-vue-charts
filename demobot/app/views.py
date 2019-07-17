from django.contrib.auth.models import Group
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import GroupSerializer, UserSerializer, GroupStatSerializer, GroupTestSerializer, \
  GroupGadgetSerializer, DataSerializer
from rest_framework.response import Response
from .models import Group, User, Data
from rest_framework import viewsets


# Create your views here.
# class GroupViewSet(viewsets.ViewSet):

# class GroupViewSet(APIView):

#    """A viewset for listing or retriving Groups"""
#    def get(self, request):
#       queryset = Group.objects.all()
#        serializer = GroupSerializer(queryset, many=True)
#        return Response(serializer.data)

#    def retrieve(self, request, pk=None):
#        queryset = Group.objects.all()
#        group = get_object_or_404(queryset, pk=pk)
#        serializer = GroupSerializer(group)
#        return Response(serializer.data)


######################################

class GroupViewSet(viewsets.ModelViewSet):
  queryset = Group.objects.all()
  serializer_class = GroupSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        gid = self.request.query_params.get('gid')
        if (gid == "all"):
          gid = 'all'

          users = User.objects.all()

          return users

        elif (gid != None):
            users = User.objects.filter(gid=gid)
            return users


class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer


class GroupStatView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = GroupStatSerializer

    def get_queryset(self):

      #User.objects.values('gid').annotate(Count('id'))
      total_user = User.objects.values('gid').annotate(total_user=Count('id'))
      total_males = User.objects.filter()
      result =  User.objects.values('gender','gid').annotate(total_user=Count('id'))
      return result


## Get the Group stats based on the request parameter

class GroupStatTest(viewsets.ReadOnlyModelViewSet):
  queryset = User.objects.all()
  serializer_class = GroupTestSerializer

  def get_queryset(self):



    # gid = '1' #self.request.query_params.get('gid')
    # total_user = User.objects.filter(gid=gid).count()
    # total_men = User.objects.filter(gender__startswith='SEX_M', gid=gid).count()
    # total_women = User.objects.filter(gender__startswith='SEX_W', gid=gid).count()
    # #total_user = User.objects.values('gid').annotate(total_user=Count('id'))
     return ("")
     #return result

"""Dashboard gadget contains the info about the group state, 
   total user, males, females
"""


class GroupGadgetView(APIView):

    def get(self, request):

        gid = self.request.query_params.get('gid')

        if (gid == "all"):
          gid = 'all'
          state = 'NA'
          total_user = User.objects.all().count()
          total_men = User.objects.filter(gender__startswith='SEX_M').count()
          total_women = User.objects.filter(gender__startswith='SEX_W').count()
          return Response({'gid': gid, 'state': state, 'total_user': total_user, 'total_men': total_men,
                           'total_women': total_women})

        if(gid!=None):
            state = Group.objects.filter(id=gid).values('state').first()
            stat = state['state']
            total_user = User.objects.filter(gid=gid).count()
            total_men = User.objects.filter(gender__startswith='SEX_M', gid=gid).count()
            total_women = User.objects.filter(gender__startswith='SEX_W', gid=gid).count()
            return Response({'gid':gid,'state':stat, 'total_user':total_user, 'total_men':total_men,'total_women':total_women})


        else:
             return Response({'gid': 'NA', 'state': 'NA', 'total_user': 0, 'total_men': 0,
                              'total_women': 0})


class GroupUserView(APIView):

    def get(self, request):
      gid = self.request.query_params.get('gid')

      if(gid=='undefined'):
        return Response('None')
      if(gid!=None):
        groupuserlist = User.objects.filter(gid=gid).values()
        return Response({groupuserlist})
      else:
        return Response('None')







