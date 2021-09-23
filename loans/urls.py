from django.urls import path
from . import views

urlpatterns =[
    path('application/', views.loan_application_view, name='loanapplication'),
    path('application/list/', views.loan_application_list_view, name='applicationlist'),
    path('loanaccount/', views.loan_account_view, name='loanaccount'),
    path('loanaccount/list/', views.loan_account_list_view, name='accountlist'),
    path('loancollection/', views.loan_collection_view, name='loancollection'),
    path('loancollection/list/', views.loan_collection_list_view, name='collectionlist'),
    path('employeePerformance/', views.performance_view, name='performance')

]