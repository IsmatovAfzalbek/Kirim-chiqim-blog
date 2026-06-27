from django.contrib import admin

from .models import RecurringTransaction, Transaction


admin.site.register(RecurringTransaction)
admin.site.register(Transaction)

