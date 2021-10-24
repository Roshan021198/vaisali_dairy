from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name='index'),

    path('dashboard/',views.dashboard,name='dashboard'),
    path('user/',views.user,name='user'),
    path('portfolio/',views.portfolio,name='portfolio'),
    path('deliverytab/',views.deliverytab,name='deliverytab'),
]