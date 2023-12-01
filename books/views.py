from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import BookForm
from matplotlib import pyplot as plt
import io
import base64


@login_required
def list_books(request):
    # Search
    search = request.GET.get('search')
    if search:
       books = Book.objects.filter(Q(name__icontains=search))
    else:
       books = Book.objects.all()

    # Order
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    if sort:
        if order == 'asc':
           books = Book.objects.order_by(sort)
        else:
           books = Book.objects.order_by(sort).reverse()

    # Pagination
    paginator = Paginator(books, 5)
    page = request.GET.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request, 'books.html', {'books': books, 'page': page})

@login_required
def create_book(request):
    form = BookForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('list_books')

    return render(request, 'books-form.html', {'form': form})

@login_required
def update_book(request, id):
    book = Book.objects.get(id=id)
    form = BookForm(request.POST or None, instance=book)

    if form.is_valid():
        form.save()
        return redirect('list_books')

    return render(request, 'books-form.html', {'form': form, 'book': book})

@login_required
def delete_book(request, id):
    book = Book.objects.get(id=id)
    book.delete()

    return redirect('list_books')

def view_book(request, id):
    book = Book.objects.get(id=id)

    return render(request, 'book-detail.html', {'book': book})



def graph(request):
    books = Book.objects.all()

    names = [book.name for book in books]
    prices = [book.price for book in books]
    fig, ax = plt.subplots()


    ax.set_title('Book Prices')
    ax.set_xlabel('Names')
    ax.set_ylabel('Prices')


    # # Create the bar graph
    plt.bar(names, prices)

    # Convert the plot to a binary string and get its mime type
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode()
    mime_type = 'image/png'

    # Return the data to the HTML template
    return render(request, 'graph.html', {'data': string, 'mime_type': mime_type})