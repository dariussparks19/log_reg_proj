from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('login_user', views.login_user),
    path('logout', views.logout),
    path('success', views.dashboard)
]
