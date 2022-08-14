from . import views
from django.urls import path

urlpatterns = [
    path('register_user',views.register_user,name='register-user'),
    path('login_user',views.login_user,name='login'),
    path('logout_user',views.logout_user,name='logout'),
]