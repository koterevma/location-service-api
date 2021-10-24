create_table_query = (
    "CREATE TABLE loc ("
    "  date DATETIME, "
    "  latitude DECIMAL(10, 8), "
    "  longitude DECIMAL(10, 8))"
)

add_data_query = (
    "INSERT INTO loc "
    "(date, latitude, longitude) "
    "VALUES (%(date)s, %(latitude)s, %(longitude)s)"
)

get_all_data_query = (
    "SELECT * FROM loc ORDER BY date ASC"
)

get_period_data_query = (
    "SELECT * FROM loc "
    "WHERE date BETWEEN %s AND %s "
    "ORDER BY date ASC"
)

