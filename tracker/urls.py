from django.urls import path
from .api.views import CustomerRegisterView,LoginView,Decline,Approve,CreateApplication,AdminLandView,UserLandView

urlpatterns=[
 path('register/',CustomerRegisterView.as_view(),name="register"),
 path('login/',LoginView.as_view(),name='login'),
 path('admin_list/',AdminLandView.as_view()),
 path('customer_list/',UserLandView.as_view()),
 path('create_app/',CreateApplication.as_view()),
 path('approve/',Approve.as_view(),name='approve'),
 path('decline/',Decline.as_view(),name='decline')
]