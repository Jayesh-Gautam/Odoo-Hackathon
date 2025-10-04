from rest_framework import serializers
from .models import ApprovalFlow, ApprovalStep, ApprovalRule, ApprovalLog

class ApprovalStepSerializer(serializers.ModelSerializer):
    approver = serializers.StringRelatedField()
    class Meta:
        model = ApprovalStep
        fields = ('approver', 'sequence')

class ApprovalFlowSerializer(serializers.ModelSerializer):
    steps = ApprovalStepSerializer(many=True, read_only=True)
    class Meta:
        model = ApprovalFlow
        fields = '__all__'

class ApprovalRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRule
        fields = '__all__'

class ApprovalLogSerializer(serializers.ModelSerializer):
    approver = serializers.StringRelatedField()
    expense_title = serializers.CharField(source='expense.title', read_only=True)
    class Meta:
        model = ApprovalLog
        fields = ('id', 'expense', 'expense_title', 'approver', 'status', 'comment', 'timestamp', 'step')

class ApprovalActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    comment = serializers.CharField(required=False, allow_blank=True, max_length=500)
