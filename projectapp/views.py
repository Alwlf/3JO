# 사용자 브라우저로 응답을 하기 위한 라이브러리 불러들이기
from django.http import HttpResponse
# 템플릿을 불러오는 라이브러리
from django.shortcuts import render

from projectapp.nonmodel_db.user import user    
from projectapp.nonmodel_db.board import Board


### 현재시간 가져오는 라이브러리
from datetime import datetime
from django.utils.dateformat import DateFormat

### File Up/Download 처리를 위한 라이브러리
from projectapp.file_util.file_util import File_Util

### 페이징 처리를 위한 라이브러리
from django.core.paginator import Paginator

import urllib

from PIL import Image

import os
path=os.path.dirname(os.path.abspath(__file__))

import base64

from io import  BytesIO

def index(request):

    board_list = Board.getBoardList()
    board_list = board_list[:6]
    return render(request,		
                  "projectapp/index.html", 
                  {"board_list":board_list})


def post(request):
    return render(request,		
                  "projectapp/post.html", 
                  {})

def disease(request):
    return render(request,		
                  "projectapp/disease.html", 
                  {})

def mypage(request):
    id = request.session["session_user_id"]

    user_view = user.userInfo(id)

    return render(request,
                  "projectapp/mypage.html",
                  {'user_view':user_view})

def update_mypage(request):
    id = request.session["session_user_id"]
    pw = request.POST.get("form_pw","ERROR")
    email = request.POST.get("form_email","ERROR")
    
    m = user.update_mypage(id,pw,email)

    msg = f"""
            <script type='text/javascript'>
                alert('회원 정보 수정이 정상적으로 완료되었습니다.');
                location.href = '/project/mypage/';
            </script>
    """
    return HttpResponse(msg)





def inputpost(request):
    return render(request,      
                  "projectapp/inputpost.html", 
                  {})

def idChk(request):

    id_list = user.idCheck()
    
    return render(request,      
                  "projectapp/include/child.html", 
                  {"id_list":id_list})

def insert_user(request):
    name = request.POST.get("name","ERROR")
    gender = request.POST.get("gender","ERROR")
    email = request.POST.get("email","ERROR")
    id = request.POST.get("id","ERROR") 
    pw = request.POST.get("pw1","ERROR")

    try :
        m = user.setUserInsert(id,pw,name,gender,email)
    except :
        msg = """
            <script type='text/javascript'>
                alert('아이디 중복 체크를 해주세요.');
                location.href = '/project/';
            </script>
        """
        return HttpResponse(msg)
    
    msg = """
            <script type='text/javascript'>
                alert('회원가입이 정상적으로 완료되었습니다.');
                location.href = '/project/';
            </script>
    """
    return HttpResponse(msg)


### 로그인 인증 처리
def login_chk(request):

    id = request.POST.get("user_id","ERROR")
    pw = request.POST.get("user_pw","ERROR")

    user_view = user.setLoginUser(id,pw)


    if user_view.get("RS") == "Data_None" :
        msg = """
            <script type="text/javascript">
                alert('아이디 또는 패스워드를 확인해주세요!!');
                history.go(-1);
            </script>
        """
        return HttpResponse(msg)
    
    elif user_view.get("RS") == "DB_ERROR" :
        msg = """
            <script type="text/javascript">
                alert('시스템에 문제가 있네요~! 잠시 후 다시 접근하세요!!');
                location.href = '/';
            </script>
        """
        return HttpResponse(msg)
    
    request.session["session_user_id"] = id
    request.session["session_user_name"] = user_view.get("user_name")


    msg = """
            <script type='text/javascript'>
                alert('환영합니다. [{}]님 로그인 되었습니다.');
                location.href = '/';
            </script>
    """.format(user_view.get("user_name"))


    
    return HttpResponse(msg)


