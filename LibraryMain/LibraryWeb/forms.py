from django import forms
from django.forms import DateTimeInput
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Book, Visitor, VisitorCard
class IssueBookForm(forms.ModelForm):
    borrowed_date = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = VisitorCard
        fields = ['visitor', 'book', 'borrowed_date']

    def __init__(self, *args, **kwargs):
        super(IssueBookForm, self).__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(copies_available__gt=0)

