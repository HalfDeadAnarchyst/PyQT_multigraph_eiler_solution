import sqlite3
from PyQt5.QtSql import (QSqlDatabase, QSqlQuery, QSqlTableModel,
                         QSqlRelationalTableModel, QSqlRelation)


def sql_put_and_get_row_id(sql_command):
    con = sqlite3.connect('sql_db.db')
    cur = con.cursor()
    cur.execute(sql_command)
    output = cur.lastrowid
    con.commit()
    con.close()
    return output


def sql_set(sql_command):
    sql_put(sql_command)  # To avoid some errors


def sql_put(sql_command):
    con = sqlite3.connect('sql_db.db')
    cur = con.cursor()
    cur.execute(sql_command)
    con.commit()
    con.close()


def sql_get(sql_command):
    con = sqlite3.connect('sql_db.db')
    cur = con.cursor()
    cur.execute(sql_command)
    output = cur.fetchone()
    con.close()
    return output


def sql_get_all(sql_command):
    con = sqlite3.connect('sql_db.db')
    cur = con.cursor()
    cur.execute(sql_command)
    output = cur.fetchall()
    con.close()
    return output


def sql_get_all_cities_in_district(district):
    return sql_get_all(f'SELECT * FROM `cities` WHERE district = "{district}";')


def sql_get_all_districts(region):
    temp = sql_get_all(f'SELECT DISTINCT district FROM `cities` WHERE region = "{region}";')
    result = ["Выберите район"]
    for elem in temp:
        result.append(elem[0])
    # print(result)
    return result


def sql_get_city_enabled_status(city):
    return sql_get(f'SELECT enabled FROM `cities` WHERE name = "{city}";')[0]


def sql_get_all_regions():
    temp = sql_get_all(f'SELECT DISTINCT region FROM `cities`;')
    result = ['Выберите регион']
    for elem in temp:
        result.append(elem[0])
    return result


def sql_set_city_enable_status(city):
    sql_set(f'UPDATE `cities` SET enabled = "True" WHERE name = "{city}";')


def sql_set_city_disable_status(city):
    sql_set(f'UPDATE `cities` SET enabled = "False" WHERE name = "{city}";')


def sql_get_all_enabled_cities(district):
    return sql_get_all(f'SELECT * FROM `cities` WHERE enabled = "True" AND district = "{district}";')


def sql_get_helis_names():
    temp = sql_get_all(f'SELECT name FROM `helicopters`;')
    result = ['Выберите вертолёт']
    for elem in temp:
        result.append(elem[0])
    return result


def sql_get_cur_heli(heli):
    return sql_get_all(f'SELECT * FROM `helicopters` WHERE name = "{heli}";')


def sql_get_helis_all():
    return sql_get_all(f'SELECT * FROM `helicopters`;')


# DATABASE #############################################################################################################

def sql_get_columns(table):
    return sql_get_all(f"PRAGMA table_info(`{table}`);")


def sql_update_data(table, column, data, name):
    query = f'UPDATE `{table}` SET "{column}" = "{data}" WHERE name = "{name}";'
    print(query)
    sql_put(f'UPDATE `{table}` SET "{column}" = "{data}" WHERE name = "{name}";')


def sql_get_previous_data(table, column, name):
    return sql_get(f'SELECT "{column}" FROM `{table}` WHERE name = "{name}";')


def sql_delete_row(table, name):
    sql_set(f'DELETE FROM `{table}` WHERE name = "{name}";')


def sql_cities_add_empty_row():
    sql_set(f'INSERT INTO `cities` (name, lat, lon, region, district, enabled) VALUES ("Город", 0.0, 0.0, "Регион", "Район", True);')


def sql_helicopters_add_empty_row():
    sql_set(f'INSERT INTO `helicopters` (name, picture, cruise_speed, max_distance, mass_empty, mass_full, fuel_consum, time_engine, cost_service, cost_crew, cost_fuel, koef_gsm, koef_diff, c_aeno) VALUES ("Название", "None", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);')