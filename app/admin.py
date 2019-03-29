from django.contrib import admin
from .models import Contact
# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'email', 'info', 'phone','date_added')
    list_editable = ('info',)
    list_per_page = 5
    search_fields = ('name','gender','email','info','phone')
    list_filter = ('gender','date_added')


admin.site.register(Contact,ContactAdmin)
