from datetime import date

from bootstrap_navbar.navbars.mixins import BootstrapNavBarViewMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.list import ListView

from .forms import  IssueBookForm
from .models import Book, Visitor, VisitorCard


class ListAllBooksView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
    paginate_by = 100

    def get_queryset(self):
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort')

        object_list = Book.objects.all()

        if query:
            object_list = Book.objects.filter(
                Q(title__icontains=query) | Q(author__icontains=query) | Q(publisher__icontains=query)
            )

        if sort_by == 'title':
            object_list = object_list.order_by('title')
        elif sort_by == 'author':
            object_list = object_list.order_by('author')
        elif sort_by == 'copies':
            object_list = object_list.order_by('copies_available')

        return object_list


class ListAllVisitorsView(ListView):
    model = Visitor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class BookCreateView(CreateView):
    model = Book
    template_name = 'LibraryWeb/add_book.html'
    fields = ["title", 'author', 'publication_year', 'publisher', 'page_count', 'copies_available']
    success_url = reverse_lazy('LibraryWeb/home.html')


class VisitorCreateView(CreateView):
    model = Visitor
    template_name = 'LibraryWeb/add_visitor.html'
    fields = ["full_name", 'phone']
    success_url = reverse_lazy('visitor_list')


class BookUpdateView(UpdateView):
    model = Book
    fields = ["title", 'author', 'publication_year', 'publisher', 'page_count', 'copies_available']
    template_name_suffix = "_update_form"


class VisitorUpdateView(UpdateView):
    model = Visitor
    fields = ["full_name", 'phone']
    template_name = "LibraryWeb/update_visitor.html"
    success_url = reverse_lazy("visitor_list")

class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy("book_list")


class IssueBookView(View):
    def get(self, request):
        form = IssueBookForm()
        return render(request, 'LibraryWeb/issue_book.html', {'form': form})

    def post(self, request):
        form = IssueBookForm(request.POST)
        if form.is_valid():
            visitor_card = form.save(commit=False)
            book = form.cleaned_data['book']
            book.copies_available -= 1
            book.save()
            visitor_card.save()
            return redirect('home')
        return render(request, 'LibraryWeb/issue_book.html', {'form': form})

def close_card_2_view(request, id):
    card = get_object_or_404(VisitorCard, id=id)
    card.returned_date = date.today()
    card.save()
    book = card.book
    book.copies_available += 1
    book.save()
    return redirect('home')


def close_card_view(request):
    open_cards = VisitorCard.objects.filter(returned_date=None)
    close_cards = VisitorCard.objects.filter(returned_date__isnull=False)
    return render(request, 'LibraryWeb/card_list.html', {'open_cards': open_cards, 'close_cards': close_cards})

def home_view(request):
    return render(request,'LibraryWeb/home.html')

