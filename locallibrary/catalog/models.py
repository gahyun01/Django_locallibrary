from django.db import models
from django.urls import reverse
import uuid
from django.db.models.constraints import UniqueConstraint
from django.db.models.functions import Lower

class MyModelName(models.Model):
    """모델 클래스를 정의하는 일반적인 클래스, Model 클래스로부터 파생됨."""
    
    # 필드
    my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')

    # 메타데이터
    class Meta:
        ordering = ['-my_field_name']  # 필드를 오름차순으로 정렬합니다.

    # 메서드
    def get_absolute_url(self):
        """MyModelName의 특정 인스턴스로 접근하는 URL을 반환합니다."""
        return reverse('model-detail-view', args=[str(self.id)])
    
    def __str__(self):
        """MyModelName 객체를 문자열로 나타냅니다 (관리자 사이트 등에서)."""
        return self.my_field_name

# 장르 모델 추가
class Genre(models.Model):
    """책 장르를 나타내는 모델."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction, French Poetry etc.)')

    def __str__(self):
        """모델 객체를 문자열로 나타냅니다."""
        return self.name
    
# 언어 모델 추가
class Language(models.Model):
    """언어를 나타내는 모델 (예: 영어, 프랑스어, 일본어 등)"""
    name = models.CharField(max_length=200, unique=True, help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def get_absolute_url(self):
        """특정 언어 인스턴스에 접근할 수 있는 URL 반환"""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        """모델 객체를 나타내는 문자열 (Admin 사이트 등에서 사용)"""
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ]

# 책 모델 추가
class Book(models.Model):
    """책을 나타내는 모델 (특정 책 복사본이 아님)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    # ForeignKey를 사용한 이유: 책은 한 명의 저자만 가질 수 있지만, 저자는 여러 권의 책을 가질 수 있습니다.
    # 'Author'를 문자열로 사용한 이유: 파일 내에서 아직 선언되지 않았기 때문입니다.
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13자리 <a href="https://www.isbn-international.org/content/what-isbn">ISBN 번호</a>')

    # ManyToManyField를 사용한 이유: 하나의 장르에 여러 권의 책이 포함될 수 있고, 책은 여러 장르를 다룰 수 있습니다.
    # Genre 클래스는 이미 정의되었으므로 위의 객체를 지정할 수 있습니다.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """모델 객체를 문자열로 나타냅니다."""
        return self.title
    
    def get_absolute_url(self):
        """이 책의 상세 정보에 접근할 URL을 반환합니다."""
        return reverse('book-detail', args=[str(self.id)])

# 복사본 모델 추가
class BookInstance(models.Model):
    """특정 책의 복사본을 나타내는 모델."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """모델 객체를 문자열로 나타냅니다."""
        return f'{self.id} ({self.book.title})'

# 저자 모델 추가
class Author(models.Model):
    """저자를 나타내는 모델"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """이 저자의 상세 정보에 접근할 URL을 반환합니다."""
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """모델 객체를 문자열로 나타냅니다."""
        return f'{self.last_name}, {self.first_name}'