from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Expense, Report, UserProfile
from .serializers import ExpenseSerializer, ReportSerializer
from .permissions import IsOwner, IsManager


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for employees to view and manage their expenses.
    """
    serializer_class = ExpenseSerializer  # This line is now uncommented
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """ This view should only return expenses for the currently authenticated user. """
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """ Automatically associate the expense with the logged-in user. """
        serializer.save(user=self.request.user)


class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint for employees to create reports and for managers to review them.
    """
    serializer_class = ReportSerializer # This line is now uncommented
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Employees see reports they created.
        Managers see all reports for now (can be refined to their team).
        """
        user = self.request.user
        if user.profile.role == 'manager':
            # A manager might see reports submitted to them
            return Report.objects.filter(manager=user)
        # An employee sees reports they have submitted
        return Report.objects.filter(user=user)

    def perform_create(self, serializer):
        """ Automatically set the user when a report is created. """
        # Ensure that the manager being assigned is actually a manager
        manager_id = self.request.data.get('manager')
        try:
            manager = User.objects.get(id=manager_id, profile__role='manager')
            serializer.save(user=self.request.user, manager=manager)
        except User.DoesNotExist:
            raise serializers.ValidationError("The assigned manager is not valid.")


    @action(detail=True, methods=['post'], permission_classes=[IsManager])
    def approve(self, request, pk=None):
        """ Custom action for a manager to approve a report. """
        report = self.get_object()
        if report.manager != request.user:
            return Response(
                {'error': 'You are not authorized to approve this report.'},
                status=status.HTTP_403_FORBIDDEN
            )
        report.status = 'approved'
        report.save()
        # Also mark all related expenses as 'approved'
        report.expenses.update(status='approved')
        return Response({'status': 'Report approved'})

    @action(detail=True, methods=['post'], permission_classes=[IsManager])
    def reject(self, request, pk=None):
        """ Custom action for a manager to reject a report. """
        report = self.get_object()
        if report.manager != request.user:
            return Response(
                {'error': 'You are not authorized to reject this report.'},
                status=status.HTTP_403_FORBIDDEN
            )
        report.status = 'rejected'
        report.save()
        # Optionally, set related expenses back to 'pending' or a 'rejected' state
        report.expenses.update(status='rejected')
        return Response({'status': 'Report rejected'})


# =============================================================================
# 5. URLS (Place this in your `urls.py` file)
# =============================================================================
#
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ExpenseViewSet, ReportViewSet
#
# router = DefaultRouter()
# router.register(r'expenses', ExpenseViewSet, basename='expense')
# router.register(r'reports', ReportViewSet, basename='report')
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]
#

