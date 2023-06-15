from projectapp.nonmodel_db import db_sql



### 입력 처리하기
def setUserInsert(id,pw,name,gender,email) :
    ### 구문 작성
    sql = """
            Insert Into user (
                user_id,user_pw,user_name,user_gender,user_email
            ) Values (
                '{}', '{}', '{}','{}','{}'
            )
    """.format(id,pw,name,gender,email)

    return db_sql.setCUD(sql)


### 로그인하기
def setLoginUser(user_id,user_pw) :
    ### 구문 작성
    sql = """
        Select *
        From user
        Where user_id = '{}' and user_pw = '{}'
    """.format(user_id,user_pw)

    return db_sql.getView(sql)


### 아이디 중복
def idCheck():
    ### 구문 작성
    sql = """
        Select user_id
        From user
    """

    return db_sql.getList(sql)


### 회원 정보 수정
def update_mypage(id,pw,email):
    ### 구문 작성
    sql = """
        Update user
            Set user_pw = '{}',
                user_email = '{}'
        Where user_id = '{}'
    """.format(pw,email,id)
    
    return db_sql.setCUD(sql)

### 회원 정보 조회
def userInfo(id):
    ### 구문 작성
    sql = f"""
        Select user_name, user_gender, user_pw, user_email
        From user
        Where user_id = '{id}'
    """
    
    return db_sql.getView(sql)

# 아이디 찾기
def search_user_id(user_name,user_email):
    # 구문 작성
    sql="""
        Select user_id
        From user
        Where user_name = '{}' and user_email = '{}'
    """.format(user_name,user_email)

    return db_sql.getView(sql)

# 비번 찾기
def search_user_pw(user_id,user_email):
    # 구문 작성
    sql="""
        Select user_pw
        From user
        Where user_id = '{}' and user_email = '{}'
    """.format(user_id,user_email)

    return db_sql.getView(sql)
