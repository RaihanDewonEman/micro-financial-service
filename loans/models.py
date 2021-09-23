from django.db import models

# Create your models here.
class Application(models.Model):
    client_name = models.CharField(max_length=30)
    client_bod = models.DateField()
    client_monthly_salary = models.DecimalField(max_digits=12, decimal_places=2)
    client_loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_by = models.CharField(max_length=30)
    is_assign_account = models.BooleanField(default=False)

    def __str__(self):
        return "%s %d %s" % self.client_name, self.client_loan_amount, self.is_assign_account

class Account(models.Model):
    loan_application = models.OneToOneField(
        Application, 
        on_delete=models.CASCADE,
        primary_key=True,
    )
    approved_loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    paid_loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField()
    created_by = models.CharField(max_length=30)

    def __str__(self):
        return "%s %d" % self.loan_application.client_name, self.approved_loan_amount


class Collection(models.Model):
    collected_amount = models.DecimalField(max_digits=15, decimal_places=2)
    collection_date = models.DateField()
    next_collection_date = models.DateField()
    collected_by = models.CharField(max_length=30)
    loan_account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return "%d" % self.loan_account.id
