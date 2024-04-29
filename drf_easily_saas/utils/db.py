from django.db import connection
from typing import List, Union

# Exceptions
from drf_easily_saas.exceptions.base import DatabaseError

def check_table_exists(table_name: str) -> bool:
    with connection.cursor() as cursor:
        try:
            table_names = connection.introspection.table_names()
            if table_name in table_names:
                return True
        except Exception as e:
            raise DatabaseError(f"Error checking if table {table_name} exists: {str(e)}")
    return False


def count_tables() -> Union[int, None]:
    with connection.cursor() as cursor:
        try:
            table_names = connection.introspection.table_names()
            return len(table_names)
        except Exception as e:
            raise DatabaseError(f"Error counting tables: {str(e)}")
        return None
    

def check_table_empty(table_name: str) -> bool:
    with connection.cursor() as cursor:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            if count > 0:
                return False
        except Exception as e:
            raise DatabaseError(f"Error checking if table {table_name} is empty: {str(e)}")
    return True