from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404,JsonResponse, response
from django.contrib.auth.models import auth

from .models import Account,Customer,Deliveryperson,Mainadmin
import requests
import random
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.
def dashboard_login(request):
    if request.method == "POST":
        username = request.POST['contact_no']
        password = request.POST['password']
        user = auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("dashboard")
        else:
            return redirect('dashboard_login')
    else:
        return redirect(dashboard_login)

def logout(request):
    auth.logout(request)
    return redirect('dashboard')



def sign_up(request):
    return render(request,'sign-up.html')



def customerAccount(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact_no = request.POST.get('phone_number')
        address = request.POST.get('address',None)
        email = request.POST.get('email',None)
        id_proof = request.POST.get('id_proof',None)
        password = request.POST.get('password',None)
        profile_img = request.FILES.get('profile_img',None)

        account_obj = Account.objects.create_user(username=contact_no)
        account_obj.set_password(password)
        account_obj.save()

        customer_id = 'VD/' + "{:06d}".format(len(Customer.objects.all()) + 1)

        customer_obj = Customer.objects.create(account=account_obj,name=name,contact_no=contact_no,email=email,profile_img=profile_img,id_proof=id_proof,address=address,customer_id=customer_id)
        customer_obj.save()
        return redirect(sign_up)
    return redirect(sign_up)


def delivery_account(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact_no = request.POST.get('contact_no')
        email = request.POST.get('email')
        id_proof = request.POST.get('id_proof')
        location = request.POST.get('location')
        address = request.POST.get('address')
        password = request.POST.get('password')
        profile_img = request.FILES.get('profile_img',None)
        account_obj = Account.objects.create_user(username=contact_no,is_delivery=True)
        account_obj.set_password(password)
        account_obj.save()

        emp_id = 'VD/EMP/' + "{:03d}".format(len(Customer.objects.all()) + 1)

        emp_obj = Deliveryperson.objects.create(account=account_obj,name=name,contact_no=contact_no,email=email,profile_img=profile_img,id_proof=id_proof,address=address,emp_id=emp_id,location=location)
        emp_obj.save()
        return redirect("deliverytab")
    return redirect("deliverytab")






def verify_uname(request):
    uname = request.GET.get('uname',None)
    print(uname,"------------------------")
    account_obj = Account.objects.filter(username = uname)
    print(account_obj)
    
    if len(account_obj) > 0 and (account_obj[0].is_customer or account_obj[0].is_superadmin or account_obj[0].is_delivery):
        print("positive")
        data = {
            'exist': Account.objects.filter(username = uname).exists(),
        }
    else:
        print("negative")
        data = {
            'exist': None,
        }

    return JsonResponse(data)
        

def uname_pwd_check(request):
    uname = request.GET.get('uname',None)
    pwd = request.GET.get('pwd',None)
    user = auth.authenticate(request,username=uname,password=pwd)
    exist = False
    if user is not None:
        exist = True
    
    else:
        exist = False

    
    data = {
        'exist':exist
    }
    return JsonResponse(data)



def forget_username(request):
    uname = request.GET.get('uname',None)
    user = Account.objects.filter(username=uname).first()
    print(user,"++++++++++++++")
    if user is not None:
        if user.is_customer:
            cust = user.customer_set.first()
            email = cust.email
            type = 'customer'
        if user.is_delivery:
            deliveryperson = user.deliveryperson_set.first()
            email = deliveryperson.email
            type = 'deliveryperson'
        if user.is_superadmin:
            admin = user.mainadmin_set.first()
            email = admin.email
            type = 'mainadmin'

    else:
        email = None
        type = None
    data = {
        'is_exist': Account.objects.filter(username=uname).exists(),
        'email':email,
        'type':type,
    }
    return JsonResponse(data)


def forget_email_sending(request):
    email = request.GET.get('email',None)
    num_list = ['1','2','3','4','5','6','7','8','9']
    otp = random.sample(num_list,6)
    str_otp = ''.join(otp)
    print("check --------- check")
    request.session['strOTP'] = str_otp
    print("check --------- check")
    
    send_mail(
    'Password Reset OTP',
    'Your one time password to reset Vasali Dairy account is :{0}'.format(str_otp),
    'support@aicnalanda.com',
    [email],
    fail_silently=False,
    )
    data = {
        'correct_otp':str_otp
    }
    return JsonResponse(data)



def verify_otp(request):
    input_otp = request.GET.get('entred_otp',None)
    correct_otp = request.session['strOTP']
    flag = 'false'
    if input_otp==correct_otp:
        flag = 'true'

    data = {
        'exist': flag,
    }
    return JsonResponse(data)

def set_password(request):
    password = request.GET.get('password',None)
    uname = request.GET.get('username',None)
    user = Account.objects.get(username=uname)
   
    user.set_password(password)
    user.save()
    data = {
        'uname':uname
    }
    return JsonResponse(data)