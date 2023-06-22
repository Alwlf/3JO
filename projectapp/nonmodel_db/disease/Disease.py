from projectapp.nonmodel_db import db_sql


def getDiseaseOne(di_name):
    sql = """
        Select *
        From Disease
        Where di_name = '{}';
    """.format(di_name)

    return db_sql.getView(sql)