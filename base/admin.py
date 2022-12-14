from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email','full_name','date_joined','last_login','is_admin','is_staff',)
    search_fields = ('email','full_name')
    readonly_fields = ('id','date_joined','last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    ordering = ('email',)

    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email','full_name', 'password1', 'password2'),
    }),
)

admin.site.register(Account,AccountAdmin)