### 로그아웃 처리 기능
def logout_chk(request) :
    ### 로그아웃의 의미 : session 정보를 삭제하면 됨...
    request.session.flush()
    
    msg = """
        <script type='text/javascript'>
            alert('로그아웃 되었습니다.');
            location.href = '/';
        </script>
    """
    return HttpResponse(msg)



def setFileInsert(request) :
    url = request.POST.get("img")
    img=Image.open(BytesIO(urllib.request.urlopen(url).read()))
    
    img=img.resize((640,440))
    img_full_name="/static/projectapp/images/image.jpg"
    img.save(path+img_full_name)
    return render(request,
                  "projectapp/disease_result.html",
                  {"img_full_name":img_full_name})



### 게시판 목록보기
def board(request):

    board_list = Board.getBoardList()
   

    searchField = request.GET.get('searchField','ERROR')
    search = request.GET.get('searchText','ERROR')
    
    if search =="":
        msg = """
                <script type='text/javascript'>
                    alert('다시 입력해주세요.');
                    location.href = '/project/board/';
                </script>
            """
        return HttpResponse(msg)
    if search != "ERROR":
        board_list = Board.searchBoard(searchField,search)
        
        if not board_list:
            msg = """
                <script type='text/javascript'>
                    alert('검색결과가 없습니다');
                    location.href = '/project/board/';
                </script>
            """
            return HttpResponse(msg)

    now_page = request.GET.get("page", "1")
    now_page = int(now_page)
    num_row = 5

    p = Paginator(board_list, num_row)

    #  # Change 10 to the number of items per page you desire
    rows_data = p.get_page(now_page)
    
    start_page = (now_page-1) // num_row * num_row + 1
    end_page = start_page + 3
    if end_page > p.num_pages :
        end_page = p.num_pages

    ####################################
    ###     다음 / 이전 버튼 처리     ###
    ####################################
    ### 다음/이전 버튼을 보여줄지 여부 처리
    is_prev = False # 이전
    is_next = False # 다음

    ### 이전 버튼 보여줄지 여부 처리
    if start_page > 1 :
        is_prev = True

    ### 다음 버튼 보여줄지 여부 처리
    if end_page < p.num_pages :
        is_next = True
   
    context = {
        ### 화면에 보여줄 10개의 행을 담고 있는 데이터
        "board_list" : rows_data,
        ### 페이지 번호의 시작(start_page)~종료(end_page) 범위
        "page_range" : range(start_page, end_page+1),
        ### 이전 버튼 보여줄지 여부
        "is_prev" : is_prev,
        ### 다음 버튼 보여줄지 여부
        "is_next" : is_next,
        ### 시작번호(start_page)
        "start_page" : start_page,
        ### 선택된 페이지 번호가 현재 페이지와 같은지 여부 확인용
        "now_page" : now_page,
        
        ### 검색 유형 (글 제목, 작성자)
        'searchField' :searchField,
        ### 검색 내용
        'searchText':search
    }
    
   
    return render(request,
                  "projectapp/board.html", 
                #   {"board_list":board_list},
                    context,
                  )

### 게시글 조회
def boardView(request):
    board_id = request.GET.get("board_id","ERROR")


    board_view = Board.getBoardView(board_id)


    return render(request,		
                  "projectapp/board_view.html", 
                  {"board_view":board_view})

### 게시글 수정 폼
def boardUpdateForm(request):

    board_id = request.GET.get("board_id","ERROR")


    board_view = Board.getBoardView(board_id)

    return render(request,"projectapp/board_update_form.html",
                  {"board_view":board_view})

### 게시글 수정 
def boardUpdate(request):
    board_id = request.POST.get("board_id",'')
    board_title = request.POST.get("board_title",'')
    board_content = request.POST.get("board_content",'')
    user_id = request.POST.get("user_id",'')

    update_chk = Board.setBoardUpdate(board_id,board_title,board_content,user_id)

    msg = """
            <script type='text/javascript'>
                alert('{}');
                location.href = '/project/board/';
            </script>
    """.format(update_chk)
    return HttpResponse(msg)


