import re
from django.db import reset_queries
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404,JsonResponse, request, response
from useraccount.models import Account,Deliveryperson,Customer,Transcation,Mainadmin,moneyTransaction,MilkValue
from django.contrib.auth.decorators import login_required


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
        customers = Customer.objects.filter(delivery_boy=delivery_obj).order_by('-pk')
        transactions = Transcation.objects.filter(delivery_per_uid=delivery_obj.emp_id).order_by('-pk')
        total_bottles = request.user.deliveryperson_set.all()[0].bottle_assigned
        milkValue = MilkValue.objects.all()
        print(type(total_bottles))
        return render(request,'delivery-dashboard.html',{'customers':customers,'transactions':transactions,'total_bottles':total_bottles,'milkValue':milkValue})
    elif request.user.is_authenticated and request.user.is_customer:
        customer_obj = request.user.customer_set.first()
        transactions = Transcation.objects.filter(connect_customer=customer_obj).order_by('-pk')
        bottles = customer_obj.bottle_numbers
        return render(request,'customer-dashboard.html',{'transactions':transactions,'bottles':bottles})
    else:
        print("-----")
        return render(request,'signin.html')


@login_required
def user(request):
    obj = request.user
    print(obj.deliveryperson_set.first(),"=================")
    return render(request,'user.html')

@login_required  
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

@login_required
def customer_wallet(request):
    if request.user.is_customer:
        customer_obj = request.user.customer_set.first()
        money_transactions = moneyTransaction.objects.filter(customer_obj=customer_obj).order_by('-pk')
        return render(request,'customer_wallet.html',{'money_transactions':money_transactions,'customer_obj':customer_obj})
    else:
        return render(request,'error.html')

@login_required
def deliverytab(request):
    values = Deliveryperson.objects.all().order_by('-pk')
    total_bottle = request.user.mainadmin_set.all()[0].bottle_numbers
    assigned_bottle = request.user.mainadmin_set.all()[0].assigned_bottle
    return render(request,'delivery.html',{'values':values,'total_bottle':total_bottle,'assigned_bottle':assigned_bottle})




@login_required
def add_delivery(request):
    print("========hello")
    if request.method == 'POST':
        print("hi")
        from_val = request.POST.get('name_from')
        print(from_val)
        from_obj = get_object_or_404(Deliveryperson,pk=int(from_val))
        delivery_per_name = from_obj.name
        delivery_per_uid =  from_obj.emp_id
        customer_pk = request.POST.get('customer_obj')
        cust_obj = get_object_or_404(Customer,pk=int(customer_pk))
        milkvalue_pk = request.POST.get('milkvalue')
        print(milkvalue_pk)
        quantity_obj = get_object_or_404(MilkValue,pk=int(milkvalue_pk))
        quantity =  quantity_obj.quantity
        price = quantity_obj.price
        bottle_given = request.POST.get('bottle_given')
        bottle_nos = '0'
        if bottle_given == "Yes":
            bottle_nos = request.POST.get('bottle_nos')
            if bottle_nos == '':
                bottle_nos = '0'
            cust_bottle = int(cust_obj.bottle_numbers) + int(bottle_nos)
            cust_obj.update_bottle_details(cust_bottle)
            from_bottle = int(from_obj.bottle_assigned) - int(bottle_nos)
            from_obj.update_delivery_bottle(from_bottle)
            bottle_taken = True
        else:
            bottle_taken = False

        money = int(cust_obj.money) - int(price)
        cust_obj.update_transaction_money(money)

        transaction_obj = Transcation.objects.create(delivery_per_name=delivery_per_name,delivery_per_uid=delivery_per_uid,connect_customer=cust_obj,quantity=quantity,price=price,bottle_taken=bottle_taken,bottle_nums=bottle_nos)
        transaction_obj.save()

        return redirect('dashboard')
    return redirect('dashboard')



@login_required
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

@login_required
def complete_transaction(request,pk):
    transaction_obj = get_object_or_404(Transcation,pk=pk)
    print(request.user.is_superadmin,"---------------------")
    if request.user.is_superadmin:
        if request.method == 'POST':
            final_message = request.POST.get('final_message',None)
            if final_message == '':
                final_message = 'Thank You'
                print(final_message)
            print(final_message)
            transaction_obj.completeTransaction(final_message=final_message)
        return redirect(dashboard)
    else:
        return render(request,'error.html')


@login_required
def individual_customer(request,pk):
    customer_obj = get_object_or_404(Customer,pk=pk)
    transactions = Transcation.objects.filter(connect_customer=customer_obj).order_by('-pk')
    money_transactions = moneyTransaction.objects.filter(customer_obj=customer_obj).order_by('-pk')
    return render(request,'individual-customer.html',{'customer_obj':customer_obj,'transactions':transactions,'money_transactions':money_transactions})


@login_required
def individual_delivery_person(request,pk):
    delivery_obj = get_object_or_404(Deliveryperson,pk=pk)
    print(delivery_obj,"================")
    customers = Customer.objects.filter(delivery_boy=delivery_obj).order_by('-pk')
    print(delivery_obj,customers)
    return render(request,'individual-delivery-person.html',{'delivery_obj':delivery_obj,'customers':customers})



@login_required
def update_customer_bottle(request,pk):
    if request.user.is_delivery:
        tran_obj = get_object_or_404(Transcation,pk=pk)
        print(pk)
        customer_obj = tran_obj.connect_customer
        delivery_obj = Deliveryperson.objects.filter(emp_id=tran_obj.delivery_per_uid)[0]
        cust_bottle = int(customer_obj.bottle_numbers) - int(tran_obj.bottle_nums)
        delivery_bottle = int(delivery_obj.bottle_assigned) + int(tran_obj.bottle_nums)
        tran_obj.update_transaction_bottle('0')
        customer_obj.update_bottle_details(str(cust_bottle))
        delivery_obj.update_delivery_bottle(str(delivery_bottle))
        return redirect('individual_customer',pk=customer_obj.pk)
    else:
        return render(request,'error.html')



@login_required
def addMoney(request,pk):
    if request.user.is_delivery:
        customer_obj = get_object_or_404(Customer,pk=pk)
        if request.method == 'POST':
            addmoney = request.POST.get('add_money')
            transaction_type = request.POST.get('transaction_type')
            transaction_id = request.POST.get('transaction_id')
            cus_money = int(customer_obj.money) + int(addmoney)
            customer_obj.update_transaction_money(cus_money)
            transaction_registered_by = request.user.deliveryperson_set.first().name + request.user.deliveryperson_set.first().emp_id
            money_obj = moneyTransaction.objects.create(customer_obj=customer_obj,money_add=addmoney,remaining_amount=str(cus_money),transaction_type=transaction_type,transaction_id=transaction_id,transaction_registered_by=transaction_registered_by)
            money_obj.save()
        return redirect('individual_customer',pk=pk)
    else:
        return render(request,'error.html')