from datetime import datetime, timedelta  # Модули для работы со временем и датой
from mysql.connector import errorcode  # Коды ошибок для отлавливания исключений
from typing import Tuple, List, Dict, Optional, Any  # Подсказки типов
# Подключаем текстовые SQL запросы к базе данных
from queries import (
    add_data_query,
    create_table_query,
    get_all_data_query,
    get_period_data_query,
    get_last_data_query
)
import mysql.connector  # Класс для взаимодействия с базой данных
import os  # Модуль системы. Нужен для получения пароля к базе данных из переменной окружения


'''Базовый класс ошибок нашего приложения'''
class Error(Exception):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


'''Ошибка доступа'''
class AccessError(Error):
    def __init__(self, message: str) -> None:
        super().__init__(message)


'''Ошибка базы данных'''
class BadDBError(Error):
    def __init__(self, message: str) -> None:
        super().__init__(message)


'''Ошибка переменной окружения'''
class EnvVarsUnset(Error):
    def __init__(self, message: str) -> None:
        super().__init__(message)


# Функция, возвращающая статичый конфиг для класса mysql.connector
def _get_config() -> Dict[str, Any]:
    conf = dict(
        host='127.0.0.1',
        raise_on_warnings=True,
        user=os.getenv('USER', 'www'),
        password=os.getenv('PASSWORD'),  # Получаем пороль от базы данных
        database=os.getenv('DATABASE', 'location')  # Имя базы данных, по умолчанию "location"
    )
    return conf


# Функция подключения к базе данных, возвращает класс-коннектор к базе данных
def _connect_to_database(config: Dict[str, Any]) -> mysql.connector.MySQLConnection:
    try:
        conn = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            if config.get('user') is None or config.get('password') is None:
                raise EnvVarsUnset('USER or PASSWORD variables are unset, try to set env vars')

            raise AccessError('Password or login are incorrect')

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise BadDBError(f"Database \"{config.get('database')}\" does not exist")

        else:
            raise

    else:
        return conn


# Запрос в базу данных на создание таблицы
def _create_table() -> None:
    conn_config = _get_config()
    conn = _connect_to_database(conn_config)
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
        conn.commit()

    conn.close()


# Анализ и обработка дат, переданных пользователем
def _parse_dates(from_date: Optional[str], to_date: Optional[str]) -> Tuple[datetime, datetime]:
    if from_date is None:
        from_date = datetime(2021, 9, 1)
    else:
        from_date = datetime.fromisoformat(from_date)

    if to_date is None:
        to_date = datetime.now().replace(microsecond=0) + (
            timedelta(minutes=1))  # Добавляем минуту к поиску, чтобы точно захватить последнее измерение
    else:
        to_date = datetime.fromisoformat(to_date)

    return from_date, to_date


# Функция получения данных по переданному запросу и аргументам
def _get_data(query: Tuple[str], *args) -> List[Dict[str, str]]:
    conn_config = _get_config()
    try:
        conn = _connect_to_database(conn_config)
    except Exception as e:
        raise ConnectionError("Could not connect to database. " + str(e))

    with conn.cursor() as cursor:
        try:
            cursor.execute(query, args)
        except mysql.connector.Error as err:
            conn.close()
            raise ValueError("Could not get data. " + str(err))
        else:
            rez = [dict(date=str(d), latitude=str(la), longitude=str(lo)) for d, la, lo in cursor]

    conn.close()
    return {"result": rez}


# Получить все данные
def get_all_data() -> Dict:
    return _get_data(get_all_data_query)


# Получить данные за определенный период времени
def get_period_data(date_from: Optional[str], date_to: Optional[str]) -> Dict:
    date_from, date_to = map(str, _parse_dates(date_from, date_to))
    return _get_data(get_period_data_query, date_from, date_to)


# Получить последние `count` записей из базы данных
def get_last_data(count: int) -> Dict:
    if count < 1:
        raise ValueError(f"{count=} is not a valid number")

    # Так как мы получаем данные в убывабщем порядке (из-за sql запроса)
    # мы должны развернуть из перед возвратом
    result = _get_data(get_last_data_query, count)
    result["result"].reverse()
    return result


# Вставка данных, представленных в структуре json в базу данных
def insert(data: Dict[str, Any]) -> None:
    conn_config = _get_config()
    try:
        conn = _connect_to_database(conn_config)
    except Exception as e:
        raise ConnectionError("Could not connect to database. " + str(e))

    with conn.cursor() as cursor:
        try:
            if data.get('date') is None:
                data['date'] = datetime.now().replace(microsecond=0)
            cursor.execute(add_data_query, data)
        except mysql.connector.Error as err:
            conn.close()
            raise ValueError("Data not added. " + str(err))
        else:
            conn.commit()

    conn.close()


# Если мы интерпретируем этот файл, мы отправляем в базу
# данных запрос на создание таблицы (сделано для удобства)
if __name__ == '__main__':
    print(_create_table())

