from django.contrib.auth import user_logged_out, logout

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
from rest_framework import viewsets, generics
from django.contrib.auth.decorators import login_required


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


class UserSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer




class GroupView(viewsets.ModelViewSet):
  queryset = Group.objects.all()
  serializer_class = GroupSerializer

  def get_queryset(self):
    id = self.request.query_params.get('id')
    if (id != None):
      group = Group.objects.filter(id=id)
      return group
    else:
      group = Group.objects.all()
      return group


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


class UserDetailViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def get_queryset(self):
    id = self.request.query_params.get('id')
    if(id != None):
      user = User.objects.filter(id=id)
      return user
    else:
      return None


class DataViewSet(viewsets.ModelViewSet):
  queryset = Data.objects.all()
  serializer_class = DataSerializer


class GroupStatView(viewsets.ReadOnlyModelViewSet):
  queryset = User.objects.all()
  serializer_class = GroupStatSerializer

  def get_queryset(self):
    # User.objects.values('gid').annotate(Count('id'))
    total_user = User.objects.values('gid').annotate(total_user=Count('id'))
    total_males = User.objects.filter()
    result = User.objects.values('gender', 'gid').annotate(total_user=Count('id'))
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
  # return result


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

    if (gid != None):
      state = Group.objects.filter(id=gid).values('state').first()
      stat = state['state']
      total_user = User.objects.filter(gid=gid).count()
      total_men = User.objects.filter(gender__startswith='SEX_M', gid=gid).count()
      total_women = User.objects.filter(gender__startswith='SEX_W', gid=gid).count()
      return Response(
        {'gid': gid, 'state': stat, 'total_user': total_user, 'total_men': total_men, 'total_women': total_women})


    else:
      return Response({'gid': 'NA', 'state': 'NA', 'total_user': 0, 'total_men': 0,
                       'total_women': 0})


class GroupUserView(APIView):

  def get(self, request):
    gid = self.request.query_params.get('gid')

    if (gid == 'undefined'):
      return Response('None')
    if (gid != None):
      groupuserlist = User.objects.filter(gid=gid).values()
      return Response({groupuserlist})
    else:
      return Response('None')


class GroupChartView(APIView):

  def get(self, request):

    queryset = Data.objects.filter(clz='jdfbots.chatbot.tracker').values(
      'value')
    list_size = len(queryset)
    if (list_size == 1):
      jsondata = queryset.first()
    elif (list_size > 1):
      # jdata = queryset.first()
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
    totalcigars = 0
    desirelow = 0
    desirenone = 0
    desiremedium = 0
    desirehigh = 0
    desireextreme = 0



    aloneyes = 0
    aloneno = 0

    drivingyes = 0
    drivingno = 0

    contextprive = 0
    contextprof = 0

    id = self.request.query_params.get('id')
    users = User.objects.filter(gid=id)
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
      # labels.append(element['desire'])
      option = element['desire']
      if (option == 'DESIRE_LOW'):
        desirelow = desirelow + 1
      elif (option == 'DESIRE_NONE'):
        desirenone = desirenone + 1
      elif (option == 'DESIRE_MEDIUM'):
        desiremedium = desiremedium + 1
      elif (option == 'DESIRE_HIGH'):
        desirehigh = desirehigh + 1
      else:
        desireextreme = desireextreme + 1

    # desirechartdata  = {"desirechart":[{
    #   'desirelow': desirelow,
    #   'desirenone': desirenone,
    #   'desiremedium': desiremedium,
    #   'desirehigh': desirehigh,
    #   'desireextreme': desireextreme
    #
    # }]}
    # desirechartobject = json.loads(desirechartdata)


    # Driving
    for element in cigars:
      option = element['driving']
      if (option == 'DRIVING_NO'):
        drivingno = drivingno + 1
      else:
        drivingyes = drivingyes + 1

    # Context
    for element in cigars:
      option = element['context']
      if (option == 'CONTEXT_PRIVE'):
        contextprive = contextprive + 1
      else:
        contextprof = contextprof + 1
    # Alone
    for element in cigars:
      option = element['alone']
      if (option == 'ALONE_YES'):
        aloneyes = aloneyes + 1
      else:
        aloneno = aloneno + 1

      labels = ['DESIRE_NONE', 'DESIRE_LOW', 'DESIRE_MEDIUM', 'DESIRE_HIGH', 'DESIRE_EXTREME']
    chartData = {
      'labels': ['None', 'Low', 'Medium', 'High', 'Extreme'],
      'datasets': [{
        'label': 'Desire Behavior',
        'data': [desirenone, desirelow, desiremedium, desirehigh, desireextreme],
        'backgroundColor': [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)'
        ],
        'borderColor': [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)'
        ]

      }]}

    return Response(chartData)

    # data = {
    #   "labels": ['ALONE_YES', 'ALONE_NO'],
    #   "datasets": [{
    #     'label': 'ALONE',
    #     'data': [aloneyes, aloneno],
    #     'backgroundColor': [
    #       'rgba(255, 99, 132, 0.2)',
    #       'rgba(54, 162, 235, 0.2)',
    #
    #     ],
    #     'borderColor': [
    #       'rgba(255, 99, 132, 1)',
    #       'rgba(54, 162, 235, 1)',
    #       'rgba(255, 206, 86, 1)',
    #
    #     ],
    #     'borderWidth': 1
    #   }]
    # }

  # return Response({'totalcigars': totalcigars, 'desirelow': desirelow, 'desirenone': desirenone,
  #                  'desiremedium': desiremedium, 'desirehigh': desirehigh, 'desireextreme': desireextreme})


class UserChartDataView(APIView):

  def get(self, request, format=None):
    id = self.request.query_params.get('id')
    queryset = Data.objects.filter(user='a788476143e945f0a729c05294210604', clz='jdfbots.chatbot.tracker').values(
      'value').first()
    # queryset = Data.objects.filter(user=id,  clz='jdfbots.chatbot.tracker').values(
    #   'value')
    data = queryset['value']
    jsondata = json.loads(data)
    cigars = jsondata['cigarettes']
    totalcigars = len(cigars)

    labels = ['Total Cigars']
    data = {
      "labels": labels,
      "totalcigars": totalcigars
    }
    return Response(data)


