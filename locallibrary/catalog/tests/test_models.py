from django.test import TestCase
from catalog.models import Author


# Author 모델에 대한 테스트 클래스
class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """ 모든 테스트 메서드에서 사용할 초기 데이터 설정 """
        Author.objects.create(first_name='Big', last_name='Bob')

    # Author 모델의 first_name 필드 라벨을 테스트
    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    # Author 모델의 last_name 필드 라벨을 테스트
    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    # Author 모델의 date_of_birth 필드 라벨을 테스트
    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    # Author 모델의 date_of_death 필드 라벨을 테스트
    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')


    # Author 모델의 first_name 필드의 최대 길이를 테스트
    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    # Author 모델의 last_name 필드의 최대 길이를 테스트
    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)


    # Author 객체의 문자열 표현을 테스트
    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = '{0}, {1}'.format(author.last_name, author.first_name)   # 예상 문자열 표현 생성 (last_name, first_name 형식)
        self.assertEqual(str(author), expected_object_name)     # Author 객체의 문자열 표현이 예상 값과 일치하는지 확인


    # Author 모델의 get_absolute_url 메서드를 테스트
    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')    # get_absolute_url 메서드가 '/catalog/author/1'을 반환하는지 확인
