from projectapp.nonmodel_db import db_sql

### 댓글 데이터 가져오기
def getReviewList(board_id):

    sql= """
        Select *
        From review
        Where board_id = {}
        Order By board_id DESC
    """.format(board_id)

    return db_sql.getList(sql)

### 댓글 데이터 입력하기
def setReviewInsert(rev_content,user_id,board_id):
    
    sql = """
            Insert Into review (
                rev_content, user_id, board_id
            ) Values (
                '{}', '{}', '{}'
            )
    """.format(rev_content,user_id,board_id)
       
    return db_sql.setCUD(sql)

### 댓글 데이터 삭제하기 
def setReviewDelete(rev_id):
    sql="""
        Delete 
        From review 
        Where rev_id = {};
    """.format(rev_id)
    return db_sql.setCUD(sql)    