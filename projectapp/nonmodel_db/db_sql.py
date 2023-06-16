from projectapp.nonmodel_db.db_util import DB_Util

### 여러건 조회하기
def getList(sql) :
    ### 클래스 생성시키기
    # 클래스 생성과 동시에 conn정보와 cursor 정보를 가지고 있음
    # - 클래스 내에 변수들은 별도로 받아오지 않아도 되며, 직접 접근가능함
    db_util = DB_Util()    

    ### 딕셔너리로 변경하기
    list_row = db_util.getFetchAll(sql)
    return list_row


### 한건 조회하기
def getView(sql) :
    ### 클래스 생성시키기
    db_util = DB_Util()

    ### 딕셔너리로 변경하기
    dict_row = db_util.getFetchOne(sql)
    return dict_row


### 입력/수정/삭제 처리하기
def setCUD(sql) :
    ### 클래스 생성하기
    db_util = DB_Util()
    db_util.setCUD(sql)    

    return "작업이 정상적으로 완료되었습니다!"



### 입력/수정/삭제 처리하기
def setCUD2(sql) :
    ### 클래스 생성하기
    db_util = DB_Util()
    db_util.setCUDscript(sql)    

    return "ok"