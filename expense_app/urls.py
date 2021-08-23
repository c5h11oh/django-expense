from django.urls import path, include
from django.urls.resolvers import URLPattern
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'expense_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('moneyaccount/', login_required(views.MoneyAccountView.as_view()), name='moneyaccount'),
    path('expense/add/', views.add_entry, name='add_entry'),
]