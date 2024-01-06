import pymysql
import os

def get_db_connection(db='WEEL'):
    return pymysql.connect(
        host=os.getenv("host"),
        user=os.getenv("db_user"),
        password=os.getenv("password"),
        db=db,
    )
