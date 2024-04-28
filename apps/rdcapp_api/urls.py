# from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views


urlpatterns = [
    path("region", views.RegionView.as_view()),
    # Список сотрудников региона
    path(
        "region/<int:regionid>/",
        include(
            [
                # path('profile/', profile, name='users-profile'),
                path("employee", views.RegionEmployeeView.as_view()),
                # path("municipalities", views.RegionMunicipalityView.as_view()),
                path(
                    "eduinstitutions/",
                    include(
                        [
                            path("", views.RegionEduInstOriginView.as_view()),
                            path("schools", views.RegionSchoolsOriginView.as_view()),
                            path("spo", views.RegionSPOOriginView.as_view()),
                        ]
                    ),
                ),
                path(
                    "municipalities/",
                    include(
                        [
                            path("", views.RegionMunicipalityView.as_view()),
                            path(
                                "<int:municipalityid>/",
                                include(
                                    [
                                        path(
                                            "eduinstitutions/",
                                            include(
                                                [
                                                    path(
                                                        "",
                                                        views.MunicipalityEduInstOriginView.as_view(),
                                                    ),
                                                    path(
                                                        "schools/",
                                                        views.MunicipalitySchoolOriginView.as_view(),
                                                    ),
                                                    path(
                                                        "spo/",
                                                        views.MunicipalitySPOOriginView.as_view(),
                                                    ),
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    path(
        "auth/",
        include(
            [
                path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
                path(
                    "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
                ),
                path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
            ]
        ),
    ),
]
