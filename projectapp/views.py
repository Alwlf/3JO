# 사용자 브라우저로 응답을 하기 위한 라이브러리 불러들이기
from django.http import HttpResponse
# 템플릿을 불러오는 라이브러리
from django.shortcuts import render,redirect

from projectapp.nonmodel_db.user import user    
from projectapp.nonmodel_db.board import Board
from projectapp.nonmodel_db.review import Review
from projectapp.nonmodel_db.disease import Disease

### 현재시간 가져오는 라이브러리
from datetime import datetime
from django.utils.dateformat import DateFormat

### File Up/Download 처리를 위한 라이브러리
from projectapp.file_util.file_util import File_Util

### 페이징 처리를 위한 라이브러리
from django.core.paginator import Paginator

### 피부 모델 가져오기
from projectapp.dc_model.model_pred import *

import urllib
import numpy as np
from PIL import Image

import os
path=os.path.dirname(os.path.abspath(__file__))

import base64

from io import  BytesIO

### 한번 실행해서 로딩시간 줄이기 
a=Image.open(path+"/static/projectapp/images/dogeye.png")
for i in ["dog","cat"]:
    for j in ["pibu","eye"]:
        bot_model(i,j,a)

### 인덱스 페이지
def index(request):

    board_list = Board.getBoardList()
    board_list = board_list[:6]
    return render(request,		
                  "projectapp/index.html", 
                  {"board_list":board_list})

### 진단 페이지
def disease(request):
    dc=request.GET.get("dc")
    return render(request,		
                  "projectapp/disease.html", 
                  {"dc":dc})

### 마이페이지
def mypage(request):
    id = request.session["session_user_id"]

    user_view = user.userInfo(id)

    return render(request,
                  "projectapp/mypage.html",
                  {'user_view':user_view})

### 회원 정보 수정
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

### 아이디 중복 체크
def idChk(request):

    id_list = user.idCheck()
    
    return render(request,      
                  "projectapp/include/child.html", 
                  {"id_list":id_list})

### 회원가입
def insert_user(request):
    name = request.POST.get("name","ERROR")
    gender = request.POST.get("gender","ERROR")
    email = request.POST.get("email","ERROR")
    id = request.POST.get("id","ERROR") 
    pw = request.POST.get("pw1","ERROR")
    url = request.POST.get("url_su","ERROR")

    try :
        m = user.setUserInsert(id,pw,name,gender,email)
    except :
        msg = f"""
            <script type='text/javascript'>
                alert('아이디 중복 체크를 해주세요.');
                location.href = '{url}';
            </script>
        """
        return HttpResponse(msg)
    
    msg = f"""
            <script type='text/javascript'>
                alert('회원가입이 정상적으로 완료되었습니다.');
                location.href = '{url}';
            </script>
    """
    return HttpResponse(msg)

### 아이디 찾기
def search_id(request):
    try:
        user_name=request.POST.get("user_name","A")
        user_email=request.POST.get("user_email","B")
        url = request.POST.get("url_fi","ERROR")

        rs_msg=user.search_user_id(user_name,user_email)

        ms = rs_msg['user_id']

        msg="""
            <script type='text/javascript'>
                alert('{}');
                location.href='{}';
            </script>
        """.format(ms,url)
        return HttpResponse(msg)
    
    except:
        msg = f"""
            <script type='text/javascript'>
                alert('이름 또는 이메일을 확인해 주세요.');
                location.href = '{url}';
            </script>
        """
        return HttpResponse(msg)


### 비번 찾기
def search_pw(request):
    try:
        user_id=request.POST.get("user_id","A")
        user_email=request.POST.get("user_email","B")
        url = request.POST.get("url_fw","ERROR")
        
        rs_msg=user.search_user_pw(user_id,user_email)

        ms = rs_msg['user_pw']
        
        msg="""
            <script type='text/javascript'>
                alert('{}');
                location.href='{}';
            </script>
        """.format(ms,url)
        return HttpResponse(msg)
    
    except:
        msg = f"""
            <script type='text/javascript'>
                alert('아이디 또는 이메일을 확인해 주세요.');
                location.href = '{url}';
            </script>
        """
        return HttpResponse(msg)


### 로그인 처리 기능
def login_chk(request):

    id = request.POST.get("user_id","")
    pw = request.POST.get("user_pw","")
    url = request.POST.get("url","ERROR")

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
    ## 해당 아이디의 이름 값 가져오기
    request.session["session_user_name"] = user_view.get("user_name")


    msg = """
            <script type='text/javascript'>
                alert('환영합니다. [{}]님 로그인 되었습니다.');
                location.href = '{}';
            </script>
    """.format(user_view.get("user_name"),url)

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


