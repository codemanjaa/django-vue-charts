from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app import views
from django.contrib import admin


router = DefaultRouter()
router.register(r'group', views.GroupViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'userset', views.UserSet)
router.register(r'groupstat',views.GroupStatView)
router.register(r'datastat', views.DataViewSet)
router.register(r'userdetails',views.UserDetailViewSet)
router.register(r'groupdetails',views.GroupView)



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
  path('groupmotivationall/', views.GroupMotivationAllView.as_view()),
  path('updatephase/', views.UpdatePhase.as_view()),
  path('lastid/', views.GroupLastId.as_view()),
  #path('logout/', views.Logout_View.as_view()),

  #path('admin/',admin.site.urls)




]
admin.site.site_header = "J'arrete de fumer - Help Admin"
admin.site.site_title = "J'arrete de fumer Admin Portal"
admin.site.index_title = "Welcome to J'arrete de fumer Portal"


