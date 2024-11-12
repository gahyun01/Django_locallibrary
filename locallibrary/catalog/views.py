# HTML과 데이터를 렌더링하는 Django 뷰 함수를 작성

from django.http import HttpResponse
from catalog.models import Book, Author, BookInstance, Genre
from django.shortcuts import render

def index(request):
    """View function for home page of site."""

    # 대소문자 구분 없이 'fiction' 단어가 포함된 장르 찾기
    target_word = 'development'
    genres_with_target_word = Genre.objects.filter(name__icontains=target_word)

    # 특정 단어를 포함하는 장르에 해당하는 책들 찾기
    books = Book.objects.filter(genre__in=genres_with_target_word)
    instances_available = BookInstance.objects.filter(book__in=books)

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'books': books.count(),
        'instances_available': instances_available.count(),
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)