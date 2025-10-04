from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.SubmitExpenseView.as_view(), name='submit_expense'),
    path('history/', views.ExpenseHistoryView.as_view(), name='expense_history'),
    path('<int:pk>/', views.ExpenseDetailView.as_view(), name='expense_detail'),
]