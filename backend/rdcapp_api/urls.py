# from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rdcapp_api import views

# router = routers.DefaultRouter()
# router.register(r'employee', views.EmployeeViewSet)
# router.register(r'municipality', views.MunicipalityViewSet)
# router.register(r'region', views.RegionViewSet)


urlpatterns = [
    path('employee', views.EmployeeView.as_view()),
    path('region', views.RegionView.as_view()),
    #Список сотрудников региона
    path('region/<int:regionid>/', include([
        path('employee', views.RegionEmployeeView.as_view()),
        
    ]
    )
    )
]