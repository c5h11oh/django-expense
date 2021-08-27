from django.urls import path, include
from django.urls.resolvers import URLPattern
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'expense_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('moneyaccount/', login_required(views.MoneyAccountView.as_view()), name='moneyaccount'),
    path('expense/add/', login_required(views.ExpenseEntry.add), name='entry_add'),
    path('expense/list/', login_required(views.ExpenseEntry.ListView.as_view()), name='entry_list'),
    path('expense/<int:pk>/', login_required(views.ExpenseEntry.DetailView.as_view()), name='entry_detail'),
    path('expense/edit/<int:pk>/', login_required(views.ExpenseEntry.UpdateEntryView.as_view()), name='entry_edit'),
    path('expense/delete/<int:pk>/', login_required(views.ExpenseEntry.DeleteEntryView.as_view()), name='entry_delete'),
]