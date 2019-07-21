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
]


