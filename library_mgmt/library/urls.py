from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book-list'),
    path('books/', views.book_list, name='book-list'),
    path('add-book/', views.add_book, name='add-book'),
    path('members/', views.member_list, name='member-list'),
    path('add-member/', views.add_member, name='add-member'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow-book'),
    path('return/<int:loan_id>/', views.return_book, name='return-book'),
    path('loans/', views.loan_list, name='loan-list'),
    path('fines/', views.fine_list, name='fine-list'),
]
