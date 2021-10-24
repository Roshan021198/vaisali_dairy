from django.db import reset_queries
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404,JsonResponse, response
from useraccount.models import Account,Deliveryperson,Customer,Transcation

# Create your views here.
def index(request):
    return render(request,'index_base.html')


def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superadmin:
            print(request.user)
            return render(request,'admin-dashboard.html')
    else:
        print("-----")
        return render(request,'login.html')



def user(request):
    return render(request,'user.html')
    
def portfolio(request):
    return render(request,'customer.html')

def deliverytab(request):
    return render(request,'delivery.html')
