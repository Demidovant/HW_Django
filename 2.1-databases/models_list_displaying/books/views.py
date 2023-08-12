from django.shortcuts import render, redirect
from books.models import Book

def index(request):
    return redirect('books')

def books_view(request):
    template = 'books/books_list.html'
    context = {"books": Book.objects.all()}
    return render(request, template, context)

def date_book_view(request, pub_date):
    books_objects = Book.objects.filter(pub_date=pub_date)
    books_next = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date').first()
    books_previous = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date').first()
    context = {
        'books': books_objects,
        'next_book': books_next,
        'previous_book': books_previous,
    }
    template = 'books/book.html'
    return render(request, template, context)
