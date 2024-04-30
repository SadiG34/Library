from django.db import models
from django.urls import reverse
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    publisher = models.CharField(max_length=100)
    page_count = models.IntegerField()
    copies_available = models.IntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_list')

class Visitor(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

class VisitorCard(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField()
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.visitor.full_name} - {self.book.title}"