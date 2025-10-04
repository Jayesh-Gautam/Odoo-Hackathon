from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction

from .models import CustomUser, Company
from .forms import CustomUserCreationForm, ProfileUpdateForm, EditRoleForm


class SignupView(CreateView):
    """
    Handles user registration.
    Creates a new Company and an Admin user for that company.
    """
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    @transaction.atomic
    def form_valid(self, form):
        # Create the company first
        company_name = form.cleaned_data.get('company_name')
        # Now, save the user
        user = form.save(commit=False)

        if Company.objects.filter(name=company_name).exists():
            company = Company.objects.get(name=company_name)
            user.role = CustomUser.Role.EMPLOYEE
        else:
            company = Company.objects.create(name=company_name)
            user.role = CustomUser.Role.ADMIN

        user.is_staff = True  # Admins should have staff access
        user.company = company
        user.save()

        self.object = user
        return redirect(self.get_success_url())


class LoginView(BaseLoginView):
    """
    Handles user login and redirects based on their role.
    """
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == CustomUser.Role.ADMIN:
            return reverse_lazy('admin_dashboard')
        elif user.role == CustomUser.Role.MANAGER:
            return reverse_lazy('manager_dashboard')
        else:  # Employee
            return reverse_lazy('employee_dashboard')


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows users to view and update their profile.
    Admins/Managers can also assign managers to other users in their company.
    """
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})

    def test_func(self):
        """
        Check if the request user has permission to view this profile.
        - A user can always view their own profile.
        - An Admin/Manager can view profiles of users in their own company.
        """
        profile_user = self.get_object()
        request_user = self.request.user

        if request_user == profile_user:
            return True

        if request_user.company == profile_user.company and \
                (request_user.role in [CustomUser.Role.ADMIN, CustomUser.Role.MANAGER]):
            return True

        return False

    def get_form_kwargs(self):
        """Pass the request user to the form."""
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs


@login_required
def dashboard_redirect(request):
    """
    Redirects user to their respective dashboard based on their role.
    """
    user = request.user
    if user.role == CustomUser.Role.ADMIN:
        return redirect(reverse('admin_dashboard'))
    elif user.role == CustomUser.Role.MANAGER:
        return redirect(reverse('manager_dashboard'))
    else:  # Employee
        return redirect(reverse('employee_dashboard'))


# --- Placeholder Dashboard Views ---
# In a real app, these would be more complex views.

@login_required
@user_passes_test(lambda u: u.role == CustomUser.Role.ADMIN)
def admin_dashboard(request):
    company = request.user.company
    employees = CustomUser.objects.filter(company=company)
    return render(request, 'accounts/admin_dashboard.html', {'employees': employees})


@login_required
@user_passes_test(lambda u: u.role in [CustomUser.Role.MANAGER, CustomUser.Role.ADMIN])
def manager_dashboard(request):
    subordinates = request.user.subordinates.all()
    return render(request, 'accounts/manager_dashboard.html', {'subordinates': subordinates})


def employee_dashboard(request):
    return render(request, 'accounts/dashboard.html', {'role': 'Employee'})


@login_required
@user_passes_test(lambda u: u.role == CustomUser.Role.ADMIN)
def edit_employee_role(request, pk):
    employee = get_object_or_404(CustomUser, pk=pk, company=request.user.company)
    if request.method == 'POST':
        form = EditRoleForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = EditRoleForm(instance=employee)
    return render(request, 'accounts/edit_employee_role.html', {'form': form, 'employee': employee})

