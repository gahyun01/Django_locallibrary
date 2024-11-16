# HTML과 데이터를 렌더링하는 Django 뷰 함수를 작성

from django.http import HttpResponse
from catalog.models import *
from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_list_or_404
from django.urls import reverse


def index(request):
    """View function for home page of site."""

    # 대소문자 구분 없이 'fiction' 단어가 포함된 장르 찾기
    target_word = 'development'
    genres_with_target_word = Genre.objects.filter(name__icontains=target_word)

    # 특정 단어를 포함하는 장르에 해당하는 책들 찾기
    books = Book.objects.filter(genre__in=genres_with_target_word)
    instances_available = BookInstance.objects.filter(book__in=books)

    # G일부 주요 개체의 수를 생성
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # 사용 가능한 책 (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # 'all()' 은 기본적으로 암시되어 있음
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    num_visits = num_visits + 1
    request.session['num_visits'] = num_visits

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
        'books': books.count(),
        'instances_available': instances_available.count(),
    }

    # 컨텍스트 변수의 데이터로 HTML 템플릿 인덱스.html 렌더링
    return render(request, 'index.html', context=context)


# 책 목록을 표시하는 뷰
class BookListView(generic.ListView):
    """ 책 목록에 대한 일반 클래스 기반 보기 """
    model = Book
    paginate_by = 5

# class BookListView(generic.ListView):
#     model = Book
#     context_object_name = 'book_list'   # 템플릿 변수로 목록에 대한 사용자 이름
#     template_name = 'books/book_list.html'  # 템플릿 파일 지정
#     paginate_by = 5 # 한 페이지에 표시할 항목 수

#     def get_queryset(self):
#         # 'war'가 포함된 책 데이터 필터링
#         queryset = Book.objects.filter(title__icontains='war')
#         # 데이터가 없으면 모든 책 데이터 반환
#         if not queryset.exists():
#             queryset = Book.objects.all()
#         return queryset[:5]  # 최대 5개만 반환

#     def get_context_data(self, **kwargs):
#         # 기본 구현을 먼저 호출하여 컨텍스트 파악
#         context = super(BookListView, self).get_context_data(**kwargs)
#         # 추가된 약간의 데이터와 함께 컨텍스트에 추가
#         context['some_data'] = 'This is just some data'
#         return context
    
class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, primary_key):
        book = get_list_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html', context={'book', book})
    

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(generic.DetailView):
    model = Author

    def author_detail_view(request, primary_key):
        author = get_list_or_404(Author, pk=primary_key)
        return render(request, 'catalog/author_detail.html', context={'author', author})