class GenderPieView(APIView):

  def get(self, request):


    gid = self.request.query_params.get('gid')

    if (gid == 'undefined'):
      return Response('None')

    if (gid == "all") :
      gid = 'all'
      total_user = User.objects.all().count()
      total_men = User.objects.filter(gender__startswith='SEX_M').count()
      total_women = User.objects.filter(gender__startswith='SEX_W').count()

      genderchartData = {
        'labels': ['Men', 'Women'],
        'datasets': [
          {

            'label': 'Gender Ratio',
            'backgroundColor': ['#3a2ff8', '#ef5ef9'],
            'data': [total_men, total_women]
          }
        ],
      }

      return Response(genderchartData)

    elif (gid != None):
      state = Group.objects.filter(id=gid).values('state').first()
      stat = state['state']
      total_user = User.objects.filter(gid=gid).count()
      total_men = User.objects.filter(gender__startswith='SEX_M', gid=gid).count()
      total_women = User.objects.filter(gender__startswith='SEX_W', gid=gid).count()

      genderchartData = {
        'labels': ['Men', 'Women'],
        'datasets': [
          {
            'label': 'Gender Ratio',
            'backgroundColor': ['#3a2ff8', '#ef5ef9'],
            'data': [total_men, total_women]
          }
        ],
      }
      return Response(genderchartData)


    else:

      genderchartData = {
        'labels': ['Men', 'Women'],
        'datasets': [
          {

            'label': 'Gender Ratio',
            'backgroundColor': ['#3a2ff8', '#ef5ef9'],
            'data': [50, 50]
          }
        ],
      }
      return Response(genderchartData)

### Group Mood View

class GroupMoodView(APIView):

  def get(self, request):
    moodstressed = 0
    moodtired = 0
    moodneutral = 0
    moodangry = 0
    moodworried = 0
    moodsad = 0
    moodhappy = 0
    moodrelaxed = 0
    moodbored = 0

    id = self.request.query_params.get('id')
    if(id=='all'):
      queryset = Data.objects.filter(clz='jdfbots.chatbot.tracker').values(
        'value').first()
      # queryset = Data.objects.filter(user=id,  clz='jdfbots.chatbot.tracker').values(
      #   'value')
      data = queryset['value']
      jsondata = json.loads(data)
      cigars = jsondata['cigarettes']
      for element in cigars:
        option = element['mood']
        if (option == 'MOOD_STRESSED'):
          moodstressed = moodstressed + 1
        elif (option == 'MOOD_TIRED'):
          moodtired = moodtired + 1
        elif (option == 'MOOD_NEUTRAL'):
          moodneutral = moodneutral + 1
        elif (option == 'MOOD_WORRIED'):
          moodworried = moodworried + 1
        elif (option == 'MOOD_ANGRY'):
          moodangry = moodangry + 1
        elif (option == 'MOOD_SAD'):
          moodsad = moodsad + 1
        elif (option == 'MOOD_HAPPY'):
          moodhappy = moodhappy + 1
        elif (option == 'MOOD_RELAXED'):
          moodrelaxed = moodrelaxed + 1
        else:
          moodbored = moodbored + 1

        labels = ['MOOD_STRESSED', 'MOOD_TIRED', 'MOOD_NEUTRAL', 'MOOD_WORRIED', 'MOOD_ANGRY', 'MOOD_SAD', 'MOOD_HAPPY',
                  'MOOD_RELAXED', 'MOOD_BORED']
        moodchartData = {
          'labels': ['Stressed', 'Tired', 'Neutral', 'Worried', 'Angry', 'Sad', 'Happy', 'Relaxed', 'Bored'],
          'datasets': [{
            'label': 'Mood Behavior',
            'data': [moodstressed, moodtired, moodneutral, moodworried, moodangry, moodsad, moodhappy, moodrelaxed,
                     moodbored],
            'backgroundColor': [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(155, 192, 192, 0.2)',
              'rgba(75, 102, 255, 0.2)',
              'rgba(95, 159, 64, 0.2)'
            ],
            'borderColor': [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
              'rgba(253, 92, 92, 1)',
              'rgba(92, 102, 255, 1)',
              'rgba(55, 159, 64, 1)'
            ]

          }]}

      return Response(moodchartData)

    queryset = Data.objects.filter
    users = User.objects.filter(gid=id)
    queryset = Data.objects.filter(user='f788476143e945f0a729c05294210604', clz='jdfbots.chatbot.tracker').values(
      'value').first()
    # queryset = Data.objects.filter(user=id,  clz='jdfbots.chatbot.tracker').values(
    #   'value')
    data = queryset['value']
    jsondata = json.loads(data)
    cigars = jsondata['cigarettes']
    for element in cigars:
      option = element['mood']
      if (option == 'MOOD_STRESSED'):
        moodstressed = moodstressed + 1
      elif (option == 'MOOD_TIRED'):
        moodtired = moodtired + 1
      elif (option == 'MOOD_NEUTRAL'):
        moodneutral = moodneutral + 1
      elif (option == 'MOOD_WORRIED'):
        moodworried = moodworried + 1
      elif (option == 'MOOD_ANGRY'):
        moodangry = moodangry + 1
      elif (option == 'MOOD_SAD'):
        moodsad = moodsad + 1
      elif (option == 'MOOD_HAPPY'):
        moodhappy = moodhappy + 1
      elif (option == 'MOOD_RELAXED'):
        moodrelaxed = moodrelaxed + 1
      else:
        moodbored = moodbored + 1

      labels = ['MOOD_STRESSED', 'MOOD_TIRED', 'MOOD_NEUTRAL', 'MOOD_WORRIED', 'MOOD_ANGRY','MOOD_SAD','MOOD_HAPPY','MOOD_RELAXED','MOOD_BORED']
      moodchartData = {
        'labels': ['Stressed', 'Tired', 'Neutral', 'Worried', 'Angry','Sad','Happy', 'Relaxed','Bored'],
        'datasets': [{
          'label': 'Mood Behavior',
          'data': [moodstressed, moodtired, moodneutral, moodworried, moodangry,moodsad,moodhappy,moodrelaxed, moodbored],
          'backgroundColor': [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(155, 192, 192, 0.2)',
            'rgba(75, 102, 255, 0.2)',
            'rgba(95, 159, 64, 0.2)'
          ],
          'borderColor': [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(253, 92, 92, 1)',
            'rgba(92, 102, 255, 1)',
            'rgba(55, 159, 64, 1)'
          ]

        }]}

    return Response(moodchartData)









class GroupTotalCigarsView(APIView):
   def get(self, request):
     groupnumber = []
     totalcigars = []
     datalist = []
     total = 0
     groups = Group.objects.values_list('id', flat=True)
     groupsize = len(groups)
     groupname = Group.objects.values_list('name', flat= True)

     for idx,group in enumerate(groups):
         groupnumber.append(group)
         data = groups[idx]
         groupusers = User.objects.filter(gid=data).values('id')
         total = 0 
         for id in groupusers:
           groupusersdata = Data.objects.filter(user=id['id'], clz='jdfbots.chatbot.tracker').values(
             'value').first()

           if(groupusersdata != None):
               datalist.append(groupusersdata)
               datas = groupusersdata['value']
               jsondata = json.loads(datas)
               cigars = jsondata['cigarettes']
               scigars = len(cigars)
               total = total + scigars
         totalcigars.append(total)
         

     totalcigarschartdata = {

       'labels': groupname,
       'datasets': [{
         'label':'Total Cigars Stats',
         'data':totalcigars,
         'backgroundColor': [
         'rgba(255, 99, 132, 0.2)',
         'rgba(54, 162, 235, 0.2)',
         'rgba(255, 206, 86, 0.2)',
         'rgba(75, 192, 192, 0.2)',
         'rgba(153, 102, 255, 0.2)',
         'rgba(255, 159, 64, 0.2)'
         ],
         
         'borderColor': [    
           'rgba(255, 99, 132, 1)', 
           'rgba(54, 162, 235, 1)',
           'rgba(255, 206, 86, 1)',
           'rgba(75, 192, 192, 1)',
           'rgba(153, 102, 255, 1)',
           'rgba(255, 159, 64, 1)'

         ]

     }]}

     return Response(totalcigarschartdata)