### 게시글 삭제
def boardDelete(request):
    try:

        board_id = request.GET.get("board_id","ERROR")
        user_id = request.GET.get("user_id","ERROR")
        
        delete_chk = Board.setBoardDelete(board_id)
    
    except:
            msg = """
                <script type='text/javascript'>
                    alert('잘못된 접근입니다.!!');
                    location.href = '/project/board/';
                </script>
            """
            return HttpResponse(msg)

    msg = """
            <script type='text/javascript'>
                alert('정상적으로 삭제되었습니다!');
                location.href='/project/board/';
            </script>
    """
    return HttpResponse(msg)





### 게시글 작성
def post(request):

    board_title = request.POST.get("title","ERROR")
    board_content = request.POST.get("content","ERROR")
    user_id = request.session.get("session_user_id")
    board_time = DateFormat(datetime.now()).format('Y.m.d H:i')
    
    if request.FILES.get("file_nm") is not None :
            file_nm = request.FILES.get("file_nm")
    else :
            file_nm = ""

    # board_time = datetime.now()
    
    board_chk = Board.setBoardInsert(board_title,board_content,user_id,board_time)
    

    board_list = Board.findBoardId(board_title,user_id,board_time)
    board_id=board_list['board_id']

    if file_nm != "" :
        ###########[ File Upload 처리하기 ]##########
        ### - 파일 업로드 폴더 위치 지정 및 물리적 위치 생성하기
        upload_dir = "./projectapp/static/projectapp/board_file/"
        download_dir = "./projectapp/static/projectapp/board_file/"

        ### 파일(이미지)을 페이지에 보여줄 경우 : 폴더 전체 경로 지정
        img_dir = "/static/projectapp/board_file/"

        ### File_Uitl 클래스 생성하기
        fu = File_Util()

        ### 초기값 셋팅(설정)하기
        fu.setUpload(file_nm, upload_dir, img_dir, download_dir)

        ### 파일 업로드 실제 수행하기*****
        fu.fileUpload()

        ########## [ 업로드된 파일 정보 조회 ] #########
        ### 파일 사이즈
        file_size = fu.file_size
        ### 업로드된 파일명
        filename = fu.filename
        ### <img> 태그에 넣을 src 전체 경로
        img_full_name = fu.img_full_name
        ### (DB 저장용) 다운로드 전체경로+파일명
        download_full_name = fu.download_full_name

        board_ee=Board.setFileInsert(filename,board_id)
    # if board_id
    
    msg = """
        <script type='text/javascript'>
            alert('{}');
            location.href = '/project/board/';
        </script>
    """.format(board_chk)

    return HttpResponse(msg)

# 아이디 찾기
def search_id(request):
    try:
        user_name=request.POST.get("user_name","A")
        user_email=request.POST.get("user_email","B")

        rs_msg=user.search_user_id(user_name,user_email)

        ms = rs_msg['user_id']

        msg="""
            <script type='text/javascript'>
                alert('{}');
                location.href='/project/';
            </script>
        """.format(ms)
        return HttpResponse(msg)
    
    except:
        msg = """
            <script type='text/javascript'>
                alert('이름 또는 이메일을 확인해 주세요.');
                location.href = '/project/';
            </script>
        """
        return HttpResponse(msg)


# 비번 찾기
def search_pw(request):
    try:
        user_id=request.POST.get("user_id","A")
        user_email=request.POST.get("user_email","B")
        
        rs_msg=user.search_user_pw(user_id,user_email)

        ms = rs_msg['user_pw']
        
        msg="""
            <script type='text/javascript'>
                alert('{}');
                location.href='/project/';
            </script>
        """.format(ms)
        return HttpResponse(msg)
    
    except:
        msg = """
            <script type='text/javascript'>
                alert('아이디 또는 이메일을 확인해 주세요.');
                location.href = '/project/';
            </script>
        """
        return HttpResponse(msg)

def mapview(request):
    return render(request,
                  "projectapp/map_view.html",
                  {})

