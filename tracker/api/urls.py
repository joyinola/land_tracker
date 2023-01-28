from django.urls import path
from .views import UserLandView

urlpatterns=[
    path('', UserLandView.as_view(),name='user_land_list')
]