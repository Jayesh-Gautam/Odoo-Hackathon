from django.urls import path
from .views import ApprovalViewSet

urlpatterns = [
    # Lists pending approvals for the logged-in user
    path('', ApprovalViewSet.as_view({'get': 'list'}), name='pending-approvals-list'),
    
    # Allows an approver to action a pending request
    # The 'pk' is the ID of the ApprovalLog record
    path('<int:pk>/action/', ApprovalViewSet.as_view({'post': 'action'}), name='approval-action'),
]