class UserMoodChartView(APIView):

  def get(self, request):

    id = self.request.query_params.get('id')
    userdata = User.objects.filter(id=id).values().first()
    usercigar = Data.objects.filter(user=id, clz='jdfbots.chatbot.tracker').values('value').first()

    moodstressed = 0
    moodtired = 0
    moodneutral = 0
    moodangry = 0
    moodworried = 0
    moodsad = 0
    moodhappy = 0
    moodrelaxed = 0
    moodbored = 0

    if(usercigar == None):
      return Response(None)

    if(usercigar != None):
      datas=usercigar['value']
      jsondata = json.loads(datas)
      cigars = jsondata['cigarettes']

    
      for element in cigars:
        option = element['mood']
        if (option == 'MOOD_STRESSED'):
          moodstressed = moodstressed + 1
        elif (option == 'MOOD_TIRED'):
          moodtired = moodtired + 1
        elif (option == 'MOOD_NEUTRAL'):
          moodneutral = moodneutral + 1
        elif (option == 'MOOD_WORRIED'):
          moodworried = moodworried + 1
        elif (option == 'MOOD_ANGRY'):
          moodangry = moodangry + 1
        elif (option == 'MOOD_SAD'):
          moodsad = moodsad + 1
        elif (option == 'MOOD_HAPPY'):
          moodhappy = moodhappy + 1
        elif (option == 'MOOD_RELAXED'):
          moodrelaxed = moodrelaxed + 1
        else:
          moodbored = moodbored + 1
            
        usermoodchartData = {
        'labels': ['Stressed', 'Tired', 'Neutral', 'Worried', 'Angry','Sad','Happy', 'Relaxed','Bored'],
        'datasets': [{
          'label': 'Mood Behavior',
          'data': [moodstressed, moodtired, moodneutral, moodworried, moodangry,moodsad,moodhappy,moodrelaxed, moodbored],
          'backgroundColor': [                                                                                    
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                  'rgba(255, 159, 64, 0.2)',
                  'rgba(155, 192, 192, 0.2)',
                  'rgba(75, 102, 255, 0.2)',
                  'rgba(95, 159, 64, 0.2)'
          ],
          'borderColor': [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(253, 92, 92, 1)',
            'rgba(92, 102, 255, 1)',
            'rgba(55, 159, 64, 1)'
            ]
        }]}
    return Response(usermoodchartData)


class UserDistractChartView(APIView):

  def get(self, request):

    id = self.request.query_params.get('id')
    userdata = User.objects.filter(id=id).values().first()
    usercigar = Data.objects.filter(user=id, clz='jdfbots.chatbot.tracker').values('value').first()

    RESISTING_WALKING = 0
    RESISTING_WATER = 0
    RESISTING_TEETH = 0
    RESISTING_CHEWING = 0
    RESISTING_MUSIC = 0
    RESISTING_WEB = 0
    RESISTING_TALKING = 0
    RESISTING_PHONE = 0
    RESISTING_SHOWER = 0
    RESISTING_RELAXING = 0
    RESISTING_PLAYING = 0

    if (usercigar == None):
      return Response(None)

    if (usercigar != None):
      datas = usercigar['value']
      jsondata = json.loads(datas)
      cigars = jsondata['cigarettes']

      for element in cigars:
        option = element['resisting']
        if (option == 'RESISTING_WALKING'):
          RESISTING_WALKING = RESISTING_WALKING + 1
        elif (option == 'RESISTING_WATER'):
          RESISTING_WATER = RESISTING_WATER + 1
        elif (option == 'RESISTING_TEETH'):
          RESISTING_TEETH = RESISTING_TEETH + 1
        elif (option == 'RESISTING_CHEWING'):
          RESISTING_CHEWING = RESISTING_CHEWING + 1
        elif (option == 'RESISTING_MUSIC'):
          RESISTING_MUSIC = RESISTING_MUSIC + 1
        elif (option == 'RESISTING_WEB'):
          RESISTING_WEB = RESISTING_WEB + 1
        elif (option == 'RESISTING_TALKING'):
          RESISTING_TALKING = RESISTING_TALKING + 1
        elif (option == 'RESISTING_PHONE'):
          RESISTING_PHONE = RESISTING_PHONE + 1
        elif (option == 'RESISTING_SHOWER'):
          RESISTING_SHOWER = RESISTING_SHOWER + 1
        elif (option == 'RESISTING_RELAXING'):
          RESISTING_RELAXING = RESISTING_RELAXING + 1

        else:
          RESISTING_PLAYING = RESISTING_PLAYING + 1

        userdistractchartData = {
          'labels': ['Walking', 'Water', 'Teeth', 'Chewing', 'Music', 'Web', 'Talking', 'Phone', 'Shower','Relaxing','Playing'],
          'datasets': [{
            'label': 'Distraction Behavior',
            'data': [RESISTING_WALKING, RESISTING_WATER, RESISTING_TEETH, RESISTING_CHEWING, RESISTING_MUSIC, RESISTING_WEB, RESISTING_TALKING, RESISTING_PHONE,
                     RESISTING_SHOWER,RESISTING_RELAXING, RESISTING_PLAYING ],
            'backgroundColor': [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(155, 192, 192, 0.2)',
              'rgba(75, 102, 255, 0.2)',
              'rgba(95, 159, 64, 0.2)'
            ],
            'borderColor': [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
              'rgba(253, 92, 92, 1)',
              'rgba(92, 102, 255, 1)',
              'rgba(55, 159, 64, 1)'
            ]
          }]}
    return Response(userdistractchartData)

  class UserMoodChartView(APIView):

    def get(self, request):

      id = self.request.query_params.get('id')
      userdata = User.objects.filter(id=id).values().first()
      usercigar = Data.objects.filter(user=id, clz='jdfbots.chatbot.tracker').values('value').first()

      moodstressed = 0
      moodtired = 0
      moodneutral = 0
      moodangry = 0
      moodworried = 0
      moodsad = 0
      moodhappy = 0
      moodrelaxed = 0
      moodbored = 0

      if (usercigar == None):
         usermoodchartData = {
          'labels': ['Stressed', 'Tired', 'Neutral', 'Worried', 'Angry', 'Sad', 'Happy', 'Relaxed', 'Bored'],
          'datasets': [{
            'label': 'Mood Behavior',
            'data': [moodstressed, moodtired, moodneutral, moodworried, moodangry, moodsad, moodhappy, moodrelaxed,
                     moodbored],
            'backgroundColor': [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(155, 192, 192, 0.2)',
              'rgba(75, 102, 255, 0.2)',
              'rgba(95, 159, 64, 0.2)'
            ],
            'borderColor': [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
              'rgba(253, 92, 92, 1)',
              'rgba(92, 102, 255, 1)',
              'rgba(55, 159, 64, 1)'
            ]
          }]}
         return Response(usermoodchartData)

        #return Response(None)

      if (usercigar != None):
        datas = usercigar['value']
        jsondata = json.loads(datas)
        cigars = jsondata['cigarettes']

        for element in cigars:
          option = element['mood']
          if (option == 'MOOD_STRESSED'):
            moodstressed = moodstressed + 1
          elif (option == 'MOOD_TIRED'):
            moodtired = moodtired + 1
          elif (option == 'MOOD_NEUTRAL'):
            moodneutral = moodneutral + 1
          elif (option == 'MOOD_WORRIED'):
            moodworried = moodworried + 1
          elif (option == 'MOOD_ANGRY'):
            moodangry = moodangry + 1
          elif (option == 'MOOD_SAD'):
            moodsad = moodsad + 1
          elif (option == 'MOOD_HAPPY'):
            moodhappy = moodhappy + 1
          elif (option == 'MOOD_RELAXED'):
            moodrelaxed = moodrelaxed + 1
          else:
            moodbored = moodbored + 1

          usermoodchartData = {
            'labels': ['Stressed', 'Tired', 'Neutral', 'Worried', 'Angry', 'Sad', 'Happy', 'Relaxed', 'Bored'],
            'datasets': [{
              'label': 'Mood Behavior',
              'data': [moodstressed, moodtired, moodneutral, moodworried, moodangry, moodsad, moodhappy, moodrelaxed,
                       moodbored],
              'backgroundColor': [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(155, 192, 192, 0.2)',
                'rgba(75, 102, 255, 0.2)',
                'rgba(95, 159, 64, 0.2)'
              ],
              'borderColor': [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(253, 92, 92, 1)',
                'rgba(92, 102, 255, 1)',
                'rgba(55, 159, 64, 1)'
              ]
            }]}
      return Response(usermoodchartData)


