from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404,JsonResponse, response
from django.contrib.auth.models import auth

# from vaisali.home.views import customer

from .models import Account,Customer,Deliveryperson,Mainadmin
import requests
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    return render(request,'signup.html')


def customerAccount(request):
    if request.method == 'POST':
        name = request.POST.get('name',None)
        contact_no = request.POST.get('contact_no',None)
        address = request.POST.get('address',None)
        email = request.POST.get('email',None)
        if not email:
            email = "panigrahi.babu98@gmail.com"
        id_proof = request.POST.get('id_proof',None)
        password = request.POST.get('password',None)
        profile_img = request.FILES.get('profile_img',None)
        if profile_img == None:
            profile_img = 'customerimg/profile_image.png'

        print(name,contact_no,address,id_proof,password)

        if not name or not contact_no or not address or not id_proof or not password:
            return render(request,'error.html')

        account_obj = Account.objects.create_user(username=contact_no,is_temporary=True)
        account_obj.set_password(password)
        account_obj.save()

        previous_ids = Customer.objects.all()
        if previous_ids:
            previous_id = previous_ids.last().customer_id
            customer_id = 'DS/CUS/' + "{:05d}".format(int(previous_id[7:]) + 1)
        else:
            customer_id = 'DS/CUS/00001'

        customer_obj = Customer.objects.create(account=account_obj,name=name,contact_no=contact_no,email=email,profile_img=profile_img,id_proof=id_proof,address=address,customer_id=customer_id)
        customer_obj.save()
        return redirect(sign_up)
    return redirect(sign_up)

@login_required
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
        bottle_assigned = request.POST.get('bottle_assigned')
        print(int(bottle_assigned) + 1 )
        print(type(request.user.mainadmin_set.all()[0].bottle_numbers))
        print(request.user.mainadmin_set.all()[0].bottle_numbers)

        if profile_img == None:
            profile_img = 'deliveryboy/profile_image.png'
        account_obj = Account.objects.create_user(username=contact_no,is_delivery=True)
        account_obj.set_password(password)
        account_obj.save()

        previous_ids = Deliveryperson.objects.all()
        if previous_ids:
            previous_id = previous_ids.last().emp_id
            emp_id = 'DS/EMP/' + "{:03d}".format(int(previous_id[7:]) + 1)
        else:
            emp_id = 'DS/EMP/001'

        emp_obj = Deliveryperson.objects.create(account=account_obj,name=name,contact_no=contact_no,email=email,profile_img=profile_img,id_proof=id_proof,address=address,emp_id=emp_id,location=location,bottle_assigned=bottle_assigned,original_bottle_assigned=bottle_assigned)
        emp_obj.save()
        bottle_numbers = int(request.user.mainadmin_set.all()[0].bottle_numbers) - int(bottle_assigned)
        print(bottle_numbers,"----------")
        assigned_bottle = int(request.user.mainadmin_set.all()[0].assigned_bottle) + int(bottle_assigned)
        print(assigned_bottle,'+++++====++++')
        request.user.mainadmin_set.all()[0].update_bottle_nos(str(bottle_numbers),str(assigned_bottle))
        return redirect("deliverytab")
    return redirect("deliverytab")


def verify_login_uname(request):
    uname = request.GET.get('uname',None)
    account_obj = Account.objects.filter(username = uname)
    print(account_obj,'avc')
    
    if len(account_obj) > 0:
        print("positive")
        if account_obj[0].is_temporary:
            data = {
                'exist': Account.objects.filter(username = uname).exists(),
                'message':'customer'
            }
        else:
            data = {
                'exist': Account.objects.filter(username = uname).exists(),
                'message':'normal'
            }
    else:
        print("negative")
        data = {
            'exist': None,
        }

    return JsonResponse(data)



def verify_uname(request):
    uname = request.GET.get('uname',None)
    print(uname,"------------------------")
    account_obj = Account.objects.filter(username = uname)
    print(account_obj)
    
    if account_obj :
    # if len(account_obj) > 0 and (account_obj[0].is_customer or account_obj[0].is_superadmin or account_obj[0].is_delivery):
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




@login_required
def update_customer(request,pk):
    customer_obj = get_object_or_404(Customer,pk=pk)
    if request.method == 'POST':
        unique_pk = request.POST.get('deli_obj')
        delivery_obj = Deliveryperson.objects.filter(pk=unique_pk)
        customer_obj.account.update_customer_account()
        customer_obj.update_request(obj=delivery_obj[0])
        return redirect('customer')
    return redirect('customer')

@login_required
def newDeliveryToCustomer(request,pk):
    customer_obj = get_object_or_404(Customer,pk=pk)
    if request.method == 'POST':
        unique_pk = request.POST.get('deli_obj')
        delivery_obj = Deliveryperson.objects.filter(pk=unique_pk)
        customer_obj.update_request(obj=delivery_obj[0])
        return redirect('customer')
    return redirect('customer')


@login_required
def delete_customer(request,pk):
    customer_obj = get_object_or_404(Customer,pk=pk)
    account_obj = customer_obj.account
    account_obj.delete()
    return redirect('customer')


@login_required
def delete_employee(request,pk):
    if request.user.is_superadmin:
        emp_obj = get_object_or_404(Deliveryperson,pk=pk)
        account_obj = emp_obj.account
        account_obj.delete()
        return redirect('delivery_account')
    return redirect('delivery_account')

@login_required
def edit_employee(request,pk):
    if request.user.is_superadmin:
        emp_obj = get_object_or_404(Deliveryperson,pk=pk)
        if request.method == 'POST':
            bottle = request.POST.get('bottle')
            print(bottle)
            unchanged_bottle = int(emp_obj.original_bottle_assigned) + int(bottle)
            changed_bottle = int(emp_obj.bottle_assigned) + int(bottle)
            admin_obj = request.user.mainadmin_set.first()
            admin_bottle_size = int(admin_obj.bottle_numbers) - int(bottle)
            admin_bottle_assigned = int(admin_obj.assigned_bottle) + int(bottle)
            admin_obj.update_bottle_nos(str(admin_bottle_size),str(admin_bottle_assigned))
            emp_obj.edit_delivery_account(str(unchanged_bottle),str(changed_bottle))
        return redirect('delivery_account')
    return redirect('delivery_account')


