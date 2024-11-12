from django.shortcuts import render
from catalog.models import *

# 모델의 생성자를 사용하여 새로운 레코드 생성
record = MyModelName(my_field_name="Instance #1")

# 객체를 데이터베이스에 저장
record.save()

# Python 속성을 사용하여 모델 필드 값에 접근
print(record.id)
print(record.my_field_name)

# 필드를 수정한 후 save()를 호출하여 레코드 변경
record.my_field_name = "New Instance Name"
record.save()

# 모든 책 객체를 가져오기
all_books = Book.objects.all()

# 제목에 'wild'가 포함된 책을 필터링
wild_books = Book.objects.filter(title__contains='wild')

# 'wild'가 포함된 책의 개수
number_wild_books = wild_books.count()

# 장르에 'fiction'이 포함된 책을 필터링 (예: Fiction, Non-Fiction 등)
books_containing_genre = Book.objects.filter(genre__name__icontains='fiction')
