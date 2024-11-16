# 모델은 데이터베이스의 구조를 정의 ( 데이터베이스의 각 테이블은 모델 클래스로 표현 )

from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
import uuid  # 고유한 북 인스턴스에 필요
from datetime import date
from django.conf import settings  # 사용자를 차용인으로 지정

class MyModelName(models.Model):
    """ 모델 클래스에서 파생된 모델을 정의하는 일반적인 클래스임 """

    # Fields
    my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
    ...

    # Metadata
    class Meta:
        ordering = ['-my_field_name']

    # Methods
    def get_absolute_url(self):
        """ MyModelName의 특정 인스턴스에 액세스하기 위해 URL을 반환 """
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """ 관리 사이트 등에서 MyModelName 개체를 나타내는 문자열 """
        return self.field_name


class Genre(models.Model):
    """ 책 장르(예: 공상과학, 논픽션)를 대표하는 모델 """
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
    )

    def __str__(self):
        """ 모델 개체를 표현하기 위한 문자열 (in Admin site etc.)"""
        return self.name

    def get_absolute_url(self):
        """ 특정 장르 인스턴스에 액세스하기 위해 URL을 반환 """
        return reverse('genre-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)"
            ),
        ]

class Language(models.Model):
    """ 언어를 나타내는 모델(예: 영어, 프랑스어, 일본어 등) """
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        """ 모델 개체를 표현하기 위한 문자열 (in Admin site etc.)"""
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ]

class Book(models.Model):
    """ 책을 나타내는 모델(특정 책 사본은 아님) """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    # 외국어 키는 책에 저자가 한 명만 있을 수 있지만 저자는 여러 권의 책을 가질 수 있기 때문에 사용
    # 아직 파일로 선언되지 않았기 때문에 개체가 아닌 문자열로 작성됨
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book")
    # 장르에 많은 책이 포함될 수 있고 책이 여러 장르를 다룰 수 있기 때문에 ManyToManyField가 사용함
    # 장르 클래스가 이미 정의되었으므로 위의 개체를 지정할 수 있음
    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

    def display_genre(self):
        """ 장르의 문자열을 만듬. 관리에서 장르를 표시하려면 이 작업이 필요함"""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """ 특정 도서 기록에 액세스하기 위해 URL을 반환 """
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """ 모델 개체를 표현하기 위한 문자열 """
        return self.title

class BookInstance(models.Model):
    """ 책의 특정 사본을 나타내는 모델(즉, 라이브러리에서 빌릴 수 있음) """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        """ 납기 및 현재 날짜를 기준으로 책이 연체되었는지 여부를 결정 """
        return bool(self.due_back and date.today() > self.due_back)

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Book availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def get_absolute_url(self):
        """ 특정 도서 인스턴스에 액세스하기 위해 URL을 반환 """
        return reverse('bookinstance-detail', args=[str(self.id)])

    def __str__(self):
        """ 모델 개체를 표현하기 위한 문자열 """
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """ 저자를 나타내는 모델 """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """ 특정 작성자 인스턴스에 액세스하기 위해 URL을 반환 """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """ 모델 개체를 표현하기 위한 문자열 """
        return f'{self.last_name}, {self.first_name}'