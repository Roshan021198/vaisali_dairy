from django.urls import path,include
from . import views
urlpatterns = [
    path('dashboard_login/',views.dashboard_login,name='dashboard_login'),
    path('logout',views.logout,name='logout'),

    path('sign_up/',views.sign_up,name='sign_up'),
    path('customerAccount/',views.customerAccount,name='customerAccount'),
    path('delivery_account/',views.delivery_account,name='delivery_account'),

    path('verify_uname/',views.verify_uname,name='verify_uname'),
    path('uname_pwd_check/',views.uname_pwd_check,name='uname_pwd_check'),

    path('forget_username',views.forget_username,name='forget_username'),
    path('forget_email_sending',views.forget_email_sending,name='forget_email_sending'),
    path('set_password',views.set_password,name='set_password'),


    path('verify_otp',views.verify_otp,name='verify_otp'),
]