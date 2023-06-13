from django.urls import path
from . import views		

urlpatterns = [
    # http://127.0.0.1:8000/project/

    # 인덱스 페이지
    path('',views.index),
    path('index/',views.index),
  
    # 게시글
    path('post/',views.post),
    # 진단하기
    path('disease/',views.disease),
    # 진단 결과
    # path('disease_result/',views.disease_result),
    # 진단 결과
    path('disease_result/',views.setFileInsert),
    # 마이 페이지
    path('mypage/',views.mypage),
    # 회원 정보 수정
    path('update_mypage/',views.update_mypage),

    #로그인
    path('login_chk/',views.login_chk),
    # 회원 가입
    path('insert/',views.insert_user),
    # 아이디 중복 체크
    path('idChk/',views.idChk),

    # 게시판
    path('board/',views.board),
    # 게시판 글쓰기
    path('inputpost/',views.inputpost),
    # 게시판 상세조회
    path('board_view/',views.boardView),

]
