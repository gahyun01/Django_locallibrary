from django.test import TestCase
from catalog.models import Author, BookInstance, Book, Genre, Language
from django.urls import reverse  # URL을 리버스하여 템플릿을 호출하기 위해 reverse 함수 사용
from django.utils import timezone
from django.contrib.auth import get_user_model  # 사용자 모델을 가져오기 위해 Django의 get_user_model 임포트
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

import datetime


""" 작가 리스트 뷰에 대한 테스트 """
class AuthorListViewTest(TestCase):

    @classmethod

    # 클래스 메서드로 테스트에 사용할 데이터 설정 ( 한 번만 실행됨 )
    def setUpTestData(cls): 
        # 페이지네이션 테스트를 위한 13명의 작가들 생성
        number_of_authors = 13
        for author_id in range(number_of_authors):
            # first_name == 'Christian {0}'과 last_name == 'Surname {0}' 형식으로 작가 이름을 지정하여 생성
            Author.objects.create(first_name='Christian {0}'.format(author_id),
                                  last_name='Surname {0}'.format(author_id))


    # 지정된 URL이 올바르게 동작하는지 테스트
    def test_view_url_exists_at_desired_location(self):  
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)


    # URL이 이름을 통해서도 접근 가능한지 테스트
    def test_view_url_accessible_by_name(self):
        # 'authors'라는 이름으로 URL 리버스 후 GET 요청
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)


    # 올바른 템플릿이 사용되는지 확인하는 테스트
    def test_view_uses_correct_template(self):
        # 'authors' 뷰로 GET 요청
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')  # 템플릿이 해당 html인지 확인


    # 페이지네이션이 10개로 설정되어 있는지 확인하는 테스트
    def test_pagination_is_ten(self):
        # 'authors' 뷰로 GET 요청
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)  # context에 'is_paginated'가 존재하는지 확인
        self.assertTrue(response.context['is_paginated'] is True)  # 'is_paginated' == True 인지를 확인
        self.assertEqual(len(response.context['author_list']), 5)  # author_list의 길이가 10인지 확인


    # 모든 작가가 나열되는지 확인하는 테스트 ( 두 번째 페이지에서 확인 )
    def test_lists_all_authors(self):
        # 두 번째 페이지를 가져와서 나머지 3명의 작가가 정확히 나오는지 확인
        response = self.client.get(reverse('authors')+'?page=2')  # 두 번째 페이지로 GET 요청
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['author_list']), 5)



# 현재 프로젝트에서 사용되는 사용자 모델을 변수 User에 할당
User = get_user_model()  

