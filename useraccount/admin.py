from django.contrib import admin
from .models import Account,Deliveryperson,Customer,Transcation,Mainadmin,moneyTransaction,MilkValue

admin.site.register(Account)
admin.site.register(Deliveryperson)
admin.site.register(Customer)
admin.site.register(Transcation)
admin.site.register(Mainadmin)
admin.site.register(moneyTransaction)
admin.site.register(MilkValue)