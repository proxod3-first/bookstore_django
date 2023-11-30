from django.urls import path
from .views import list_books, create_book, update_book, delete_book, view_book

urlpatterns = [
    path('', list_books, name='list_books'),
    path('new', create_book, name='create_books'),
    path('update/<int:id>/', update_book, name='update_book'),
    path('delete/<int:id>/', delete_book, name='delete_book'),
	path('view/<int:id>', view_book, name='view_book'),
]
