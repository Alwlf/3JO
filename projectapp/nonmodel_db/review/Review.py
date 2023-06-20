from projectapp.nonmodel_db import db_sql


def getReviewList(board_id):

    sql= """
        Select *
        From review
        Where board_id = {}
        Order By board_id DESC
    """.format(board_id)

    return db_sql.getList(sql)


def setReviewInsert(rev_content,user_id,board_id):
    
    sql = """
            Insert Into review (
                rev_content, user_id, board_id
            ) Values (
                '{}', '{}', '{}'
            )
    """.format(rev_content,user_id,board_id)
       
    return db_sql.setCUD(sql)

       
def setReviewDelete(rev_id):
    sql="""
        Delete 
        From review 
        Where rev_id = {};
    """.format(rev_id)
    return db_sql.setCUD(sql)    