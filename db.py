from datetime import datetime
from mysql.connector import errorcode
from typing import Tuple, List, Dict, Optional, Any
from queries import add_data_query, create_table_query, get_all_data_query
import mysql.connector
import os
import json


class Error(Exception):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class AccessError(Error):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class BadDBError(Error):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class EnvVarsUnset(Error):
    def __init__(self, message: str) -> None:
        super().__init__(message)


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
            if config.get('user') is None or config.get('password') is None:
                raise AccessError('USER or PASSWORD variables are unset, try to set env vars')

            raise AccessError('Password or login are incorrect')

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise BadDBError(f"Database \"{config.get('database')}\" does not exist")

        else:
            raise

    else:
        return conn


def _get_data(query: Tuple[str]) -> List[Dict[str, str]]:
    conn_config = _get_config()
    try:
        conn = _connect_to_database(conn_config)
    except Exception as e:
        raise ConnectionError("Could not connect to database. " + str(e))

    with conn.cursor() as cursor:
        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            raise ValueError("Could not get data. " + str(err))
        else:
            rez = []
            for date, latitude, longitude in cursor:
                rez.append(
                    dict(
                        date=str(date),
                        latitude=str(latitude),
                        longitude=str(longitude)
                    )
                )

            return rez

    conn.close()


def get_all_data() -> Dict[str, str]:
    return _get_data(get_all_data_query)


def insert(data: Dict[str, Any]) -> None:
    conn_config = _get_config()
    try:
        conn = _connect_to_database(conn_config)
    except Exception as e:
        raise ConnectionError("Could not connect to database. " + str(e))

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

