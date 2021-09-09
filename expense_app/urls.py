from django.urls import path, include
from django.urls.resolvers import URLPattern
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'expense_app'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('moneyaccount/', login_required(views.MoneyAccount.MoneyAccountView.as_view()), name='moneyaccount'),
    path('moneyaccount/add/', login_required(views.MoneyAccount.MoneyAccountAddView.as_view()), name='moneyaccount_add'),
    path('moneyaccount/edit/<int:pk>', login_required(views.MoneyAccount.MoneyAccountUpdateView.as_view()), name='moneyaccount_edit'),
    path('moneyaccount/delete/<int:pk>', login_required(views.MoneyAccount.MoneyAccountDeleteView.as_view()), name='moneyaccount_delete'),

    path('category/add/', login_required(views.Category.Add.as_view()), name='category_add'),

    path('expense/', login_required(views.ExpenseEntry.ListView.as_view()), name='entry'),
    path('expense/add/', login_required(views.ExpenseEntry.add), name='entry_add'),
    path('expense/<int:pk>/', login_required(views.ExpenseEntry.DetailView.as_view()), name='entry_detail'),
    path('expense/edit/<int:pk>/', login_required(views.ExpenseEntry.UpdateEntryView.as_view()), name='entry_edit'),
    path('expense/delete/<int:pk>/', login_required(views.ExpenseEntry.DeleteEntryView.as_view()), name='entry_delete'),
]