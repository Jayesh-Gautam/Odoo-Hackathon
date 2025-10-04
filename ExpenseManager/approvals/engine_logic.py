from .models import ApprovalFlow, ApprovalStep, ApprovalLog, Expense

class ApprovalEngine:
    """
    A service class to handle the logic of the approval process.
    """
    @staticmethod
    def start_approval_flow(expense: Expense):
        """
        Kicks off the approval process for a newly created expense.
        """
        # For now, let's find the default approval flow for the company.
        # A more complex system might determine the flow based on expense type or amount.
        try:
            approval_flow = ApprovalFlow.objects.get(company=expense.submitted_by.company, is_default=True)
        except ApprovalFlow.DoesNotExist:
            # If no default flow, maybe auto-approve or assign to admin?
            # For now, we'll just mark it as approved.
            expense.status = 'approved'
            expense.save()
            return

        expense.approval_flow = approval_flow
        first_step = approval_flow.steps.order_by('sequence').first()

        if first_step:
            expense.current_approver = first_step.approver
            expense.save()
            # Create the first log entry
            ApprovalLog.objects.create(
                expense=expense,
                approver=first_step.approver,
                status='pending',
                step=first_step
            )
        else:
            # No steps in the flow, so approve it.
            expense.status = 'approved'
            expense.save()

    @staticmethod
    def process_action(log: ApprovalLog, action: str, comment: str):
        """
        Processes an 'approve' or 'reject' action from an approver.
        """
        log.status = 'approved' if action == 'approve' else 'rejected'
        log.comment = comment
        log.save()

        expense = log.expense

        if action == 'reject':
            expense.status = 'rejected'
            expense.current_approver = None
            expense.save()
            return

        if action == 'approve':
            # Check for conditional rules first
            if ApprovalEngine.check_conditional_rules(expense):
                ApprovalEngine.finalize_expense(expense, 'approved')
                return

            # Find the next step in the sequence
            current_sequence = log.step.sequence
            next_step = ApprovalStep.objects.filter(
                approval_flow=expense.approval_flow,
                sequence__gt=current_sequence
            ).order_by('sequence').first()

            if next_step:
                # Move to the next approver
                expense.current_approver = next_step.approver
                expense.save()
                ApprovalLog.objects.create(
                    expense=expense,
                    approver=next_step.approver,
                    status='pending',
                    step=next_step
                )
            else:
                # This was the last step, finalize the expense
                ApprovalEngine.finalize_expense(expense, 'approved')

    @staticmethod
    def check_conditional_rules(expense: Expense) -> bool:
        """
        Checks if any conditional approval rules are met.
        Returns True if the expense should be auto-approved, False otherwise.
        """
        # This is where you would implement the logic for percentage, specific approver, etc.
        # This is a placeholder for that complex logic.
        return False

    @staticmethod
    def finalize_expense(expense: Expense, status: str):
        """
        Sets the final status of an expense.
        """
        expense.status = status
        expense.current_approver = None
        expense.save()