class UserAloneChartView(APIView):

  def get(self, request):

    id = self.request.query_params.get('id')
    userdata = User.objects.filter(id=id).values().first()
    usercigar = Data.objects.filter(user=id, clz='jdfbots.chatbot.tracker').values('value').first()

    ALONE_YES = 0
    ALONE_NO = 0


    if (usercigar == None):
      return Response(None)

    if (usercigar != None):
      datas = usercigar['value']
      jsondata = json.loads(datas)
      cigars = jsondata['cigarettes']

      for element in cigars:
        option = element['alone']
        if (option == 'ALONE_YES'):
          ALONE_YES = ALONE_YES + 1
        else:
          ALONE_NO = ALONE_NO + 1

        useralonechartData = {
          'labels': ['Yes', 'No'],
          'datasets': [{
            'label': 'Loneliness Behavior',
            'data': [ALONE_YES, ALONE_NO],
            'backgroundColor': [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(155, 192, 192, 0.2)',
              'rgba(75, 102, 255, 0.2)',
              'rgba(95, 159, 64, 0.2)'
            ],
            'borderColor': [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
              'rgba(253, 92, 92, 1)',
              'rgba(92, 102, 255, 1)',
              'rgba(55, 159, 64, 1)'
            ]
          }]}
    return Response(useralonechartData)

class UserDriveChartView(APIView):

  def get(self, request):

    id = self.request.query_params.get('id')
    userdata = User.objects.filter(id=id).values().first()
    usercigar = Data.objects.filter(user=id, clz='jdfbots.chatbot.tracker').values('value').first()

    DRIVING_YES = 0
    DRIVING_NO = 0


    if (usercigar == None):
      return Response(None)

    if (usercigar != None):
      datas = usercigar['value']
      jsondata = json.loads(datas)
      cigars = jsondata['cigarettes']

      for element in cigars:
        option = element['driving']
        if (option == 'DRIVING_YES'):
          DRIVING_YES = DRIVING_YES + 1
        else:
          DRIVING_NO = DRIVING_NO + 1

        userdrivechartData = {
          'labels': ['Yes', 'No'],
          'datasets': [{
            'label': 'Loneliness Behavior',
            'data': [DRIVING_YES, DRIVING_NO],
            'backgroundColor': [
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(155, 192, 192, 0.2)',
              'rgba(75, 102, 255, 0.2)',
              'rgba(95, 159, 64, 0.2)'
            ],
            'borderColor': [
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
              'rgba(253, 92, 92, 1)',
              'rgba(92, 102, 255, 1)',
              'rgba(55, 159, 64, 1)'
            ]
          }]}
    return Response(userdrivechartData)


class GroupNecessarylCigarsView(APIView):
  def get(self, request):
    groupnumber = []
    totalcigars = []
    datalist = []
    total = 0
    totalyes = 0
    totalno = 0

    groups = Group.objects.values_list('id', flat=True)
    groupsize = len(groups)
    groupname = Group.objects.values_list('name', flat=True)

    for idx, group in enumerate(groups):
      groupnumber.append(group)
      data = groups[idx]
      groupusers = User.objects.filter(gid=data).values('id')
      total = 0

      for id in groupusers:
        groupusersdata = Data.objects.filter(user=id['id'], clz='jdfbots.chatbot.tracker').values(
          'value').first()

        # if(groupusersdata == None):
        #    datalist.append(groupusersdata)
        #    totalcigars.append(0)

        if (groupusersdata != None):
          datalist.append(groupusersdata)
          datas = groupusersdata['value']
          jsondata = json.loads(datas)
          cigars = jsondata['cigarettes']

          for element in cigars:
            option = element['necessary']
            if (option == 'NECESSARY_YES'):
              totalyes = totalyes + 1
            else:
              totalno = totalno + 1

    groupnecessarychartData = {
          'labels': ['Yes', 'No'],
          'datasets': [{
          'label': 'Necessary Behavior',
          'data': [totalyes, totalno],
          'backgroundColor': [
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)',
          'rgba(155, 192, 192, 0.2)',
          'rgba(75, 102, 255, 0.2)',
          'rgba(95, 159, 64, 0.2)'
          ],
          'borderColor': [
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
          'rgba(253, 92, 92, 1)',
          'rgba(92, 102, 255, 1)',
          'rgba(55, 159, 64, 1)'
              ]
            }]}


    return Response(groupnecessarychartData)



