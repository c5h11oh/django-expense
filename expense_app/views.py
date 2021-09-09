from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import render
from django.views import View, generic
from django.views.generic import edit
from django.db.models import F, QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Account as acc, Entry, Entry_type_category as Category
from .forms import ExpenseEntryForm, ExpenseEditForm, MoneyAccountForm

# test
# def user

# Create your views here.
def index(request):
    context = {
        'name': __name__
    }
    return render(request, 'expense_app/index.html', context)

class MoneyAccount: 
    class MoneyAccountView(generic.ListView):
        template_name = 'expense_app/money_account.html'
        context_object_name = 'money_accounts'

        def get_queryset(self) -> QuerySet:
            """
            return the money account owned by the login user.
            """
            return acc.objects.filter(user_id=self.request.user).order_by('account_type', 'name')
            # return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

    class MoneyAccountAddView(View):
        template_name = 'expense_app/money_account_add.html'
        form_class = MoneyAccountForm
        def get(self, request, *args, **kwargs):
            form = self.form_class()
            return render(request, self.template_name, { 'form':form })
        def post(self, request, *args, **kwargs):
            form = self.form_class(request.POST)
            if form.is_valid():
                new_account = acc()
                new_account.user_id = request.user
                new_account.account_type = form.cleaned_data['account_type']
                new_account.name = form.cleaned_data['name']
                new_account.save()
                return HttpResponseRedirect(reverse('expense_app:moneyaccount')) 
            else:
                return render(request, self.template_name, { 'form':form })
    
    class MoneyAccountUpdateView(UserPassesTestMixin, edit.UpdateView):
        model = acc
        template_name = 'expense_app/money_account_edit.html'
        fields = ['account_type', 'name']
        def get_success_url(self) -> str:
            return reverse('expense_app:moneyaccount')
        def test_func(self):
            return acc.objects.get(pk=self.kwargs['pk']).user_id == self.request.user
    
    class MoneyAccountDeleteView(UserPassesTestMixin, edit.DeleteView):
        template_name = 'expense_app/money_account_delete.html'
        context_object_name = 'account'
        model = acc
        success_url = reverse_lazy('expense_app:moneyaccount')
        
        def test_func(self):
            return acc.objects.get(pk=self.kwargs['pk']).user_id == self.request.user
        def delete(self, request, *args, **kwargs):
            try:
                return super().delete(request, *args, **kwargs)
            except ProtectedError as err:
                context = self.get_context_data()
                context['err_msg'] = 'The account cannot be deleted. There is at least one expense entry belongs to this account.'
                return self.render_to_response(context)
                
class Category:
    class Add(generic.CreateView):
        model = Category
        template_name = 'expense_app/category_add.html' # default is app_name/(Model-name)_form.html -> expense_app/entry_type_category_form.html
        fields = ['type', 'name']
        success_url = reverse_lazy('expense_app:entry_add')
        def form_valid(self, form):
            form.instance.user_id = self.request.user
            return super().form_valid(form)

class ExpenseEntry:
    class ListView(generic.ListView):
        template_name = 'expense_app/entry.html'
        context_object_name = 'context'

        def get_queryset(self):
            return Entry.objects.filter(user_id=self.request.user).order_by('-date')

    class DetailView(UserPassesTestMixin, generic.DetailView):
        template_name = 'expense_app/entry_detail.html'
        context_object_name = 'entry'
        model = Entry
        def test_func(self):
            return Entry.objects.get(pk=self.kwargs['pk']).user_id == self.request.user

    class UpdateEntryView(UserPassesTestMixin, edit.UpdateView):
        model = Entry
        def test_func(self):
            return Entry.objects.get(pk=self.kwargs['pk']).user_id == self.request.user
        def get_form(self, form_class=ExpenseEditForm):
            item = Entry.objects.get(id=self.kwargs['pk'])
            form = form_class(user=self.request.user, initial={
                'type' : item.type,
                'category' : item.category,
                'date' : item.date,
                'account' : item.account,
                'name' : item.name,
                'amount' : item.amount,
                'memo' : item.memo,

            })
            return form
        template_name = 'expense_app/entry_edit.html'
        def get_initial(self):
            the_initial = super().get_initial()
            # the_initial['category'] = Entry_ty
            return the_initial
        def get_success_url(self) -> str:
            return reverse('expense_app:entry')
        # context_object_name = 'entry'

    class DeleteEntryView(UserPassesTestMixin, edit.DeleteView):
        template_name = 'expense_app/entry_delete.html'
        context_object_name = 'entry'
        model = Entry
        def test_func(self):
            return Entry.objects.get(pk=self.kwargs['pk']).user_id == self.request.user
        def get_success_url(self) -> str:
            return reverse('expense_app:entry')

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

                return HttpResponseRedirect(reverse('expense_app:entry'))
        else: 
            form = ExpenseEntryForm(user=request.user)
        context = {
            'form': form,
            'new_entry': new_entry,
        }
        return render(request, 'expense_app/entry_add.html', context)
