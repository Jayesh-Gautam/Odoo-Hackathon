from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Expense, ApprovalLog
from .serializers import ApprovalLogSerializer, ApprovalActionSerializer
from .engine import ApprovalEngine

class ApprovalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for viewing pending approvals and taking action.
    """
    serializer_class = ApprovalLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all pending approvals
        for the currently authenticated user.
        """
        return ApprovalLog.objects.filter(approver=self.request.user, status='pending')

    def action(self, request, pk=None):
        """
        Approve or reject an expense.
        'pk' here is the ID of the ApprovalLog entry.
        """
        try:
            log = ApprovalLog.objects.get(pk=pk, approver=request.user, status='pending')
        except ApprovalLog.DoesNotExist:
            return Response({'error': 'Pending approval not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ApprovalActionSerializer(data=request.data)
        if serializer.is_valid():
            user_action = serializer.validated_data['action']
            comment = serializer.validated_data.get('comment', '')
            
            ApprovalEngine.process_action(log, user_action, comment)
            
            return Response({'status': f'Expense has been {user_action}d.'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
