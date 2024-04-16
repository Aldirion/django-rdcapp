# from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rdcapp_api import views


urlpatterns = [
    path('region', views.RegionView.as_view()),
    #Список сотрудников региона
    path('region/<int:regionid>/', include([
        # path('profile/', profile, name='users-profile'),
        path('employee', views.RegionEmployeeView.as_view()),
        path('municipalities', views.RegionMunicipalityView.as_view())
    ]))
]