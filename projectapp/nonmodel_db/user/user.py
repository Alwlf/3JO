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