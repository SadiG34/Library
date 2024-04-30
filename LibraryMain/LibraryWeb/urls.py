from django.urls import path

from .views import ListAllBooksView, BookCreateView, BookUpdateView, BookDeleteView, VisitorCreateView, \
    VisitorUpdateView, ListAllVisitorsView, IssueBookView, home_view, close_card_2_view, close_card_view

urlpatterns = [
    path('', home_view, name='home'),
    path('book_list/', ListAllBooksView.as_view(), name='book_list'),
    path("add_book/", BookCreateView.as_view(), name="add_book"),
    path("<int:pk>/update_book/", BookUpdateView.as_view(), name="update_book"),
    path("<int:pk>/delete_book/", BookDeleteView.as_view(), name="delete_book"),
    path('visitor_list/', ListAllVisitorsView.as_view(), name='visitor_list'),
    path("add_visitor/", VisitorCreateView.as_view(), name="add_visitor"),
    path("<int:pk>/update_visitor/", VisitorUpdateView.as_view(), name="update_visitor"),
    path('issue_book/', IssueBookView.as_view(), name='issue_book'),
    path('return_book/<int:id>/', close_card_2_view, name='return_book'),
    path('card_list/', close_card_view, name='card_list'),
]