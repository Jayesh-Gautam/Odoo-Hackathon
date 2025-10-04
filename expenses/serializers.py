from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Expense, Report, UserProfile

class UserSerializer(serializers.ModelSerializer):
    """ Serializer for User details. """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ExpenseSerializer(serializers.ModelSerializer):
    """ Serializer for the Expense model. """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Expense
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    """ Serializer for the Report model. """
    user = UserSerializer(read_only=True)
    total_amount = serializers.ReadOnlyField()
    expenses = ExpenseSerializer(many=True, read_only=True) # Show detailed expenses
    expense_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Expense.objects.all(), source='expenses'
    )

    class Meta:
        model = Report
        fields = [
            'id', 'name', 'user', 'manager', 'start_date', 'end_date',
            'comments', 'status', 'total_amount', 'submitted_at', 'expenses', 'expense_ids'
        ]