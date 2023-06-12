from projectapp.nonmodel_db import db_sql


def getBoardList():

    sql= """
        Select *
        From board
        Order By board_id Desc
    """

    return db_sql.getList(sql)