from projectapp.nonmodel_db import db_sql


def getBoardList():

    sql= """
        Select *
        From board
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


### 첨부파일 데이터 삽입
def setFileInsert(file_name,board_id):

    sql = """
        Insert into file(
            fi_name,board_id
        ) Values ('{}',{});
    """.format(file_name,board_id)
    return db_sql.setCUD(sql)



### 게시글 검색
def searchBoard(searchField,search):

    sql = """
        Select * 
        From Board
        Where {} LIKE '%{}%';
    """.format(searchField,search)
    return db_sql.getList(sql)


### 게시글아이디로 해당하는 값들 불러오기 (board_view)
def getBoardView(board_id):
    sql="""
        Select * 
        From Board
        Where board_id = {};
    """.format(board_id)
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
def setBoardUpdate(board_id,board_title,board_content,user_id):
    sql ="""
        Update Board
        Set board_title= '{}', board_content='{}'
        Where board_id = {}
        """.format(board_title,board_content,board_id)
    return db_sql.setCUD(sql)

### 게시글 삭제
def setBoardDelete(board_id):
    sql = """
        Delete
        From Board
        Where board_id = {};
    """.format(board_id)
    return db_sql.setCUD(sql)

