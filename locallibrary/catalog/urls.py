from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]


urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),
]


# 사서가 책을 갱신할 수 있도록 URLConf를 추가
urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]


# 저자 생성, 업데이트 및 삭제를 위한 URLConf 추가
urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]


# 책 생성, 업데이트 및 삭제를 위한 URLConf 추가
urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]


# 장르를 나열하고, 보기, 생성하고, 업데이트하고, 삭제하기 위한 URLConf 추가
urlpatterns += [
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('genre/<int:pk>', views.GenreDetailView.as_view(), name='genre-detail'),
]


# 언어를 나열하고, 보기, 생성하고, 업데이트하고, 삭제하기 위한 URLConf 추가
urlpatterns += [
    path('languages/', views.LanguageListView.as_view(), name='languages'),
    path('language/<int:pk>', views.LanguageDetailView.as_view(), name='language-detail'),
]


# 책 인스턴스를 나열하고, 보기, 생성하고, 업데이트하고, 삭제하기 위한 URLConf 추가
urlpatterns += [
    path('bookinstances/', views.BookInstanceListView.as_view(), name='bookinstances'),
]