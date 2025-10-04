from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Expense, Receipt
from .forms import ExpenseForm, ReceiptForm
from . import ocr_service

class SubmitExpenseView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/submit_expense.html'

    def get_success_url(self):
        return reverse_lazy('expense_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.employee = self.request.user
        self.object = form.save()

        if self.request.FILES.get('receipt_image'):
            receipt_image = self.request.FILES['receipt_image']
            Receipt.objects.create(expense=self.object, image=receipt_image)
            # The OCR data can be used for pre-filling the form in a more advanced implementation
            ocr_data = ocr_service.extract_text_from_image(receipt_image)
            print("OCR Data:", ocr_data)

        return redirect(self.get_success_url())

class ExpenseHistoryView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_history.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        return Expense.objects.filter(employee=self.request.user)

class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = 'expenses/expense_detail.html'
    context_object_name = 'expense'