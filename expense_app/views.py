from django.shortcuts import render
from django.views import generic
from django.views.generic import edit
from django.db.models import F, QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
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

class ExpenseEntry:
    class ListView(generic.ListView):
        template_name = 'expense_app/entry_list.html'
        context_object_name = 'context'

        def get_queryset(self):
            return Entry.objects.filter(user_id=self.request.user).order_by('-date')

    class DetailView(generic.DetailView):
        template_name = 'expense_app/entry_detail.html'
        context_object_name = 'entry'
        model = Entry

    class UpdateEntryView(edit.UpdateView):
        template_name = 'expense_app/entry_edit.html'
        context_object_name = 'entry'
        model = Entry
        fields = [
            'type',
            'category',
            'date',
            'account',
            'name',
            'amount',
            'memo',
        ]
        def get_success_url(self) -> str:
            return reverse('expense_app:entry_list')

    class DeleteEntryView(edit.DeleteView):
        template_name = 'expense_app/entry_delete.html'
        context_object_name = 'entry'
        model = Entry
        def get_success_url(self) -> str:
            return reverse('expense_app:entry_list')

    def add(request):
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

                return HttpResponseRedirect(reverse('expense_app:entry_list'))
        else: 
            form = ExpenseEntryForm(user=request.user)
        context = {
            'form': form,
            'new_entry': new_entry,
        }
        return render(request, 'expense_app/entry_add.html', context)