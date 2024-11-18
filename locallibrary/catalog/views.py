# HTML과 데이터를 렌더링하는 Django 뷰 함수를 작성

from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.forms import RenewBookForm
from .models import Book, Author, BookInstance, Genre, Language

import datetime


def index(request):
    """ 사이트 홈 페이지의 보기 기능 """

    # 주요 객체 중 일부의 수를 생성
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # 사용 가능한 책 (status = 'a')의 수 계산
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # 'all()' 은 기본적으로 암시되어 있음
    num_authors = Author.objects.count()

    # 이 뷰에 대한 방문 수는 세션 변수에서 계산
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    # 사용자가 사서인 경우 staff 표시
    is_librarian = None
    is_librarian = request.user.groups.filter(name='Librarians').exists()

    if is_librarian:
        # 컨텍스트 변수의 데이터로 index.html HTML 템플릿을 렌더링
        return render(
            request,
            'index.html',
            context={'num_books': num_books, 'num_instances': num_instances,
                    'num_instances_available': num_instances_available, 'num_authors': num_authors,
                    'num_visits': num_visits, 'is_librarian': is_librarian},
        )
    
    else:
        # 컨텍스트 변수의 데이터로 index.html HTML 템플릿을 렌더링
        return render(
            request,
            'index.html',
            context={'num_books': num_books, 'num_instances': num_instances,
                    'num_instances_available': num_instances_available, 'num_authors': num_authors,
                    'num_visits': num_visits},
        )

    """
    # 대소문자 구분 없이 'fiction' 단어가 포함된 장르 찾기
    target_word = 'development'
    genres_with_target_word = Genre.objects.filter(name__icontains=target_word)

    # 특정 단어를 포함하는 장르에 해당하는 책들 찾기
    books = Book.objects.filter(genre__in=genres_with_target_word)
    instances_available = BookInstance.objects.filter(book__in=books)

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
    """



# 책 목록을 위한 뷰
class BookListView(generic.ListView):
    """ 책 목록에 대한 일반 클래스 기반 뷰 """
    model = Book
    paginate_by = 5

"""
class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # 템플릿 변수로 목록에 대한 사용자 이름
    template_name = 'books/book_list.html'  # 템플릿 파일 지정
    paginate_by = 5 # 한 페이지에 표시할 항목 수

    def get_queryset(self):
        # 'war'가 포함된 책 데이터 필터링
        queryset = Book.objects.filter(title__icontains='war')
        # 데이터가 없으면 모든 책 데이터 반환
        if not queryset.exists():
            queryset = Book.objects.all()
        return queryset[:5]  # 최대 5개만 반환

    def get_context_data(self, **kwargs):
        # 기본 구현을 먼저 호출하여 컨텍스트 파악
        context = super(BookListView, self).get_context_data(**kwargs)
        # 추가된 약간의 데이터와 함께 컨텍스트에 추가
        context['some_data'] = 'This is just some data'
        return context
"""
    
class BookDetailView(generic.DetailView):
    """ 책을 위한 일반 클래스 기반 세부 정보 뷰 """
    model = Book

    # def book_detail_view(request, primary_key):
    #     book = get_list_or_404(Book, pk=primary_key)
    #     return render(request, 'catalog/book_detail.html', context={'book', book})
    


# 저자 목록을 위한 뷰
class AuthorListView(generic.ListView):
    """ 저자 목록에 대한 일반 클래스 기반 뷰 """
    model = Author
    paginate_by = 5

class AuthorDetailView(generic.DetailView):
    """ 저자에 대한 일반 클래스 기반 세부 정보 뷰 """
    model = Author

    # def author_detail_view(request, primary_key):
    #     author = get_list_or_404(Author, pk=primary_key)
    #     return render(request, 'catalog/author_detail.html', context={'author', author})



# 장르 목록을 위한 뷰
class GenreListView(generic.ListView):
    """ 장르 목록을 위한 일반 클래스 기반 목록 뷰 """
    model = Genre
    paginate_by = 10

class GenreDetailView(generic.DetailView):
    """ 장르에 대한 일반 클래스 기반 세부 정보 뷰 """
    model = Genre



# 언어 목록을 위한 뷰
class LanguageListView(generic.ListView):
    """ 언어 목록을 위한 일반 클래스 기반 목록 뷰 """
    model = Language
    paginate_by = 10

