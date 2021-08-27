from unicodedata import category
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Account, Entry, Entry_type, Entry_type_category
import datetime

class ExpenseEntryForm(forms.Form):
    """add/edit an expense entry"""
    type = forms.ModelChoiceField(queryset=Entry_type.objects.all(), label='What kind of transaction?',
        widget=forms.Select(attrs={'class' : 'browser-default'}))
    category = forms.ModelChoiceField(queryset=Entry_type_category.objects.all(), label='What category?',
        widget=forms.Select(attrs={'class' : 'browser-default'}))
    date = forms.DateField(label='When?')
    withdraw_account = forms.ModelChoiceField(queryset=Account.objects.all(), label='withdraw from..',
        widget=forms.Select(attrs={'class' : 'browser-default'}))
    save_account = forms.ModelChoiceField(queryset=Account.objects.all(), label='save to..',
        widget=forms.Select(attrs={'class' : 'browser-default'}))
    name = forms.CharField(max_length=40, label='What was it about?')
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    memo = forms.CharField(max_length=300, required=False, widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ExpenseEntryForm, self).__init__(*args, **kwargs)
        if user:
            # self.fields['user_id'].queryset = user
            self.fields['category'].queryset = Entry_type_category.objects.filter(user_id=user)
            self.fields['withdraw_account'].queryset = Account.objects.filter(user_id=user)
            self.fields['save_account'].queryset = Account.objects.filter(user_id=user)
        else:
            raise ValidationError('no user')

"""
TODO:
- validate: category, date, XXXacount really belongs to user
- validate: in account != out account
- validate: if pay, must mave an out account; if deposit, ...; if transfer, ...
- display currency (USD/TWD) depending on the selected account
"""