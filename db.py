from datetime import datetime
from mysql.connector import errorcode
from typing import Dict, Optional, Any
from queries import add_data_query, create_table_query
import mysql.connector
import os


class Error(Exception):
    pass


class AccessError(Error):
    pass


class BadDBError(Error):
    pass


class EnvVarsUnset(Error):
    message: str
    
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


def _get_config() -> Dict[str, Any]:
    conf = dict(
        host='127.0.0.1',
        raise_on_warnings=True,
        user=os.getenv('USER', 'www'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE', 'location')
    )
    return conf


def _create_table() -> None:
    conn_config = _get_config()
    conn = _connect_to_database(conn_config)
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
        conn.commit()

    conn.close()


def _connect_to_database(config: Dict[str, Any]) -> Optional[mysql.connector.MySQLConnection]:
    try:
        conn = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise AccessError()
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise BadDBError()
        else:
            raise
    else:
        return conn


def insert(data: Dict[str, Any]) -> None:
    conn_config = _get_config()
    # TODO move error texts to _connect_to_database
    try:
        conn = _connect_to_database(conn_config)
    except AccessError:
        if conn_config.get('user') is None or conn_config.get('password') is None:
            raise ConnectionError('USER or PASSWORD variables are unset, try to set env vars')
        raise ConnectionError('Password or login are incorrect')

    except BadDBError:
        raise ConnectionError(f"Database \"{config.get('database')}\" does not exist")

    except mysql.connector.Error as e:
        raise ConnectionError(
            f'Could not get connection to database \"{conn_config.get("database")}\". ' + str(e)
        )

    with conn.cursor() as cursor:
        try:
            cursor.execute(add_data_query, data)
        except mysql.connector.Error as err:
            raise ValueError("Data not added. " + str(err))
        else:
            conn.commit()
            
    conn.close()


if __name__ == '__main__':
    _create_table()

