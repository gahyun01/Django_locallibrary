# URL 경로를 views.py에 매핑하는 데 사용 () 이 파일은 Django 프로젝트의 루트 디렉토리에 있음 )

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 기본 홈 페이지 뷰를 설정
]
