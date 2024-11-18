from django.test import TestCase
import datetime
from catalog.forms import RenewBookForm

# Django TestCase를 상속하여 테스트 케이스 클래스 정의
class RenewBookFormTest(TestCase):

    """ 갱신 날짜가 오늘 이전인 경우 양식이 유효하지 않은지 테스트 """ 
    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        # 어제 날짜를 폼에 전달하여 RenewBookForm 생성
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())  # 유효 != False


    """ 갱신 날짜가 오늘로부터 4주 이상인 경우, 양식이 유효하지 않은지 테스트 """ 
    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)  # 4주보다 하루 더 많은 날짜
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())  # 유효 != False


    """ 갱신 날짜가 오늘인 경우 양식이 유효한지 테스트 """
    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())  # =유효 == True


    """ 갱신 날짜가 4주 이내일 경우 양식이 유효한지 테스트"""
    def test_renew_form_date_max(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())  # =유효 == True


    """ 갱신 날짜 레이블이 '갱신 날짜'인지 테스트 """
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()  # 새로운 폼 객체 생성

        # 필드에 레이블이 없거나 'renewal date'인 경우 테스트 통과
        self.assertTrue(
            form.fields['renewal_date'].label is None or
            form.fields['renewal_date'].label == 'renewal date'
        )


    """ renewal_date의 도움말 텍스트가 예상대로인지 테스트 """
    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()  # 새로운 폼 객체 생성
        self.assertEqual(
            form.fields['renewal_date'].help_text,  # 필드의 도움말 텍스트가 아래 텍스트와 일치하는지 확인
            'Enter a date between now and 4 weeks (default 3).'
        )