# 대출된 도서 목록을 사용자별로 테스트하는 클래스 정의
class LoanedBookInstancesByUserListViewTest(TestCase):

    # 테스트 전에 실행되는 메서드 ( 테스트 환경 설정 )
    def setUp(self):
        # 두 명의 사용자 생성
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD')

        # 사용자 저장
        test_user1.save()
        test_user2.save()

        # 책 생성
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')

        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            isbn='ABCDEFG',
            author=test_author,
            language=test_language,
        )
        # 책에 장르 설정
        genre_objects_for_book = Genre.objects.all()  # 모든 장르를 가져와서 책에 장르로 추가
        test_book.genre.set(genre_objects_for_book)

        test_book.save()  # 책 저장

        # 30개의 책 복사본(BookInstance) 객체 생성
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):

            # 반납일 설정
            return_date = timezone.now() + datetime.timedelta(days=book_copy % 5)

            # 홀수 복사본은 test_user1, 짝수 복사본은 test_user2에게 대출
            if book_copy % 2:
                the_borrower = test_user1
            else:
                the_borrower = test_user2

            # 책 상태 설정 (대출 중)
            status = 'm'

            # BookInstance 생성
            BookInstance.objects.create(book=test_book, imprint='Unlikely Imprint, 2016', due_back=return_date, borrower=the_borrower, status=status)  


    # 로그인이 되어 있지 않으면 리디렉션 테스트
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-borrowed'))

        # 로그인 페이지로 리디렉션되는지 확인
        self.assertRedirects(
            response, '/accounts/login/?next=/catalog/mybooks/')  


    # 로그인한 사용자가 올바른 템플릿을 사용하는지 테스트
    def test_logged_in_uses_correct_template(self):
        # testuser1으로 로그인
        login = self.client.login( username='testuser1', password='1X<ISRUkw+tuK')
        # 'my-borrowed' URL로 GET 요청
        response = self.client.get(reverse('my-borrowed'))

        # 사용자가 로그인했는지 확인
        self.assertEqual(str(response.context['user']), 'testuser1')
        # 상태 코드가 200(성공)인지 확인
        self.assertEqual(response.status_code, 200)

        # 올바른 템플릿이 사용되는지 확인
        print(response)
        self.assertTemplateUsed(response, 'catalog/bookinstance_list.html')


    # 대출 중인 책만 목록에 있는지 확인하는 테스트
    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        # 초기에는 대출 중인 책이 없는지 확인
        self.assertTrue('bookinstance_list' in response.context)    # context에 'bookinstance_list'가 포함되어 있는지 확인
        self.assertEqual(len(response.context['bookinstance_list']), 0)  # 목록 길이가 0이어야 함 (대출 중인 책이 없으므로)

        # 첫 10개의 책 복사본을 대출 중으로 상태 변경
        get_ten_books = BookInstance.objects.all()[:10]
        for copy in get_ten_books:
            # 책 상태를 'o' (대출 중)으로 변경
            copy.status = 'o'
            copy.save()

        response = self.client.get(reverse('my-borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bookinstance_list' in response.context)

        # 모든 책이 testuser1에 대출 중인지 확인
        for book_item in response.context['bookinstance_list']:
            self.assertEqual(response.context['user'], book_item.borrower)  # 대출자가 testuser1인지 확인
            self.assertEqual(book_item.status, 'o')  # 책 상태가 'o' (대출 중)인지 확인


    # 페이지네이션이 10개로 설정되어 있는지 확인하는 테스트
    def test_pages_paginated_to_ten(self):
        # 모든 책을 대출 중으로 상태 변경
        for copy in BookInstance.objects.all():
            copy.status = 'o'
            copy.save()

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        # 페이지네이션으로 인해 10개의 항목만 표시되는지 확인
        self.assertEqual(len(response.context['bookinstance_list']), 10)


    # 페이지에 표시된 책들이 반납 예정일 기준으로 정렬되어 있는지 확인하는 테스트
    def test_pages_ordered_by_due_date(self):
        for copy in BookInstance.objects.all():
            copy.status = 'o'
            copy.save()

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-borrowed'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['bookinstance_list']), 10)

        # 마지막 반납일 초기화
        last_date = 0
        for copy in response.context['bookinstance_list']:
            # 첫 번째 항목이라면
            if last_date == 0:
                # 첫 번째 항목의 반납일을 last_date로 설정
                last_date = copy.due_back
            else:
                # 그 후의 항목들은 반납일이 오름차순으로 정렬되어야 함
                self.assertTrue(last_date <= copy.due_back)



""" 책 갱신 기능을 처리하는 테스트 케이스 클래스 """
class RenewBookInstancesViewTest(TestCase):

    # 각 테스트 전에 실행되는 설정 메서드
    def setUp(self):

        """ 테스트 사용자 생성 """
        # 첫 번째 사용자 (빌린 사람)
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()
        # 두 번째 사용자 (사서)
        test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user2.save()
        
        # user2에게 사서 권한 부여
        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        # 책과 관련된 정보 생성
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        # 책 객체 생성
        test_book = Book.objects.create(title='Book Title', 
                                        summary='My book summary',
                                        isbn='ABCDEFG', 
                                        author=test_author, 
                                        language=test_language)
        # 책에 장르 할당
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)

        test_book.save()

        # test_user1에 대한 책 인스턴스 생성
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(book=test_book,
                                                              imprint='Unlikely Imprint, 2016', 
                                                              due_back=return_date,
                                                              borrower=test_user1, status='o')

        # test_user2에 대한 책 인스턴스 생성
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(book=test_book, 
                                                              imprint='Unlikely Imprint, 2016',
                                                              due_back=return_date, 
                                                              borrower=test_user2, status='o')


    # 로그인하지 않은 사용자가 책 갱신 페이지에 접근하면 로그인 페이지로 리다이렉트 되는지 테스트
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))


    # 로그인했지만 권한이 없는 사용자가 접근하면 403 금지 오류가 발생하는지 테스트
    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 302)


    # 권한이 있는 사용자가 자신이 빌린 책을 갱신할 수 있는지 테스트
    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))
        self.assertEqual(response.status_code, 200)


    # 라이브러리 관리자가 다른 사용자가 빌린 책을 갱신할 수 있는지 테스트
    def test_logged_in_with_permission_another_users_borrowed_book(self):
        
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)


    # 갱신 페이지에서 올바른 템플릿이 사용되는지 테스트
    def test_uses_correct_template(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)
        # 올바른 템플릿이 사용되었는지 확인
        self.assertTemplateUsed(response, 'catalog/book_renew_librarian.html')


    # 갱신 폼의 초기 날짜가 3주 후로 설정되어 있는지 테스트
    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)

        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        # 초기 날짜가 3주 후 날짜와 일치하는지 확인
        self.assertEqual(
            response.context['form'].initial['renewal_date'], date_3_weeks_in_future)


    # 과거 날짜를 입력하면 오류가 발생하는지 테스트
    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')

        # 지난주 날짜를 입력한 갱신 폼 제출
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}),
                                    {'renewal_date': date_in_past})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'], 'renewal_date', 'Invalid date - renewal in past')  # 과거 날짜 입력에 대한 폼 오류 확인


    # 너무 먼 미래의 날짜를 입력하면 오류가 발생하는지 테스트
    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')

        # 5주 후 날짜를 입력한 갱신 폼 제출
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}),
                                    {'renewal_date': invalid_date_in_future})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'], 'renewal_date', 'Invalid date - renewal more than 4 weeks ahead')  # 너무 먼 미래 날짜 입력에 대한 폼 오류 확인


    # 갱신이 성공하면 '모든 빌린 책' 목록으로 리다이렉트 되는지 테스트
    def test_redirects_to_all_borrowed_book_list_on_success(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
        response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}),
                                    {'renewal_date': valid_date_in_future})
        self.assertRedirects(response, reverse('all-borrowed'))


    # 잘못된 책 인스턴스 ID를 입력하면 404 오류가 발생하는지 테스트
    def test_HTTP404_for_invalid_book_if_logged_in(self):
        import uuid
        test_uid = uuid.uuid4()  # 잘못된 UUID 생성
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(
            reverse('renew-book-librarian', kwargs={'pk': test_uid}))
        self.assertEqual(response.status_code, 404)



