from django.contrib import admin
from .models import Expense, ExpenseCategory, Receipt

admin.site.register(Expense)
admin.site.register(ExpenseCategory)
admin.site.register(Receipt)