class GroupContextView(APIView):

  def get(self, request):

    gid = self.request.query_params.get('gid')
    contextpriv = 0
    contextprof = 0
    groupname = []
    groupnumber = []


    if (gid == "all"):
      gid = 'all'
      tracker = Data.objects.filter(clz='jdfbots.chatbot.tracker').values('value').first()
      groups = Group.objects.values_list('id', flat=True)
      groupsize = len(groups)
      groupname = Group.objects.values_list('name', flat=True)

      for idx, group in enumerate(groups):
        groupnumber.append(group)
        data = groups[idx]
        groupusers = User.objects.filter(gid=data).values('id')
        total = 0

        for id in groupusers:
          groupusersdata = Data.objects.filter(user=id['id'], clz='jdfbots.chatbot.tracker').values(
            'value').first()

          # if(groupusersdata == None):
          #    datalist.append(groupusersdata)
          #    totalcigars.append(0)

          if (groupusersdata != None):

            datas = groupusersdata['value']
            jsondata = json.loads(datas)
            cigars = jsondata['cigarettes']

            for element in cigars:
              option = element['context']
              if (option == 'CONTEXT_PRIVE'):
                contextpriv = contextpriv + 1
              else:
                contextprof = contextprof + 1

      groupcontextchartData = {
        'labels': ['Private', 'Professional'],
        'datasets': [{
          'label': 'Context Stats',
          'data': [contextpriv, contextprof],
          'backgroundColor': [
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(155, 192, 192, 0.2)',
            'rgba(75, 102, 255, 0.2)',
            'rgba(95, 159, 64, 0.2)'
          ],
          'borderColor': [
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(253, 92, 92, 1)',
            'rgba(92, 102, 255, 1)',
            'rgba(55, 159, 64, 1)'
          ]
        }]}

      return Response(groupcontextchartData)

    if (gid != None):
      groupusers = User.objects.filter(gid=gid).values('id')

      for id in groupusers:
          groupusersdata = Data.objects.filter(user=id['id'], clz='jdfbots.chatbot.tracker').values(
            'value').first()

          # if(groupusersdata == None):
          #    datalist.append(groupusersdata)
          #    totalcigars.append(0)

          if (groupusersdata != None):

            datas = groupusersdata['value']
            jsondata = json.loads(datas)
            cigars = jsondata['cigarettes']

            for element in cigars:
              option = element['context']
              if (option == 'CONTEXT_PRIVE'):
                contextpriv = contextpriv + 1
              else:
                contextprof = contextprof + 1

      groupcontextchartData = {
        'labels': ['Private', 'Professional'],
        'datasets': [{
          'label': 'Context Stats',
          'data': [contextpriv, contextprof],
          'backgroundColor': [
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(155, 192, 192, 0.2)',
            'rgba(75, 102, 255, 0.2)',
            'rgba(95, 159, 64, 0.2)'
          ],
          'borderColor': [
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(253, 92, 92, 1)',
            'rgba(92, 102, 255, 1)',
            'rgba(55, 159, 64, 1)'
          ]
        }]}

      return Response(groupcontextchartData)



    else:
      groupcontextchartData = {
        'labels': ['Private', 'Professional'],
        'datasets': [{
          'label': 'Context Stats',
          'data': [contextpriv, contextprof],
          'backgroundColor': [
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(155, 192, 192, 0.2)',
            'rgba(75, 102, 255, 0.2)',
            'rgba(95, 159, 64, 0.2)'
          ],
          'borderColor': [
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(253, 92, 92, 1)',
            'rgba(92, 102, 255, 1)',
            'rgba(55, 159, 64, 1)'
          ]
        }]}

      return Response(groupcontextchartData)

class GroupMoodAllView(APIView):

  def get(self, request):

    gid = self.request.query_params.get('gid')

    moodstressed = 0
    moodtired = 0
    moodneutral = 0
    moodangry = 0
    moodworried = 0
    moodsad = 0
    moodhappy = 0
    moodrelaxed = 0
    moodbored = 0
    groupnumber =[]



    if (gid == "all"):
      gid = 'all'
      tracker = Data.objects.filter(clz='jdfbots.chatbot.tracker').values('value')
      groups = Group.objects.values_list('id', flat=True)
      groupsize = len(groups)
      groupname = Group.objects.values_list('name', flat= True)

      for idx, group in enumerate(groups):
        groupnumber.append(group)

        data = groups[idx]
        groupusers = User.objects.filter(gid=data).values('id')


        for id in groupusers:
          groupusersdata = Data.objects.filter(user=id['id'], clz='jdfbots.chatbot.tracker').values(
            'value').first()

          # if(groupusersdata == None):
          #    datalist.append(groupusersdata)
          #    totalcigars.append(0)

          if (groupusersdata != None):

            datas = groupusersdata['value']
            jsondata = json.loads(datas)
            cigars = jsondata['cigarettes']

            for element in cigars:
              option = element['mood']
              if (option == 'MOOD_STRESSED'):
                moodstressed = moodstressed + 1
              elif (option == 'MOOD_TIRED'):
                moodtired = moodtired + 1
              elif (option == 'MOOD_NEUTRAL'):
                moodneutral = moodneutral + 1
              elif (option == 'MOOD_WORRIED'):
                moodworried = moodworried + 1
              elif (option == 'MOOD_ANGRY'):
                moodangry = moodangry + 1
              elif (option == 'MOOD_SAD'):
                moodsad = moodsad + 1
              elif (option == 'MOOD_HAPPY'):
                moodhappy = moodhappy + 1
              elif (option == 'MOOD_RELAXED'):
                moodrelaxed = moodrelaxed + 1
              else:
                moodbored = moodbored + 1

              groupallmoodchartData = {
                'labels': ['Stressed', 'Tired', 'Neutral', 'Worried', 'Angry', 'Sad', 'Happy', 'Relaxed', 'Bored'],
                'datasets': [{
                  'label': 'Mood Behavior',
                  'data': [moodstressed, moodtired, moodneutral, moodworried, moodangry, moodsad, moodhappy,
                           moodrelaxed,
                           moodbored],
                  'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(155, 192, 192, 0.2)',
                    'rgba(75, 102, 255, 0.2)',
                    'rgba(95, 159, 64, 0.2)'
                  ],
                  'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(253, 92, 92, 1)',
                    'rgba(92, 102, 255, 1)',
                    'rgba(55, 159, 64, 1)'
                  ]
                }]}
      return Response(groupallmoodchartData)

    if (gid != None):
      groupusers = User.objects.filter(gid=gid).values('id')

      for id in groupusers:
          groupusersdata = Data.objects.filter(user=id['id'], clz='jdfbots.chatbot.tracker').values(
            'value').first()

          # if(groupusersdata == None):
          #    datalist.append(groupusersdata)
          #    totalcigars.append(0)

          if (groupusersdata != None):

            datas = groupusersdata['value']
            jsondata = json.loads(datas)
            cigars = jsondata['cigarettes']

            for element in cigars:
              option = element['mood']
              if (option == 'MOOD_STRESSED'):
                moodstressed = moodstressed + 1
              elif (option == 'MOOD_TIRED'):
                moodtired = moodtired + 1
              elif (option == 'MOOD_NEUTRAL'):
                moodneutral = moodneutral + 1
              elif (option == 'MOOD_WORRIED'):
                moodworried = moodworried + 1
              elif (option == 'MOOD_ANGRY'):
                moodangry = moodangry + 1
              elif (option == 'MOOD_SAD'):
                moodsad = moodsad + 1
              elif (option == 'MOOD_HAPPY'):
                moodhappy = moodhappy + 1
              elif (option == 'MOOD_RELAXED'):
                moodrelaxed = moodrelaxed + 1
              else:
                moodbored = moodbored + 1

              groupallmoodchartData = {
                'labels': ['Stressed', 'Tired', 'Neutral', 'Worried', 'Angry', 'Sad', 'Happy', 'Relaxed', 'Bored'],
                'datasets': [{
                  'label': 'Mood Behavior',
                  'data': [moodstressed, moodtired, moodneutral, moodworried, moodangry, moodsad, moodhappy,
                           moodrelaxed,
                           moodbored],
                  'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(155, 192, 192, 0.2)',
                    'rgba(75, 102, 255, 0.2)',
                    'rgba(95, 159, 64, 0.2)'
                  ],
                  'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(253, 92, 92, 1)',
                    'rgba(92, 102, 255, 1)',
                    'rgba(55, 159, 64, 1)'
                  ]
                }]}
      return Response(groupallmoodchartData)

    else:
           groupallmoodchartData = {
          'labels': ['Stressed', 'Tired', 'Neutral', 'Worried', 'Angry', 'Sad', 'Happy', 'Relaxed', 'Bored'],
          'datasets': [{
          'label': 'Mood Behavior',
          'data': [moodstressed, moodtired, moodneutral, moodworried, moodangry, moodsad, moodhappy,
               moodrelaxed,
               moodbored],
         'backgroundColor': [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(155, 192, 192, 0.2)',
        'rgba(75, 102, 255, 0.2)',
        'rgba(95, 159, 64, 0.2)'
      ],
      'borderColor': [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(253, 92, 92, 1)',
        'rgba(92, 102, 255, 1)',
        'rgba(55, 159, 64, 1)'
      ]
    }]}
    return Response(groupallmoodchartData)


