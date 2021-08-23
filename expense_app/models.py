from unicodedata import category
from django.db import models
from django.contrib.auth import models as auth_models

# Create your models here.
class Account_type(models.Model):
    name = models.CharField(max_length=40)
    currency = models.CharField(max_length=3, default='USD')
    class Meta:
        verbose_name = 'Account Type'
    def __str__(self):
        return self.name

class Account(models.Model):
    user_id = models.ForeignKey(auth_models.User, on_delete=models.PROTECT)
    account_type = models.ForeignKey(Account_type, on_delete=models.PROTECT)
    name = models.CharField(max_length=40)

    def __str__(self):
        return '[' + str(self.user_id.id) + '] ' + self.name

class Entry_type(models.Model):
    name = models.CharField(max_length=40)
    must_deduct = models.BooleanField(default=False)
    must_add = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Expense entry type'
    def __str__(this):
        return this.name

class Entry_type_category(models.Model):
    user_id = models.ForeignKey(auth_models.User, on_delete=models.PROTECT)
    type = models.ForeignKey(Entry_type, on_delete=models.PROTECT)
    name = models.CharField(max_length=40)
    class Meta:
        verbose_name = 'Expense entry category'
        verbose_name_plural = 'Expense entry categories'
    def __str__(this):
        return this.name

class Entry(models.Model):
    user_id = models.ForeignKey(auth_models.User, on_delete=models.PROTECT)
    type = models.ForeignKey(Entry_type, on_delete=models.PROTECT)
    category = models.ForeignKey(Entry_type_category, on_delete=models.PROTECT)
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    name = models.CharField(max_length=40)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    memo = models.TextField(max_length=300, blank=True) # max_length does not enforce the content length but just affects Textarea widget.
    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'
    def __str__(this):
        return '[' + str(this.user_id) + ']-[' + this.date.strftime("%Y/%m/%d") + ']-' + this.name

# from django.forms import ModelForm
# TITLE_CHOICES = [
#     ('MR', 'Mr.'),
#     ('MRS', 'Mrs.'),
#     ('MS', 'Ms.'),
# ]

# class Author(models.Model):
#     name = models.CharField(max_length=100)
#     title = models.CharField(max_length=3, choices=TITLE_CHOICES)
#     birth_date = models.DateField(blank=True, null=True)

#     def __str__(self):
#         return self.name

# class Book(models.Model):
#     name = models.CharField(max_length=100)
#     authors = models.ManyToManyField(Author)

# class AuthorForm(ModelForm):
#     class Meta:
#         model = Author
#         fields = ['name', 'title', 'birth_date']

# class BookForm(ModelForm):
#     class Meta:
#         model = Book
#         fields = ['name', 'authors']