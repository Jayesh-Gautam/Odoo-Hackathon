from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExpenseApprovalView.as_view(), name='expense_approvals'),
    path('review/<int:expense_id>/', views.ReviewExpenseView.as_view(), name='review_expense'),
    path('history/', views.ApprovalHistoryView.as_view(), name='approval_history'),
]