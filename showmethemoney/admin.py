from django.contrib import admin
from models import Transaction
class TransactionAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('timestamp', 'id', 'event', 'amount', 'comment')
    list_display_links = ('timestamp', 'id')
    list_filter = ('subscription', 'user')
admin.site.register(Transaction, TransactionAdmin)
