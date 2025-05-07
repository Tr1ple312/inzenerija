from django.contrib import admin
from testsite.models import Transaction, Category


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'amount', 'transaction_type', 'transaction_date')
    list_editable = ('amount', 'transaction_type')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_editable = ('name',)