# from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
<<<<<<< Updated upstream:backend/rdcapp_api/urls.py
from rdcapp_api import views
=======

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views
>>>>>>> Stashed changes:apps/rdcapp_api/urls.py


urlpatterns = [
    path('region', views.RegionView.as_view()),
    #Список сотрудников региона
    path('region/<int:regionid>/', include([
        # path('profile/', profile, name='users-profile'),
        path('employee', views.RegionEmployeeView.as_view()),
        path('municipalities', views.RegionMunicipalityView.as_view())
<<<<<<< Updated upstream:backend/rdcapp_api/urls.py
    ]))
]
=======
    ])),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
>>>>>>> Stashed changes:apps/rdcapp_api/urls.py
