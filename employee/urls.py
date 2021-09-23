from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('home/', views.home_page, name='home'),
    path('home/employeelist/', views.employee_list_view, name='employeeList'),
    path('registration/', views.registration_page, name='regpage'),
    path('home/loan/', include('loans.urls')),

]