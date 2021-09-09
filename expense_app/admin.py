from .models import *
from django.contrib import admin

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'account_type', 'name')
    list_filter = ['user_id']

class EntryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'must_deduct', 'must_add')

class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'name', 'amount', 'user_id')
    list_filter = ['user_id']

# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(Account_type)
admin.site.register(Entry_type, EntryTypeAdmin)
admin.site.register(Entry_type_category)
admin.site.register(Entry, EntryAdmin)