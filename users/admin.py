from django.contrib import admin

from users.models import User, Payment

admin.site.register(User)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_date',)