from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app import views



router = DefaultRouter()
router.register(r'group', views.GroupViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'groupstat',views.GroupStatView)
router.register(r'datastat', views.DataViewSet)



urlpatterns = [
  path('', include(router.urls)),
  path('groupgadget/', views.GroupGadgetView.as_view()),
  path('groupuserlist/', views.GroupUserView.as_view()),
  path('groupchart/', views.GroupChartView.as_view()),
  path('userprofile/', views.UserProfileView.as_view()),
  path('userchart/', views.UserChartDataView.as_view()),
  path('grouppie/', views.GenderPieView.as_view()),
  path('groupmood/', views.GroupMoodView.as_view()),
  path('grouptotal/', views.GroupTotalCigarsView.as_view()),
  path('usermood/', views.UserMoodChartView.as_view()),
  path('userdistract/', views.UserDistractChartView.as_view()),
  path('useralone/', views.UserAloneChartView.as_view()),
  path('userdrive/', views.UserDriveChartView.as_view()),
  path('groupnecessary/', views.GroupNecessarylCigarsView.as_view()),
  path('groupcontext/', views.GroupContextView.as_view()),
  path('groupmoodall/', views.GroupMoodAllView.as_view()),
  path('groupdesireall/', views.GroupDesireAllView.as_view()),




]


