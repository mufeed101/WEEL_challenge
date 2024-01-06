import pymysql
import os
# Connect to the database

# Read the .sql file
# This Script is copied from my side project
def load_schema(db="WEEL"):
    connection = pymysql.connect(
        host=os.getenv("host"),
        user=os.getenv("db_user"),
        password=os.getenv("password"),
    )

    with open('database/schema.sql', 'r') as file:
        sql_file_contents = file.read().format(db=db)

    sql_commands = sql_file_contents.split(';')

    try:
        with connection.cursor() as cursor:
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
                    connection.commit()
        
        print("SQL commands executed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()


if __name__ == "__main__":
    load_schema()