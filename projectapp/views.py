# 사용자 브라우저로 응답을 하기 위한 라이브러리 불러들이기
from django.http import HttpResponse
# 템플릿을 불러오는 라이브러리
from django.shortcuts import render

from projectapp.nonmodel_db.user import user    
from projectapp.nonmodel_db.board import Board

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

def disease_result(request):
    return render(request,		
                  "projectapp/disease_result.html", 
                  {})

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

def idChk(request):

    id_list = user.idCheck()
    
    return render(request,      
                  "projectapp/include/child.html", 
                  {"id_list":id_list})


def insert_user(request):
    idDuplication =request.POST.get("idDuplication","ERROR")
    if idDuplication == "idUncheck":
        msg = """
            <script type='text/javascript'>
                alert('아이디 중복체크를 해주세요');
                self.close();
            </script>
    """
    else:
        name = request.POST.get("name","ERROR")
        gender = request.POST.get("gender","ERROR")
        email = request.POST.get("email","ERROR")
        id = request.POST.get("id","ERROR") 
        pw = request.POST.get("pw","ERROR")

        m = user.setUserInsert(id,pw,name,gender,email)

        msg = f"""
                <script type='text/javascript'>
                    alert('회원가입이 정상적으로 완료되었습니다.');
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

