from django.shortcuts import render, redirect
from .models import Application, Account, Collection
from django.contrib.auth.models import User
import time
from datetime import datetime, date, timedelta

# Create your views here.

def loan_application_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            user_name = user.username
            application_data = Application(client_name=request.POST['client_name'], client_bod=request.POST['dob'], client_monthly_salary=request.POST['income'], client_loan_amount=request.POST['expectedloan'], created_by=user_name)
            application_data.save()
            time.sleep(1)
            return redirect('home')
        else:
            return render(request, 'loans/loan_application.html', {'title': 'Application Form'})
    else:
        return render(request, 'employee/loginpage.html', {'title' : 'Login Page'})


def loan_account_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            app_id = request.POST['application_id']
            app_id = str(app_id)
            client_app = Application.objects.filter(id=app_id)
            approved_loan = round(float(client_app[0].client_loan_amount)*.8, 2)
            Application.objects.filter(id=app_id).update(is_assign_account=True)
            acc = Account(loan_application=client_app[0], approved_loan_amount=approved_loan, paid_loan_amount =0, created_at = datetime.now(), created_by=request.user.username)
            acc.save()
            return redirect('loanaccount')
        else:
            app_list = Application.objects.filter(is_assign_account=False)
            return render(request, 'loans/loan_account.html', {'title': 'Loan Account', 'appList': app_list})
    else:
        return render(request, 'employee/loginpage.html', {'title' : 'Login Page'})

def loan_application_list_view(request):
    if request.user.is_authenticated:
        app_list = Application.objects.all()
        return render(request, 'loans/application_list.html', {'title':'Application List', 'list': app_list})
    else:
        return render(request, 'employee/loginpage.html', {'title' : 'Login Page'})

def loan_account_list_view(request):
    if request.user.is_authenticated:
        acc_list = Account.objects.all()
        return render(request, 'loans/account_list.html', {'title': 'Account List', 'accList': acc_list})
    else:
        return render(request, 'employee/loginpage.html', {'title' : 'Login Page'})

def loan_collection_view(request):
    if request.user.is_authenticated:
        next_installment = date.today()+ timedelta(days=7)
        if request.method == 'POST':
            acc_id = request.POST['account_id']
            acc_id = str(acc_id)
            client_acc = Account.objects.filter(loan_application_id=acc_id)
            paid_loan = client_acc[0].paid_loan_amount
            paid_loan += int(request.POST['loan_pay'])
            Account.objects.filter(loan_application_id=acc_id).update(paid_loan_amount=paid_loan)
            collection = Collection(loan_account =client_acc[0], collected_amount= request.POST['loan_pay'], collection_date= date.today(), next_collection_date=next_installment, collected_by= request.user.username )
            collection.save()
            return redirect('loancollection')
        else:
            acc_list = Account.objects.all() 
            return render(request, 'loans/loan_collection.html', {'title': 'Loan Collection', 'accList': acc_list, 'nextInstallment': next_installment})
    else:
        return render(request, 'employee/loginpage.html', {'title' : 'Login Page'})

def loan_collection_list_view(request):
    if request.user.is_authenticated:
        collection_list = Collection.objects.all()
        return render(request, 'loans/collection_list.html', {'title': 'Collection List', 'collectionList': collection_list})
    else:
        return render(request, 'employee/loginpage.html', {'title' : 'Login Page'})

def performance_view(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        dic =[]
        for user in users:
            employee_per = {}
            num_of_app = Application.objects.filter(created_by=user.username).count()
            num_of_acc = Account.objects.filter(created_by=user.username).count()
            ### Make dictionary value into a list
            employee_per['name'] = user.username
            employee_per['app'] = num_of_app
            employee_per['acc'] = num_of_acc
            dic.append( employee_per)
        print(dic)
        return render(request, 'loans/performance_list.html', {'title': 'Employee Performance', 'dic': dic })
    else:
        render(request, 'employee/loginpage.html', {'title' : 'Login Page'})