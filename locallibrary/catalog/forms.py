from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms


class RenewBookForm(forms.Form):
    """ 사서가 책을 갱신하기 위한 양식 """
    renewal_date = forms.DateField(
            help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # 날짜가 과거가 아닌지 확인
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        
        # 날짜가 사서가 변경할 수 있는 범위 내에 있는지 확인 ( 4주 이상인지 )
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        # 항상 정리된 데이터를 반환함
        return data