from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='catalog-home'),  # 기본 홈 페이지 뷰를 설정
]
