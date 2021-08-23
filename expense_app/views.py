from django.shortcuts import render
from django.views import generic
from django.db.models import F, QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Account as acc, Account_type as acc_typ, Entry
from .forms import ExpenseEntryForm

# Create your views here.
def index(request):
    context = {
        'name': __name__
    }
    return render(request, 'expense_app/index.html', context)

class MoneyAccountView(generic.ListView):
    template_name = 'expense_app/money_account.html'
    context_object_name = 'money_accounts'

    def get_queryset(self) -> QuerySet:
        """
        return the money account owned by the login user.
        """
        return acc.objects.filter(user_id=self.request.user).order_by('account_type', 'name')
        # return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

@login_required
def add_entry(request):
    new_entry = Entry()
    if request.method == 'POST':
        form = ExpenseEntryForm(request.POST, user=request.user)
        if form.is_valid():
            new_entry.user_id = request.user
            new_entry.type    = form.cleaned_data['type']
            new_entry.category= form.cleaned_data['category']
            new_entry.date    = form.cleaned_data['date']
            new_entry.account = form.cleaned_data['withdraw_account']
            new_entry.name = form.cleaned_data['name']
            new_entry.amount = form.cleaned_data['amount']
            new_entry.memo = form.cleaned_data['memo']
            new_entry.save()

            return HttpResponseRedirect(reverse('expense_app:index'))
    else: 
        form = ExpenseEntryForm(user=request.user)
    context = {
        'form': form,
        'new_entry': new_entry,
    }

    return render(request, 'expense_app/add_entry.html', context)