class GroupDesireAllView(APIView):

  def get(self, request):

    gid = self.request.query_params.get('gid')

    desirelow = 0
    desirenone = 0
    desiremedium = 0
    desirehigh = 0
    desireextreme = 0
    groupnumber =[]


    if (gid == "all"):
      gid = 'all'
      tracker = Data.objects.filter(clz='jdfbots.chatbot.tracker').values('value')
      groups = Group.objects.values_list('id', flat=True)
      groupsize = len(groups)
      groupname = Group.objects.values_list('name', flat= True)

      for idx, group in enumerate(groups):
        groupnumber.append(group)

        data = groups[idx]
        groupusers = User.objects.filter(gid=data).values('id')


        for id in groupusers:
          groupusersdata = Data.objects.filter(user=id['id'], clz='jdfbots.chatbot.tracker').values(
            'value').first()

          # if(groupusersdata == None):
          #    datalist.append(groupusersdata)
          #    totalcigars.append(0)

          if (groupusersdata != None):

            datas = groupusersdata['value']
            jsondata = json.loads(datas)
            cigars = jsondata['cigarettes']

            for element in cigars:
              option = element['desire']
              if (option == 'DESIRE_LOW'):
                desirelow = desirelow + 1
              elif (option == 'DESIRE_NONE'):
                desirenone = desirenone + 1
              elif (option == 'DESIRE_MEDIUM'):
                desiremedium = desiremedium + 1
              elif (option == 'DESIRE_HIGH'):
                desirehigh = desirehigh + 1
              else:
                desireextreme = desireextreme + 1
              groupalldesirechartData = {
                'labels': ['None', 'Low', 'Medium', 'High', 'Extreme'],
                'datasets': [{
                  'label': 'Group Desire Behavior',
                  'data': [desirenone, desirelow, desiremedium, desirehigh, desireextreme
                           ],
                  'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(155, 192, 192, 0.2)',
                    'rgba(75, 102, 255, 0.2)',
                    'rgba(95, 159, 64, 0.2)'
                  ],
                  'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(253, 92, 92, 1)',
                    'rgba(92, 102, 255, 1)',
                    'rgba(55, 159, 64, 1)'
                  ]
                }]}
      return Response(groupalldesirechartData)

    if (gid != None):
      groupusers = User.objects.filter(gid=gid).values('id')

      for id in groupusers:
          groupusersdata = Data.objects.filter(user=id['id'], clz='jdfbots.chatbot.tracker').values(
            'value').first()

          # if(groupusersdata == None):
          #    datalist.append(groupusersdata)
          #    totalcigars.append(0)

          if (groupusersdata != None):

            datas = groupusersdata['value']
            jsondata = json.loads(datas)
            cigars = jsondata['cigarettes']

            for element in cigars:
              option = element['desire']
              if (option == 'DESIRE_LOW'):
                desirelow = desirelow + 1
              elif (option == 'DESIRE_NONE'):
                desirenone = desirenone + 1
              elif (option == 'DESIRE_MEDIUM'):
                desiremedium = desiremedium + 1
              elif (option == 'DESIRE_HIGH'):
                desirehigh = desirehigh + 1
              else:
                desireextreme = desireextreme + 1
              groupalldesirechartData = {
                'labels': ['None', 'Low', 'Medium', 'High', 'Extreme'],
                'datasets': [{
                  'label': 'Group Desire Behavior',
                  'data': [desirenone, desirelow, desiremedium, desirehigh, desireextreme
                           ],
                  'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(155, 192, 192, 0.2)',
                    'rgba(75, 102, 255, 0.2)',
                    'rgba(95, 159, 64, 0.2)'
                  ],
                  'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(253, 92, 92, 1)',
                    'rgba(92, 102, 255, 1)',
                    'rgba(55, 159, 64, 1)'
                  ]
                }]}
            return Response(groupalldesirechartData)

      else:
             groupalldesirechartData = {
               'labels': ['None', 'Low', 'Medium', 'High', 'Extreme'],
               'datasets': [{
                 'label': 'Group Desire Behavior',
                 'data': [desirenone, desirelow, desiremedium, desirehigh, desireextreme
                          ],
                 'backgroundColor': [
                   'rgba(255, 99, 132, 0.2)',
                   'rgba(54, 162, 235, 0.2)',
                   'rgba(255, 206, 86, 0.2)',
                   'rgba(75, 192, 192, 0.2)',
                   'rgba(153, 102, 255, 0.2)',
                   'rgba(255, 159, 64, 0.2)',
                   'rgba(155, 192, 192, 0.2)',
                   'rgba(75, 102, 255, 0.2)',
                   'rgba(95, 159, 64, 0.2)'
                 ],
                 'borderColor': [
                   'rgba(255, 99, 132, 1)',
                   'rgba(54, 162, 235, 1)',
                   'rgba(255, 206, 86, 1)',
                   'rgba(75, 192, 192, 1)',
                   'rgba(153, 102, 255, 1)',
                   'rgba(255, 159, 64, 1)',
                   'rgba(253, 92, 92, 1)',
                   'rgba(92, 102, 255, 1)',
                   'rgba(55, 159, 64, 1)'
                 ]
               }]}
      return Response(groupalldesirechartData)

    else:
          groupalldesirechartData = {
              'labels': ['None', 'Low', 'Medium', 'High', 'Extreme'],
              'datasets': [{
                'label': 'Group Desire Behavior',
                'data': [desirenone, desirelow, desiremedium, desirehigh, desireextreme
                         ],
         'backgroundColor': [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(155, 192, 192, 0.2)',
        'rgba(75, 102, 255, 0.2)',
        'rgba(95, 159, 64, 0.2)'
      ],
      'borderColor': [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(253, 92, 92, 1)',
        'rgba(92, 102, 255, 1)',
        'rgba(55, 159, 64, 1)'
      ]
    }]}
    return Response(groupalldesirechartData)