### 진단 결과 페이지
def setFileInsert(request) :
    url = request.POST.get("img")

    options=request.POST.get("inlineRadioOptions")
    dc=request.POST.get("dc")
    
    #print(request.POST)
    if url:
        # 바이트 이미지 변환
        img=Image.open(BytesIO(urllib.request.urlopen(url).read()))
        #보여주는 이미지 사이즈 조절
        img_view=img.resize((640,440))
        # 이지미 저장 경로 
        img_full_name="/static/projectapp/images/image.jpg"
        # 이미지 저장
        img_view=img_view.convert("RGB")
        img_view.save(path+img_full_name)

        # 모델 
        p,b=bot_model(dc,options,img)

        di_name=b.replace(' ','')
      
        di_view = Disease.getDiseaseOne(di_name)
        
        show_image_path="/static/projectapp/bot/"+di_name
        
        show_image_paths=[]
        
        # print(os.listdir(path+show_image_path))
        img_lis=os.listdir(path+show_image_path)
        if img_lis:
            img_lis=np.random.choice(img_lis,3)
        for i in img_lis:
            show_image_paths.append(show_image_path+"/"+i)
        
    else:
        msg = """
        <script type='text/javascript'>
            alert('이미지가 없습니다.');
            history.go(-1);
        </script>
            """
        return HttpResponse(msg)
    return render(request,
                  "projectapp/disease_result.html",
                  {"img_full_name":img_full_name,
                   "result_b":b,
                   "result_p":p,
                   "show_image_path":show_image_paths,
                   "di_view":di_view})


### 자유 게시판 목록보기
def board(request):

    board_list = Board.getBoardList()
   

    searchField = request.GET.get('searchField','ERROR')
    search = request.GET.get('searchText','ERROR')
    
    if search =="":
        msg = """
                <script type='text/javascript'>
                    alert('검색어를 입력해주세요.');
                    location.href = '/project/board/';
                </script>
            """
        return HttpResponse(msg)
    if search != "ERROR":
        board_list = Board.searchBoard(searchField,search)
        
        if not board_list:
            msg = """
                <script type='text/javascript'>
                    alert('검색 결과가 없습니다');
                    location.href = '/project/board/';
                </script>
            """
            return HttpResponse(msg)

    now_page = request.GET.get("page", "1")
    now_page = int(now_page)
    num_row = 5

    p = Paginator(board_list, num_row)

    #  # Change 5 to the number of items per page you desire
    rows_data = p.get_page(now_page)
    
    start_page = (now_page-1) // num_row * num_row + 1
    end_page = start_page + 5
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
        ### 화면에 보여줄 5개의 행을 담고 있는 데이터
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

### 리뷰 게시판 목록보기
def board_hospital(request):

    board_list = Board.getBoardList2()
    searchField = request.GET.get('searchField','ERROR')
    search = request.GET.get('searchText','ERROR')
    
    if search =="":
        msg = """
                <script type='text/javascript'>
                    alert('검색어를 입력해주세요.');
                    location.href = '/project/board_hospital/';
                </script>
            """
        return HttpResponse(msg)
    if search != "ERROR":
        board_list = Board.searchBoard2(searchField,search)
        
        if not board_list:
            msg = """
                <script type='text/javascript'>
                    alert('검색결과가 없습니다');
                    location.href = '/project/board_hospital/';
                </script>
            """
            return HttpResponse(msg)

    now_page = request.GET.get("page", "1")
    now_page = int(now_page)
    num_row = 5

    p = Paginator(board_list, num_row)

    #  # Change 5 to the number of items per page you desire
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
        ### 화면에 보여줄 5개의 행을 담고 있는 데이터
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
                  "projectapp/board_hospital.html", 
                    context,
                  )

### 자유 게시판 게시글 조회
def boardView(request):
    board_id = request.GET.get("board_id","ERROR")

    first_id = Board.first_post('board')
    last_id = Board.last_post('board')
    goButton = request.GET.get("goButton",'')
    
    ## 이전글 다음글 기능
    if goButton =="goPrev":
        board_id = Board.getBoardPrevView('board',board_id)
        board_id = board_id['board_id']
        return redirect('/project/board_view/?board_id='+str(board_id))
    if goButton =="goNext":
        board_id = Board.getBoardNextView('board',board_id)
        board_id = board_id['board_id']
        return redirect('/project/board_view/?board_id='+str(board_id))
        
    ## 해당 게시글 보여주기    
    board_view = Board.getBoardView('board',board_id)
    
    ## 해당 게시글의 사진 보여주기
    file_list = Board.getBoardFileView(board_id)

    ## 댓글 기능
    rev_content = request.POST.get("rev_content")
    # print(request.POST)
    if (rev_content is not None) and (rev_content !="") :
        user_id = request.session.get("session_user_id")
        rev_chk = Review.setReviewInsert(rev_content,user_id,board_id)
        if rev_chk !="작업이 정상적으로 완료되었습니다!":
            msg = """
                <script type='text/javascript'>
                    alert('다시작성해주세요');
                    location.href = '/project/board_view/?board_view'+board_id;
                </script>
            """
            return HttpResponse(msg)
        else :
            rev_content=""
        return redirect('/project/board_view/?board_id='+board_id)
    
    
    review_list = Review.getReviewList(board_id)
    
    return render(request,		
                  "projectapp/board_view.html", 
                  {"board_view":board_view,
                    ## 게시글 사진
                  "file_list":file_list,
                    ## 처음 게시글과 마지막 게시글 번호
                  "last_id":last_id,
                  "first_id":first_id,
                    ## 댓글
                  "review_lst":review_list})

