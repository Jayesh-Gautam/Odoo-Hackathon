from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from expenses.models import Expense
from .models import Approval
from .forms import ReviewForm
from accounts.models import CustomUser


def _update_expense_status(expense):
    """
    Checks the current approvals for an expense and updates its status
    based on the 60% approval / 40%+ rejection rule.
    """
    employee = expense.employee
    total_managers = employee.managers.count()

    if total_managers == 0:
        expense.status = 'APPROVED'
        expense.save()
        return

    approvals = expense.approvals.all()
    approved_count = approvals.filter(decision=Approval.Decision.APPROVED).count()
    rejected_count = approvals.filter(decision=Approval.Decision.REJECTED).count()

    approval_percentage = (approved_count / total_managers) * 100
    rejection_percentage = (rejected_count / total_managers) * 100

    if approval_percentage >= 60:
        expense.status = 'APPROVED'
    elif rejection_percentage > 40:
        expense.status = 'REJECTED'
    else:
        expense.status = 'PENDING'

    expense.save()

class ExpenseApprovalView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role not in [CustomUser.Role.ADMIN, CustomUser.Role.MANAGER]:
            return redirect('dashboard_redirect')

        subordinates = request.user.subordinates.all()

        pending_expenses = Expense.objects.filter(
            employee__in=subordinates,
            status='PENDING'
        ).exclude(
            approvals__manager=request.user
        )

        return render(request, 'approvals/expense_approval_list.html', {'expenses': pending_expenses})


class ApprovalHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role not in [CustomUser.Role.ADMIN, CustomUser.Role.MANAGER]:
            return redirect('dashboard_redirect')

        reviewed_expenses = Expense.objects.filter(approvals__manager=request.user).distinct()

        return render(request, 'approvals/approval_history.html', {'expenses': reviewed_expenses})


class ReviewExpenseView(LoginRequiredMixin, View):
    def get(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id)
        if expense.approvals.filter(manager=request.user).exists():
            return redirect('expense_approvals')

        form = ReviewForm()

        # Calculate counts in the view
        approved_count = expense.approvals.filter(decision='APPROVED').count()
        rejected_count = expense.approvals.filter(decision='REJECTED').count()

        context = {
            'expense': expense,
            'form': form,
            'approved_count': approved_count,
            'rejected_count': rejected_count,
        }
        return render(request, 'approvals/review_expense.html', context)

    def post(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id)
        form = ReviewForm(request.POST)

        if form.is_valid():
            decision = form.cleaned_data['decision']
            comments = form.cleaned_data['comments']

            Approval.objects.create(
                expense=expense,
                manager=request.user,
                decision=decision,
                comments=comments
            )

            _update_expense_status(expense)

            return redirect('expense_approvals')

        # Recalculate counts for the context if the form is invalid
        approved_count = expense.approvals.filter(decision='APPROVED').count()
        rejected_count = expense.approvals.filter(decision='REJECTED').count()

        context = {
            'expense': expense,
            'form': form,
            'approved_count': approved_count,
            'rejected_count': rejected_count,
        }
        return render(request, 'approvals/review_expense.html', context)