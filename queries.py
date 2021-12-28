'''SQL queries'''

# Создание базы данных с полями хранящими широту, долготу и время
create_table_query = (
    "CREATE TABLE loc ("
    "  date DATETIME, "
    "  latitude DECIMAL(10, 6), "
    "  longitude DECIMAL(10, 6))"
)

# Добавление данных
add_data_query = (
    "INSERT INTO loc "
    "(date, latitude, longitude) "
    "VALUES (%(date)s, %(latitude)s, %(longitude)s)"
)

# Получить все данные
get_all_data_query = (
    "SELECT * FROM loc ORDER BY date ASC"
)

# Получить данные за период
get_period_data_query = (
    "SELECT * FROM loc "
    "WHERE date BETWEEN %s AND %s "
    "ORDER BY date ASC"
)

# Получение последних N данных
get_last_data_query = (
    "SELECT * FROM loc "
    "ORDER BY DATE DESC "
    "LIMIT %s"
)

