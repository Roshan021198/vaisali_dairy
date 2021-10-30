from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name='index'),

    path('dashboard/',views.dashboard,name='dashboard'),
    path('user/',views.user,name='user'),
    path('customer/',views.customer,name='customer'),
    path('deliverytab/',views.deliverytab,name='deliverytab'),

    path('add_delivery/',views.add_delivery,name='add_delivery'),

    path('update_transaction/<int:pk>/',views.update_transaction,name='update_transaction'),
    path('complete_transaction/<int:pk>/',views.complete_transaction,name='complete_transaction'),

    path('individual_customer/<int:pk>/',views.individual_customer,name='individual_customer'),
    path('individual_delivery_person/<int:pk>/',views.individual_delivery_person,name='individual_delivery_person'),
]