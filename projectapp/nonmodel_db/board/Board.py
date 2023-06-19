from projectapp.nonmodel_db import db_sql


def getBoardList():

    sql= """
        Select *
        From board
        Order By board_id DESC
    """

    return db_sql.getList(sql)

def getBoardList2():

    sql= """
        Select *
        From board_hospital
        Order By board_id DESC
    """

    return db_sql.getList(sql)


def findBoardId(board_title,user_id,board_time):

    sql ="""
        Select board_id
        From board
        Where board_title = '{}' and user_id = '{}' and board_time = '{}'
    """.format(board_title,user_id,board_time)

    return db_sql.getView(sql)


### 게시글 테이블에 데이터 작성
def setBoardInsert(board_title,board_content,user_id,board_time) :
    
    sql = """
            Insert Into board (
                board_title, board_content, user_id,board_time
            ) Values (
                '{}', '{}', '{}','{}'
            )
    """.format(board_title,board_content,user_id,board_time)

    return db_sql.setCUD(sql)

def setBoardInsert2(hospital,address,reviewStar,reviewContents,user_id,board_time) :
    
    sql = """
            Insert Into board_hospital (
                hospital,address,reviewStar, board_content, user_id,board_time
            ) Values (
                '{}', '{}', '{}', '{}','{}','{}'
            )
    """.format(hospital,address,reviewStar,reviewContents,user_id,board_time)

    return db_sql.setCUD(sql)


### 첨부파일 데이터 삽입
def setFileInsert(file_name,board_id):

    sql = """
        Insert into file(
            fi_name,board_id
        ) Values ('{}',{});
    """.format(file_name,board_id)
    return db_sql.setCUD(sql)

def setFileDelete(fi_num):
    sql ="""
        Delete 
        From file 
        Where fi_num = {};
    """.format(fi_num)
    return db_sql.setCUD(sql)


### 게시글 검색
def searchBoard(searchField,search):

    sql = """
        Select * 
        From Board
        Where {} LIKE '%{}%';
    """.format(searchField,search)
    return db_sql.getList(sql)

def searchBoard2(searchField,search):

    sql = """
        Select * 
        From board_hospital
        Where {} LIKE '%{}%';
    """.format(searchField,search)
    return db_sql.getList(sql)



### 게시글아이디로 해당하는 값들 불러오기 (board_view)
def getBoardView(table,board_id):
    sql="""
        Select * 
        From {}
        Where board_id = {};
    """.format(table,board_id)
    return db_sql.getView(sql)

### 첫 번째 게시글 번호 조회 
def first_post(table):
    # 구문 작성
    sql=f"""
        Select board_id
        From {table} 
        ORDER BY board_id LIMIT 1"""

    return db_sql.getView(sql)

### 마지막 게시글 번호 조회 
def last_post(table):
    # 구문 작성
    sql=f"""
        Select board_id
        From {table}  
        ORDER BY board_id DESC LIMIT 1"""

    return db_sql.getView(sql)

### 해당 게시글 첨부파일 가져오기
def getBoardFileView(board_id):
    sql="""
        Select *
        From File
        Where board_id = {};
    """.format(board_id)
    return db_sql.getList(sql)



### 게시글 수정
def setBoardUpdate(board_id,board_title,board_content):
    sql ="""
        Update Board
        Set board_title= '{}', board_content='{}'
        Where board_id = {}
        """.format(board_title,board_content,board_id)
    return db_sql.setCUD(sql)


### 게시글 삭제
def setBoardDelete(board_id):
    
    sql = f"""
        Delete
        From file
        Where board_id = {board_id};

        Delete
        From rev
        Where board_id = {board_id};

        Delete
        From board
        Where board_id = {board_id};

    """
    
    return db_sql.setCUD2(sql)

def setBoardDelete2(board_id):
    
    sql = f"""

        Delete
        From board_hospital
        Where board_id = {board_id};

    """
    
    return db_sql.setCUD2(sql)


### 파일 삭제
def setFileDelete(board_id,fi_num):
    
    sql = f"""
        Delete
        From file
        Where board_id = {board_id} and fi_num not in {fi_num};
    """

    return db_sql.setCUD(sql)


### 파일 삭제 리스트

def getFileDeleteList(board_id,fi_num):
    sql = f"""
        Select fi_name
        From file
        Where board_id = {board_id} and fi_num not in {fi_num};
    """
    print(sql)
    return db_sql.getList(sql)