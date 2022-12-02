from django.contrib import admin
from account.models import Wallet
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class WalletInline(admin.StackedInline):
    model = Wallet
    #list_display = ['name','money',]
    can_delete = False
    verbose_name = 'Wallets'
class CustomizeUserAdmin(UserAdmin):
    inlines = (WalletInline,)
admin.site.unregister(User)
admin.site.register(User,CustomizeUserAdmin)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user','money','peticion']

#@admin.register(User)
#class wallet(admin.ModelAdmin):
#    search_fields = ['name']
    #list_display: ['name']