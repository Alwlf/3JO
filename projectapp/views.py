# 사용자 브라우저로 응답을 하기 위한 라이브러리 불러들이기
from django.http import HttpResponse
# 템플릿을 불러오는 라이브러리
from django.shortcuts import render

from projectapp.nonmodel_db.user import user    
from projectapp.nonmodel_db.board import Board

### File Up/Download 처리를 위한 라이브러리
from projectapp.file_util.file_util import File_Util

import urllib

def index(request):

    # board_list =  {"board_title":"EEEE"}
    board_list = Board.getBoardList()
    return render(request,		
                  "projectapp/index.html", 
                  {"board_list":board_list})

def board(request):

    board_list = Board.getBoardList()
    return render(request,		
                  "projectapp/board.html", 
                  {"board_list":board_list})

def post(request):
    return render(request,		
                  "projectapp/post.html", 
                  {})

def disease(request):
    return render(request,		
                  "projectapp/disease.html", 
                  {})
def disease2(request):
    return render(request,		
                  "projectapp/disease2.html", 
                  {})

def disease_result(request):
    return render(request,		
                  "projectapp/disease_result.html", 
                  {})
# def disease_result2(request):
#     img = request.GET["image"]
#     # print(img)
#     print(urllib.request.urlopen(img[5:]))
#     return render(request,		
#                   "projectapp/disease_result2.html", 
#                   {"image":img})

### File Upload 처리하기
def setFileInsert(request) :
    try :
        title = request.POST.get("title")

        if request.FILES.get("fileUpload") is not None :
            file_nm = request.FILES.get("fileUpload")
        else :
            file_nm = ""
        #file_nm = request.POST.get("fileUpload")
        print(request.POST,request.FILES,file_nm)
    except :
        pass
    if file_nm != "" :
        ###########[ File Upload 처리하기 ]##########
        ### - 파일 업로드 폴더 위치 지정 및 물리적 위치 생성하기
        upload_dir = "./projectapp/static/projectapp/file_UpDown/"
        download_dir = "./projectapp/static/projectapp/file_UpDown/"

        ### 파일(이미지)을 페이지에 보여줄 경우 : 폴더 전체 경로 지정
        img_dir = "/static/projectapp/file_UpDown/"

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

        ####### [Database 이용시]
        # 컬럼은 두개사용 : img_full_name, download_full_name

    # msg = """
    #     <p><img src='{0}'></p>
    # """.format(img_full_name, file_size, 
    #            filename, download_full_name)
    
    return render(request,
                  "projectapp/disease_result2.html",
                  {"img_full_name":img_full_name})
    # return HttpResponse(msg)



def mypage(request):
    return render(request,		
                  "projectapp/mypage.html", 
                  {})

def update_mypage(request):
    return render(request,		
                  "projectapp/update_mypage.html", 
                  {})


def boardView(request):
    return render(request,		
                  "projectapp/board_view.html", 
                  {})


def inputpost(request):
    return render(request,      
                  "projectapp/inputpost.html", 
                  {})



def insert_user(request):

    name = request.POST.get("name","ERROR")
    gender = request.POST.get("gender","ERROR")
    email = request.POST.get("email","ERROR")
    id = request.POST.get("id","ERROR")
    pw = request.POST.get("pw","ERROR")

    m = user.setUserInsert(id,pw,name,gender,email)

    msg = f"""
            <script type='text/javascript'>
                alert('{id}'+'/'+'{pw}');
                location.href = '/project/';
            </script>
    """
    return HttpResponse(msg)


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
    
    # request.session["ses_user_id"] = id
    # request.session["ses_user_name"] = user_view.get("user_name")


    msg = """
            <script type='text/javascript'>
                alert('환영합니다. [{}]님 로그인 되었습니다.');
                location.href = '/project/';
            </script>
    """.format(user_view.get("user_name"))


    
    return HttpResponse(msg)


# ### 로그아웃 처리 기능
# def logout_chk(request) :
#     ### 로그아웃의 의미 : session 정보를 삭제하면 됨...
#     request.session.flush()
    
#     msg = """
#         <script type='text/javascript'>
#             alert('로그아웃 되었습니다.');
#             location.href = '/';
#         </script>
#     """
#     return HttpResponse(msg)

