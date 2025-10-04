from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
# You will need to import your actual models once you create them in models.py
# from .models import UserProfile, Expense, Report

# NOTE: For these tests to run, you must first move the model definitions
# from your views.py file into your models.py file and create them in the database
# by running `python manage.py makemigrations` and `python manage.py migrate`.


class ExpenseAPITests(APITestCase):
    """
    Test suite for the Expense and Report API endpoints.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        This runs once for the entire test class.
        """
        # Create users: one manager, two employees
        cls.manager = User.objects.create_user(username='manager', password='password123')
        cls.employee1 = User.objects.create_user(username='employee1', password='password123')
        cls.employee2 = User.objects.create_user(username='employee2', password='password123')

        # Create UserProfiles to assign roles
        # Assuming UserProfile model is in the same app's models.py
        # UserProfile.objects.create(user=cls.manager, role='manager')
        # UserProfile.objects.create(user=cls.employee1, role='employee', manager=cls.manager)
        # UserProfile.objects.create(user=cls.employee2, role='employee', manager=cls.manager)

        # Create a sample expense for employee1
        # cls.expense1 = Expense.objects.create(
        #     user=cls.employee1,
        #     date='2025-10-04',
        #     category='food',
        #     amount=50.00,
        #     description='Team lunch'
        # )

    def test_create_expense_unauthenticated(self):
        """
        Ensure unauthenticated users cannot create expenses.
        """
        url = reverse('expense-list') # Assumes you named your route 'expense' in urls.py
        data = {'date': '2025-10-05', 'category': 'travel', 'amount': 250.00, 'description': 'Flight ticket'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_and_view_own_expense(self):
        """
        Ensure an authenticated user can create and view their own expense.
        """
        # NOTE: This test will fail until the models are created and setUpTestData is uncommented.
        self.client.login(username='employee1', password='password123')
        
        # Create a new expense
        create_url = reverse('expense-list')
        data = {'date': '2025-10-05', 'category': 'travel', 'amount': 300.00, 'description': 'Hotel booking'}
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['amount'], '300.00')

        # Verify employee1 can see their own expenses but not others'
        list_url = reverse('expense-list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 2) # Should see the one from setUp and the new one
        # self.assertEqual(response.data[0]['user'], 'employee1')

    def test_cannot_view_other_user_expense(self):
        """
        Ensure a user cannot view or access expenses of another user.
        """
        # NOTE: This test will fail until the models are created and setUpTestData is uncommented.
        self.client.login(username='employee2', password='password123')
        
        # Try to access the detail view of employee1's expense
        # detail_url = reverse('expense-detail', kwargs={'pk': self.expense1.pk})
        # response = self.client.get(detail_url)
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_manager_can_approve_report(self):
        """
        Test that a manager can approve a report submitted to them.
        """
        # NOTE: This test will fail until the models are created and setUpTestData is uncommented.
        self.client.login(username='employee1', password='password123')
        
        # Create a report as employee1
        # report_data = {
        #     'name': 'October Conference',
        #     'start_date': '2025-10-01',
        #     'end_date': '2025-10-05',
        #     'manager': self.manager.pk,
        #     'expense_ids': [self.expense1.pk]
        # }
        # create_report_url = reverse('report-list')
        # response = self.client.post(create_report_url, report_data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # report_id = response.data['id']
        # report = Report.objects.get(id=report_id)
        # self.assertEqual(report.status, 'submitted')

        # # Now, log in as the manager and approve it
        # self.client.login(username='manager', password='password123')
        # approve_url = reverse('report-approve', kwargs={'pk': report_id})
        # response = self.client.post(approve_url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # report.refresh_from_db() # Reload the report data from the database
        # self.assertEqual(report.status, 'approved')
        # self.expense1.refresh_from_db()
        # self.assertEqual(self.expense1.status, 'approved')