### 리뷰 게시판 게시글 조회
def boardview2(request):
    board_id = request.GET.get("board_id","ERROR")

    first_id = Board.first_post('board_hospital')
    last_id = Board.last_post('board_hospital')
    goButton = request.GET.get("goButton",'')
    
    ## 이전글 다음글 기능
    if goButton =="goPrev":
        board_id = Board.getBoardPrevView('board_hospital',board_id)
        board_id = board_id['board_id']
        return redirect('/project/board_view2/?board_id='+str(board_id))
    if goButton =="goNext":
        board_id = Board.getBoardNextView('board_hospital',board_id)
        board_id = board_id['board_id']
        return redirect('/project/board_view2/?board_id='+str(board_id))

    board_view = Board.getBoardView('board_hospital',board_id)

    return render(request,		
                  "projectapp/board_view2.html", 
                  {"board_view":board_view,
                   ## 처음 게시글과 마지막 게시글 번호
                  "last_id":last_id,
                  "first_id":first_id})

### 자유 게시판 글쓰기 페이지
def inputpost(request):
    return render(request,      
                  "projectapp/inputpost.html", 
                  {})

### 리뷰 게시판 글쓰기 페이지
def inputpost2(request):
    return render(request,      
                  "projectapp/inputpost2.html", 
                  {})

### 게시글 작성
def post(request):

    board_title = request.POST.get("title","ERROR")
    board_content = request.POST.get("content","ERROR")
    user_id = request.session.get("session_user_id")
    # 글을 작성한 시간
    board_time = DateFormat(datetime.now()).format('Y.m.d H:i')
    
    if user_id :

        if request.FILES.get("fi_name") is not None :
                fi_name = dict(request.FILES).get("fi_name")
                # print(fi_name)
        else :
                fi_name = ""
        
        
        board_chk = Board.setBoardInsert(board_title,board_content,user_id,board_time)
        

        board_list = Board.findBoardId(board_title,user_id,board_time)
        board_id=board_list['board_id']

        if fi_name != "" :

            for data in fi_name:

                ###########[ File Upload 처리하기 ]##########
                ### - 파일 업로드 폴더 위치 지정 및 물리적 위치 생성하기
                upload_dir = "./projectapp/static/projectapp/board_file/"
                download_dir = "./projectapp/static/projectapp/board_file/"

                ### 파일(이미지)을 페이지에 보여줄 경우 : 폴더 전체 경로 지정
                img_dir = "/static/projectapp/board_file/"

                ### File_Uitl 클래스 생성하기
                fu = File_Util()

                ### 초기값 셋팅(설정)하기
                fu.setUpload(data, upload_dir, img_dir, download_dir)

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
                
                img=Image.open(path+img_full_name)
                
                img=img.resize((620,450))
                img=img.convert("RGB")
                img.save(path+img_full_name)

        msg = """
            <script type='text/javascript'>
                alert('{}');
                location.href = '/project/board/';
            </script>
        """.format(board_chk)
    
    else :
         
         msg = """
            <script type='text/javascript'>
                alert('로그인을 해주세요!');
                location.href = '/project/board/';
            </script>
        """
    return HttpResponse(msg)


### 리뷰 게시글 작성
def post2(request):

    hospital = request.POST.get("hospital","ERROR")
    address =  request.POST.get("address","ERROR")
    reviewStar = request.POST.get("reviewStar","ERROR")
    reviewContents = request.POST.get("reviewContents","ERROR")
    user_id = request.session.get("session_user_id")
    #글을 작성한 시간
    board_time = DateFormat(datetime.now()).format('Y.m.d H:i')
    
    if user_id :
        
        board_chk = Board.setBoardInsert2(hospital,address,reviewStar,reviewContents,user_id,board_time)

        msg = """
            <script type='text/javascript'>
                alert('{}');
                location.href = '/project/board_hospital/';
            </script>
        """.format(board_chk)
    
    else :
         
         msg = """
            <script type='text/javascript'>
                alert('로그인을 해주세요!');
                location.href = '/project/board_hospital/';
            </script>
        """
    return HttpResponse(msg)