class LanguageDetailView(generic.DetailView):
    """ 언어에 대한 일반 클래스 기반 세부 정보 뷰 """
    model = Language



# 책 인스턴스 목록을 위한 뷰
class BookInstanceListView(generic.ListView):
    """ 책 목록을 위한 일반 클래스 기반 뷰 """
    model = BookInstance
    paginate_by = 10

class BookInstanceDetailView(generic.DetailView):
    """ 책을 위한 일반 클래스 기반 세부 정보 뷰 """
    model = BookInstance
    


# 로그인한 사용자가 대출한 책 목록에 대한 뷰
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """ 로그인한 사용자가 대출한 책 목록에 대한 일반 클래스 기반 뷰 """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

# 대출 중인 모든 책을 나열하는 뷰 ( 사서용 )
class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """ 대출 중인 모든 책을 나열하는 일반 클래스 기반 뷰. ( 반환 표시 권한이 있는 사용자만 볼 수 있음 ) """
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    


# 사서가 책을 갱신할 수 있도록 뷰
@login_required
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """ 도서관 사서에 의해 특정 BookInstance를 갱신하는 뷰 """
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # POST 요청인 경우 form 데이터 처리
    if request.method == 'POST':

        # form 인스턴스를 생성하고 요청에 의한 데이터로 채운다 ( binding: 바인딩 )
        book_renewal_form = RenewBookForm(request.POST)

        # form이 유효한지 확인
        if book_renewal_form.is_valid():
            # book_renewal_form.cleaned_data 데이터를 요청받은대로 처리 ( 여기서는 그냥 모델 due_back 필드에 할당 )
            book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            book_instance.save()

            # 새로운 URL로 리디렉션
            return HttpResponseRedirect(reverse('all-borrowed'))
        
    # GET 요청 ( 혹은 다른 메서드 )인 경우, 기본 폼을 생성
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': book_renewal_form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)



# 저자 생성, 업데이트 및 삭제를 위한 뷰
class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    # 권장하지 않음 ( 더 많은 필드가 추가될 경우 잠재적인 보안 문제가 발생할 수 있음 )
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )
        


# 책 생성, 업데이트 및 삭제를 위한 뷰
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.add_book'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.change_book'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("book-delete", kwargs={"pk": self.object.pk})
            )
        


# 장르 생성, 업데이트 및 삭제를 위한 뷰
class GenreCreate(PermissionRequiredMixin, CreateView):
    model = Genre
    fields = ['name', ]
    permission_required = 'catalog.add_genre'

class GenreUpdate(PermissionRequiredMixin, UpdateView):
    model = Genre
    fields = ['name', ]
    permission_required = 'catalog.change_genre'

class GenreDelete(PermissionRequiredMixin, DeleteView):
    model = Genre
    success_url = reverse_lazy('genres')
    permission_required = 'catalog.delete_genre'



# 언어 생성, 업데이트 및 삭제를 위한 뷰
class LanguageCreate(PermissionRequiredMixin, CreateView):
    model = Language
    fields = ['name', ]
    permission_required = 'catalog.add_language'

class LanguageUpdate(PermissionRequiredMixin, UpdateView):
    model = Language
    fields = ['name', ]
    permission_required = 'catalog.change_language'

class LanguageDelete(PermissionRequiredMixin, DeleteView):
    model = Language
    success_url = reverse_lazy('languages')
    permission_required = 'catalog.delete_language'



# 책 인스턴스 생성, 업데이트 및 삭제를 위한 뷰
class BookInstanceCreate(PermissionRequiredMixin, CreateView):
    model = BookInstance
    fields = ['book', 'imprint', 'due_back', 'borrower', 'status']
    permission_required = 'catalog.add_bookinstance'

class BookInstanceUpdate(PermissionRequiredMixin, UpdateView):
    model = BookInstance
    # fields = "__all__"
    fields = ['imprint', 'due_back', 'borrower', 'status']
    permission_required = 'catalog.change_bookinstance'

class BookInstanceDelete(PermissionRequiredMixin, DeleteView):
    model = BookInstance
    success_url = reverse_lazy('bookinstances')
    permission_required = 'catalog.delete_bookinstance'