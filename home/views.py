import re
from django.db import reset_queries
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404,JsonResponse, response
from useraccount.models import Account,Deliveryperson,Customer,Transcation

# Create your views here.
def index(request):
    return render(request,'index_base.html')


def dashboard(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        transactions = Transcation.objects.all().order_by('-pk')
        customer_approved = Transcation.objects.filter(customer_approval=True)
        pendings = Transcation.objects.filter(customer_approval=False)
        return render(request,'admin-dashboard.html',{'transactions':transactions,'customer_approved':customer_approved,'pendings':pendings})
    elif request.user.is_authenticated and request.user.is_delivery:
        delivery_obj = request.user.deliveryperson_set.first()
        customers = Customer.objects.filter(delivery_boy=delivery_obj)
        transactions = Transcation.objects.filter(from_delivery=delivery_obj).order_by('-pk')
        return render(request,'delivery-dashboard.html',{'customers':customers,'transactions':transactions})
    elif request.user.is_authenticated and request.user.is_customer:
        customer_obj = request.user.customer_set.first()
        transactions = Transcation.objects.filter(connect_customer=customer_obj).order_by('-pk')
        return render(request,'customer-dashboard.html',{'transactions':transactions})
    else:
        print("-----")
        return render(request,'login.html')



def user(request):
    obj = request.user
    print(obj.deliveryperson_set.first(),"=================")
    return render(request,'user.html')
    
def customer(request):
    if request.user.is_superadmin:
        values = Customer.objects.all().order_by('-pk')
        pendings = Customer.objects.filter(request=False).order_by('-pk')
        approvals = Customer.objects.filter(request=True).order_by('-pk')
        deliverPyersons = Deliveryperson.objects.all()
        print(values)
        return render(request,'customer.html',{'values':values,'pendings':pendings,'approvals':approvals,'deliverPyersons':deliverPyersons})
    elif request.user.is_delivery:
        delivery_obj = request.user.deliveryperson_set.first()
        customers = Customer.objects.filter(delivery_boy=delivery_obj)
        print(customers)
        return render(request,'delivery-customer.html',{'customers':customers})

def deliverytab(request):
    values = Deliveryperson.objects.all().order_by('-pk')
    return render(request,'delivery.html',{'values':values})





def add_delivery(request):
    if request.method == 'POST':
        from_val = request.POST.get('name_from')
        print(from_val)
        from_obj = get_object_or_404(Deliveryperson,pk=int(from_val))
        customer_pk = request.POST.get('customer_obj')
        cust_obj = get_object_or_404(Customer,pk=int(customer_pk))
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        transaction_obj = Transcation.objects.create(from_delivery=from_obj,connect_customer=cust_obj,quantity=quantity,price=price)
        transaction_obj.save()

        return redirect('dashboard')
    return redirect('dashboard')




def update_transaction(request,pk):
    transaction_obj = get_object_or_404(Transcation,pk=pk)
    if request.user.is_customer:
        if request.method == 'POST':
            product_status = request.POST.get('product_status')
            customer_message = request.POST.get('customer_message')

            transaction_obj.updateTransaction(remark=product_status,customer_message=customer_message)

            return redirect(dashboard)
    else:
        return render(request,'error.html')


def complete_transaction(request,pk):
    transaction_obj = get_object_or_404(Transcation,pk=pk)
    print(request.user.is_superadmin,"---------------------")
    if request.user.is_superadmin:
        transaction_obj.completeTransaction()
        return redirect(dashboard)
    else:
        return render(request,'error.html')



def individual_customer(request,pk):
    customer_obj = get_object_or_404(Customer,pk=pk)
    transactions = Transcation.objects.filter(connect_customer=customer_obj).order_by('-pk')
    return render(request,'individual-customer.html',{'customer_obj':customer_obj,'transactions':transactions})


def individual_delivery_person(request,pk):
    delivery_obj = get_object_or_404(Deliveryperson,pk=pk)
    print(delivery_obj,"================")
    customers = Customer.objects.filter(delivery_boy=delivery_obj).order_by('-pk')
    print(delivery_obj,customers)
    return render(request,'individual-delivery-person.html',{'delivery_obj':delivery_obj,'customers':customers})


