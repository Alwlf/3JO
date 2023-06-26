from projectapp.nonmodel_db import db_sql

### 질병 데이터 가져오기
def getDiseaseOne(di_name):
    sql = """
        Select *
        From Disease
        Where di_name = '{}';
    """.format(di_name)

    return db_sql.getView(sql)