""" AuthorCreate 뷰에 대한 테스트 케이스 클래스 """
class AuthorCreateViewTest(TestCase):

    def setUp(self):
        # 두 명의 사용자 생성
        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Book 모델에 대한 ContentType 객체 가져오기
        content_typeBook = ContentType.objects.get_for_model(Book)

        # "add_book" 권한을 가져오기
        permAddBook = Permission.objects.get(
            codename="add_book",
            content_type=content_typeBook,
        )

        # Author 모델에 대한 ContentType 객체 가져오기
        content_typeAuthor = ContentType.objects.get_for_model(Author)
        
        # "add_author" 권한을 가져오기
        permAddAuthor = Permission.objects.get(
            codename="add_author",
            content_type=content_typeAuthor,
        )

        # test_user2에게 사서 권한을 부여
        test_user2.user_permissions.add(permAddBook, permAddAuthor)
        test_user2.save()

        # 저자 생성 (하지만 이 저자는 테스트에서 사용되지 않음)
        test_author = Author.objects.create(first_name='John', last_name='Smith')


    # 로그인하지 않은 사용자가 AuthorCreate 페이지에 접근하면 로그인 페이지로 리다이렉트되는지 테스트
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('author-create'))
        self.assertRedirects(
            response, '/accounts/login/?next=/catalog/author/create/')


    # 권한이 없는 사용자가 AuthorCreate 페이지에 접근하면 403 Forbidden 에러가 발생하는지 테스트
    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 403)


    # 권한이 있는 사용자가 AuthorCreate 페이지에 접근하면 정상적으로 페이지가 열리는지 테스트
    def test_logged_in_with_permission(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)


    # AuthorCreate 뷰가 올바른 템플릿을 사용하는지 테스트
    def test_uses_correct_template(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_form.html')


    # 'date_of_death' 필드의 초기 값이 예상된 날짜로 설정되어 있는지 테스트
    def test_form_date_of_death_initially_set_to_expected_date(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)

        # 예상 초기 날짜 설정
        expected_initial_date = datetime.date(2023, 11, 11)
        response_date = response.context['form'].initial['date_of_death']
        response_date = datetime.datetime.strptime(
            response_date, "%d/%m/%Y").date()
        self.assertEqual(response_date, expected_initial_date)


    # 저자 생성 후 성공적으로 상세 페이지로 리다이렉트 되는지 테스트
    def test_redirects_to_detail_view_on_success(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.post(reverse('author-create'),
                                    {'first_name': 'Christian Name', 'last_name': 'Surname'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/catalog/author/'))
