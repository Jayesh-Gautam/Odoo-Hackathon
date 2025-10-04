from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Auth views
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Profile view
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),

    # Dashboard placeholder views
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    path('dashboard/employee/', views.employee_dashboard, name='employee_dashboard'),

    # Edit employee role
    path('employee/edit/<int:pk>/', views.edit_employee_role, name='edit_employee_role'),

    # Root path now redirects to the correct dashboard
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('', views.dashboard_redirect, name='accounts-home'),
]
