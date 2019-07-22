from django.contrib.auth.models import Group
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.utils import json
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


class GroupChartView(APIView):

    def get(self, request):

        queryset = Data.objects.filter(clz='jdfbots.chatbot.tracker').values(
        'value')
        list_size = len(queryset)
        if(list_size==1):
            jsondata = queryset.first()
        elif(list_size > 1):
          #jdata = queryset.first()
          queryset = Data.objects.filter(clz='jdfbots.chatbot.tracker').values(
            'value').first()
          result = []
          # for value in queryset:
          #      cigarettes = value['cigerettes']
          #      for cigars in cigarettes:
          #          result = dict()
          data = queryset['value']
          jsondata = json.loads(data)
          cigars = jsondata['cigarettes']
          return Response(cigars)


class UserProfileView(APIView):

    def get(self, request):
        totalcigars=0
        desirelow = 0
        desirenone=0
        desiremedium=0
        desirehigh=0
        desireextreme=0


        moodstressed = 0
        moodtired = 0
        moodneutral = 0
        moodangry = 0
        moodworried = 0
        moodsad = 0
        moodhappy = 0
        moodrelaxed = 0
        moodbored = 0

        aloneyes = 0
        aloneno = 0

        drivingyes = 0
        drivingno = 0

        contextprive = 0
        contextprof = 0


        id = self.request.query_params.get('id')
        queryset = Data.objects.filter(user='f788476143e945f0a729c05294210604', clz='jdfbots.chatbot.tracker').values(
          'value').first()
        # queryset = Data.objects.filter(user=id,  clz='jdfbots.chatbot.tracker').values(
        #   'value')
        data = queryset['value']
        jsondata = json.loads(data)
        cigars = jsondata['cigarettes']
        totalcigars = len(cigars)

        # Calculate the desire low numbers
# Desire
        for element in cigars:
           option=element['desire']
           if(option=='DESIRE_LOW'):
             desirelow = desirelow + 1
           elif(option=='DESIRE_NONE'):
             desirenone = desirenone +1
           elif (option == 'DESIRE_MEDIUM'):
             desiremedium = desiremedium + 1
           elif(option== 'DESIRE_HIGH'):
             desirehigh = desirehigh+1
           else:
             desireextreme= desireextreme+1


        # desirechartdata  = {"desirechart":[{
        #   'desirelow': desirelow,
        #   'desirenone': desirenone,
        #   'desiremedium': desiremedium,
        #   'desirehigh': desirehigh,
        #   'desireextreme': desireextreme
        #
        # }]}
        # desirechartobject = json.loads(desirechartdata)


# Mood
        for element in cigars:
           option=element['mood']
           if(option=='MOOD_STRESSED'):
             moodstressed = moodstressed + 1
           elif(option=='MOOD_TIRED'):
             moodtired = moodtired +1
           elif (option == 'MOOD_NEUTRAL'):
             moodneutral = moodneutral + 1
           elif(option== 'MOOD_WORRIED'):
             moodworried = moodworried+1
           elif(option=='MOOD_ANGRY'):
             moodangry = moodangry +1
           elif(option=='MOOD_SAD'):
             moodsad = moodsad +1
           elif(option=='MOOD_HAPPY'):
             moodhappy = moodhappy + 1
           elif(option=='MOOD_RELAXED'):
             moodrelaxed = moodrelaxed + 1
           else:
             moodbored= moodbored+1


# Driving
        for element in cigars:
            option = element['driving']
            if(option == 'DRIVING_NO'):
                drivingno = drivingno + 1
            else:
                drivingyes = drivingyes + 1


#Context
        for element in cigars:
          option = element['context']
          if(option == 'CONTEXT_PRIVE'):
              contextprive = contextprive + 1
          else:
              contextprof = contextprof + 1
#Alone
        for element in cigars:
          option = element['alone']
          if(option=='ALONE_YES'):
            aloneyes = aloneyes +1
          else:
            aloneno = aloneno + 1

          chartdata =  {
        'labels': ['ALONE_YES', 'ALONE_NO'],
        'datasets': [{
            'label': 'ALONE',
            'data': [aloneyes, aloneno],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',

            ],
            'borderColor': [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',

            ],
            'borderWidth': 1
        }]
    }



       # return Response({'chartdata':chartdata})
        return Response({'totalcigars':totalcigars, 'desirelow':desirelow, 'desirenone':desirenone,
                         'desiremedium':desiremedium, 'desirehigh':desirehigh, 'desireextreme':desireextreme})