### 게시글 수정 폼
def boardUpdateForm(request):

    board_id = request.GET.get("board_id","ERROR")

    board_view = Board.getBoardView('board',board_id)
    file_list = Board.getBoardFileView(board_id)

    return render(request,"projectapp/board_update_form.html",
                  {"board_view":board_view,
                   "file_list":file_list})

### 리뷰 게시글 수정 폼
def boardUpdateForm2(request):

    board_id = request.GET.get("board_id","ERROR")
 
    board_view = Board.getBoardView('board_hospital',board_id)

    return render(request,"projectapp/board_update_form2.html",
                  {"board_view":board_view})


### 게시글 수정 
def boardUpdate(request):
    board_id = request.POST.get("board_id",'')
    board_title = request.POST.get("board_title",'')
    board_content = request.POST.get("board_content",'')
    user_id = request.POST.get("user_id",'')

    # print(request.POST)
    # print(dict(request.POST)['fi_num'])

    if request.FILES.get("file_nm") is not None :
            file_nm = request.FILES.get("file_nm")
    else :
            file_nm = ""
    
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

            fileInsert_chk = Board.setFileInsert(filename,board_id)

            img=Image.open(path+img_full_name)
            
            img=img.resize((620,450))
            img=img.convert("RGB")
            img.save(path+img_full_name)

            
    fi_num = dict(request.POST).get("fi_num",'')
    
    fi_num = tuple(map(int,fi_num))
    
    if 0 in fi_num:
        if len(fi_num) == 1:
            fi_num = f"({fi_num[0]})"
        file_delete_list = Board.getFileDeleteList(board_id,fi_num)
        
        for ee in file_delete_list:   ### 로컬에서 이미지 삭제
            if os.path.exists(path+'/static/projectapp/board_file/'+ee['fi_name']) :
                # print(path+'/static/projectapp/board_file/'+ee['fi_name'])
                os.remove(path+'/static/projectapp/board_file/'+ee['fi_name'])
        fi_delete_chk = Board.setFileDelete(board_id,fi_num) ### file db 데이터 삭제

    update_chk = Board.setBoardUpdate(board_id,board_title,board_content)

    # setFileDelete(file_nm)
    
    msg = """
            <script type='text/javascript'>
                alert('{}');
                location.href = '/project/board/';
            </script>
    """.format(update_chk)
    return HttpResponse(msg)


### 리뷰 게시글 수정 
def boardUpdate2(request):
    board_id = request.POST.get("board_id",'')
    hospital = request.POST.get("hospital",'')
    address = request.POST.get("address",'')
    reviewStar = request.POST.get("reviewStar",'')
    board_content = request.POST.get("board_content",'')
    
    update_chk = Board.setBoardUpdate2(board_id,hospital,address,reviewStar,board_content)

    msg = """
            <script type='text/javascript'>
                alert('{}');
                location.href = '/project/board_hospital/';
            </script>
    """.format(update_chk)
    return HttpResponse(msg)


### 게시글 삭제
def boardDelete(request):
    try:

        board_id = request.GET.get("board_id","ERROR")
        
        file_view = Board.getBoardFileView(board_id)
        # print(file_view)
        delete_chk = Board.setBoardDelete(board_id)
        # print(delete_chk)

        for ee in file_view:
            if os.path.exists(path+'/static/projectapp/board_file/'+ee['fi_name']) :
                # print(path+'/static/projectapp/board_file/'+ee['fi_name'])
                os.remove(path+'/static/projectapp/board_file/'+ee['fi_name'])

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


### 리뷰 게시글 삭제
def boardDelete2(request):
    try:

        board_id = request.GET.get("board_id","ERROR")

        delete_chk = Board.setBoardDelete2(board_id)
        

    except:
            msg = """
                <script type='text/javascript'>
                    alert('잘못된 접근입니다.!!');
                    location.href = '/project/board_hospital/';
                </script>
            """
            return HttpResponse(msg)

    msg = """
            <script type='text/javascript'>
                alert('정상적으로 삭제되었습니다!');
                location.href='/project/board_hospital/';
            </script>
    """
    return HttpResponse(msg)



## 댓글 삭제
def reviewDelete(request):
 
    rev_id = request.GET.get("rev_id",'')
    board_id = request.GET.get("board_id",'')
    review_chk=Review.setReviewDelete(rev_id)
    
    msg = """
            <script type='text/javascript'>
                alert('{}');
                location.href=history.go(-1);
            </script>
        """.format(review_chk)
    return redirect('/project/board_view/?board_id='+board_id)