### Group Motivation view

class GroupMotivationAllView(APIView):

  def get(self, request):



    gid = self.request.query_params.get('gid')
      #users = User.objects.filter(gid=id)

    DISTRACT_WALKING = 0
    DISTRACT_WATER = 0
    DISTRACT_TEETH = 0
    DISTRACT_CHEWING = 0
    DISTRACT_MUSIC = 0
    DISTRACT_WEB = 0
    DISTRACT_TALKING = 0
    DISTRACT_PHONE = 0
    DISTRACT_SHOWER = 0
    DISTRACT_RELAXING = 0
    DISTRACT_PLAYING = 0
    DISTRACT_GAME = 0
    DISTRACT_APPLE = 0
    DISTRACT_VEGETABLES = 0
    DISTRACT_MOVE = 0
    DISTRACT_JUICE = 0
    DISTRACT_EXERCISING = 0


    groupnumber = []

    if (gid == "all"):
        gid = 'all'
        tracker = Data.objects.filter(clz='jdfbots.chatbot.cessation').values('value')
        groups = Group.objects.values_list('id', flat=True)
        groupsize = len(groups)
        groupname = Group.objects.values_list('name', flat=True)

        for idx, group in enumerate(groups):
          groupnumber.append(group)

          data = groups[idx]
          groupusers = User.objects.filter(gid=data).values('id')

          for id in groupusers:
            groupusersdata = Data.objects.filter(user=id['id'], clz='jdfbots.chatbot.cessation').values(
              'value').first()

            # if(groupusersdata == None):
            #    datalist.append(groupusersdata)
            #    totalcigars.append(0)

            if (groupusersdata != None):

              datas = groupusersdata['value']
              jsondata = json.loads(datas)
              cigars = jsondata['helped']

              for element in cigars:
                option = element['distraction']
                if (option == 'DISTRACT_WALKING'):
                  DISTRACT_WALKING = DISTRACT_WALKING + 1
                elif (option == 'DISTRACT_WATER'):
                  DISTRACT_WATER = DISTRACT_WATER + 1
                elif (option == 'DISTRACT_TEETH'):
                  DISTRACT_TEETH = DISTRACT_TEETH + 1
                elif (option == 'DISTRACT_CHEWING'):
                  DISTRACT_CHEWING = DISTRACT_CHEWING + 1
                elif (option == 'DISTRACT_MUSIC'):
                  DISTRACT_MUSIC = DISTRACT_MUSIC + 1
                elif (option == 'DISTRACT_WEB'):
                  DISTRACT_WEB = DISTRACT_WEB + 1
                elif (option == 'DISTRACT_TALKING'):
                  DISTRACT_TALKING = DISTRACT_TALKING + 1
                elif (option == 'DISTRACT_PHONE'):
                  DISTRACT_PHONE = DISTRACT_PHONE + 1
                elif (option == 'DISTRACT_SHOWER'):
                  DISTRACT_SHOWER = DISTRACT_SHOWER + 1
                elif (option == 'DISTRACT_GAME'):
                  DISTRACT_GAME = DISTRACT_GAME + 1
                elif (option == 'DISTRACT_APPLE'):
                  DISTRACT_APPLE = DISTRACT_APPLE + 1
                elif (option == 'DISTRACT_VEGETABLES'):
                  DISTRACT_VEGETABLES = DISTRACT_VEGETABLES + 1
                elif (option == 'DISTRACT_MOVE'):
                  DISTRACT_MOVE = DISTRACT_MOVE + 1
                elif (option == 'DISTRACT_JUICE'):
                  DISTRACT_JUICE = DISTRACT_JUICE + 1
                elif (option == 'DISTRACT_EXERCISING'):
                  DISTRACT_EXERCISING = DISTRACT_EXERCISING + 1
                else:
                  DISTRACT_PLAYING = DISTRACT_PLAYING + 1
              groupallmotivechartData = {
                   'labels': ['Walking', 'Water', 'Teeth', 'Chewing', 'Music', 'Web', 'Talking', 'Phone', 'Shower','Relaxing','Game','Apple','Vegetables','Move','Juice','Excercising','Playing'],
            'datasets': [{
            'label': 'Distraction Behavior',
            'data': [DISTRACT_WALKING, DISTRACT_WATER, DISTRACT_TEETH, DISTRACT_CHEWING, DISTRACT_MUSIC, DISTRACT_WEB, DISTRACT_TALKING, DISTRACT_PHONE,
                     DISTRACT_SHOWER, DISTRACT_RELAXING, DISTRACT_GAME, DISTRACT_APPLE, DISTRACT_VEGETABLES, DISTRACT_MOVE, DISTRACT_JUICE, DISTRACT_EXERCISING, DISTRACT_PLAYING ],
            'backgroundColor': [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(155, 192, 192, 0.2)',
              'rgba(75, 102, 255, 0.2)',
              'rgba(95, 159, 64, 0.2)',
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(155, 192, 192, 0.2)',
              'rgba(75, 102, 255, 0.2)',
              'rgba(95, 159, 64, 0.2)'
            ],
            'borderColor': [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
              'rgba(253, 92, 92, 1)',
              'rgba(92, 102, 255, 1)',
              'rgba(55, 159, 64, 1)',
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
              'rgba(253, 92, 92, 1)',
              'rgba(92, 102, 255, 1)',
              'rgba(55, 159, 64, 1)'
            ]
          }]}
        return Response(groupallmotivechartData)

    if (gid != None):
        groupusers = User.objects.filter(gid=gid).values('id')

        for id in groupusers:
          groupusersdata = Data.objects.filter(user=id['id'], clz='jdfbots.chatbot.cessation').values(
            'value').first()

          # if(groupusersdata == None):
          #    datalist.append(groupusersdata)
          #    totalcigars.append(0)

          if (groupusersdata != None):

            datas = groupusersdata['value']
            jsondata = json.loads(datas)
            cigars = jsondata['helped']

            for element in cigars:
              option = element['distraction']
              if (option == 'DISTRACT_WALKING'):
                DISTRACT_WALKING = DISTRACT_WALKING + 1
              elif (option == 'DISTRACT_WATER'):
                DISTRACT_WATER = DISTRACT_WATER + 1
              elif (option == 'DISTRACT_TEETH'):
                DISTRACT_TEETH = DISTRACT_TEETH + 1
              elif (option == 'DISTRACT_CHEWING'):
                DISTRACT_CHEWING = DISTRACT_CHEWING + 1
              elif (option == 'DISTRACT_MUSIC'):
                DISTRACT_MUSIC = DISTRACT_MUSIC + 1
              elif (option == 'DISTRACT_WEB'):
                DISTRACT_WEB = DISTRACT_WEB + 1
              elif (option == 'DISTRACT_TALKING'):
                DISTRACT_TALKING = DISTRACT_TALKING + 1
              elif (option == 'DISTRACT_PHONE'):
                DISTRACT_PHONE = DISTRACT_PHONE + 1
              elif (option == 'DISTRACT_SHOWER'):
                DISTRACT_SHOWER = DISTRACT_SHOWER + 1
              elif (option == 'DISTRACT_GAME'):
                DISTRACT_GAME = DISTRACT_GAME + 1
              elif (option == 'DISTRACT_APPLE'):
                DISTRACT_APPLE = DISTRACT_APPLE + 1
              elif (option == 'DISTRACT_VEGETABLES'):
                DISTRACT_VEGETABLES = DISTRACT_VEGETABLES + 1
              elif (option == 'DISTRACT_MOVE'):
                DISTRACT_MOVE = DISTRACT_MOVE + 1
              elif (option == 'DISTRACT_JUICE'):
                DISTRACT_JUICE = DISTRACT_JUICE + 1
              elif (option == 'DISTRACT_EXERCISING'):
                DISTRACT_EXERCISING = DISTRACT_EXERCISING + 1
              else:
                DISTRACT_PLAYING = DISTRACT_PLAYING + 1
            groupallmotivechartData = {
                'labels': ['Walking', 'Water', 'Teeth', 'Chewing', 'Music', 'Web', 'Talking', 'Phone', 'Shower',
                           'Relaxing', 'Game', 'Apple', 'Vegetables', 'Move', 'Juice', 'Excercising', 'Playing'],
                'datasets': [{
                  'label': 'Distraction Behavior',
                  'data': [DISTRACT_WALKING, DISTRACT_WATER, DISTRACT_TEETH, DISTRACT_CHEWING, DISTRACT_MUSIC,
                           DISTRACT_WEB, DISTRACT_TALKING, DISTRACT_PHONE,
                           DISTRACT_SHOWER, DISTRACT_RELAXING, DISTRACT_GAME, DISTRACT_APPLE, DISTRACT_VEGETABLES,
                           DISTRACT_MOVE, DISTRACT_JUICE, DISTRACT_EXERCISING, DISTRACT_PLAYING],
                  'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(155, 192, 192, 0.2)',
                    'rgba(75, 102, 255, 0.2)',
                    'rgba(95, 159, 64, 0.2)'
                  ],
                  'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(253, 92, 92, 1)',
                    'rgba(92, 102, 255, 1)',
                    'rgba(55, 159, 64, 1)'
                  ]
                }]}
          else:
            groupallmotivechartData = {
              'labels': ['Walking', 'Water', 'Teeth', 'Chewing', 'Music', 'Web', 'Talking', 'Phone', 'Shower',
                         'Relaxing', 'Game', 'Apple', 'Vegetables', 'Move', 'Juice', 'Excercising', 'Playing'],
              'datasets': [{
                'label': 'Distraction Behavior',
                'data': [DISTRACT_WALKING, DISTRACT_WATER, DISTRACT_TEETH, DISTRACT_CHEWING, DISTRACT_MUSIC,
                         DISTRACT_WEB, DISTRACT_TALKING, DISTRACT_PHONE,
                         DISTRACT_SHOWER, DISTRACT_RELAXING, DISTRACT_GAME, DISTRACT_APPLE, DISTRACT_VEGETABLES,
                         DISTRACT_MOVE, DISTRACT_JUICE, DISTRACT_EXERCISING, DISTRACT_PLAYING],
                'backgroundColor': [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                  'rgba(255, 159, 64, 0.2)',
                  'rgba(155, 192, 192, 0.2)',
                  'rgba(75, 102, 255, 0.2)',
                  'rgba(95, 159, 64, 0.2)'
                ],
                'borderColor': [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)',
                  'rgba(253, 92, 92, 1)',
                  'rgba(92, 102, 255, 1)',
                  'rgba(55, 159, 64, 1)'
                ]
              }]}
            return Response(groupallmotivechartData)

        return Response(groupallmotivechartData)
    else:
            groupallmotivechartData = {
              'labels': ['Walking', 'Water', 'Teeth', 'Chewing', 'Music', 'Web', 'Talking', 'Phone', 'Shower',
                         'Relaxing', 'Game', 'Apple', 'Vegetables', 'Move', 'Juice', 'Excercising', 'Playing'],
              'datasets': [{
                'label': 'Distraction Behavior',
                'data': [DISTRACT_WALKING, DISTRACT_WATER, DISTRACT_TEETH, DISTRACT_CHEWING, DISTRACT_MUSIC,
                         DISTRACT_WEB, DISTRACT_TALKING, DISTRACT_PHONE,
                         DISTRACT_SHOWER, DISTRACT_RELAXING, DISTRACT_GAME, DISTRACT_APPLE, DISTRACT_VEGETABLES,
                         DISTRACT_MOVE, DISTRACT_JUICE, DISTRACT_EXERCISING, DISTRACT_PLAYING],
                'backgroundColor': [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                  'rgba(255, 159, 64, 0.2)',
                  'rgba(155, 192, 192, 0.2)',
                  'rgba(75, 102, 255, 0.2)',
                  'rgba(95, 159, 64, 0.2)'
                ],
                'borderColor': [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)',
                  'rgba(253, 92, 92, 1)',
                  'rgba(92, 102, 255, 1)',
                  'rgba(55, 159, 64, 1)'
                ]
              }]}
            return Response(groupallmotivechartData)


  def logout(request):
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
      user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)

    request.session.flush()
    if hasattr(request, 'user'):
      from django.contrib.auth.models import AnonymousUser
      request.user = AnonymousUser()


class UpdatePhase(generics.UpdateAPIView):
  queryset = Group.objects.all()
  serializer_class = GroupSerializer


  def update(self, request, *args, **kwargs):
        group = self.get_object()
        group.name = request.data.get("state")
        group.save()

        serializer = self.get_serializer(group)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)



class GroupLastId(APIView):
   def get(self, request):

     last = Group.objects.values_list('id', flat=True)
     if(last == None):
       newid = '1'
     else:
      idlist = list(last)
      idlist.reverse()
      newid= str(int(idlist[0]) + 1)

     return Response({'id':newid})

#class Logout_View(APIView):
def logout_view(self, request):
    logout(request)






