from mt5monitor_dbv1.db.db_connection import DB_Connection
from MT5Monitor_EMACross_DBv1.mt5monitor_dbv1.db.db_trades_crud import TardesCrud



# d = DB_Connection()

trade_crud = TardesCrud()

trds = trade_crud.selectBySymbolSignalOpenStatus('AUDUSD','SELL',True)

print(trds)
print(len(trds))

if(len(trds)>0):
    for trd in trds:
        print(f"PID: {trd.position_id}")


# import mariadb
# import sys
# import pandas as pd
# import sqlalchemy
#
# # Connect to MariaDB Platform
# try:
#     conn = mariadb.connect(
#         user="root",
#         password="root",
#         host="192.168.8.101",
#         port=3306,
#         database="schema_ema_monitor"
#     )
# except mariadb.Error as e:
#     print(f"Error connecting to MariaDB Platform: {e}")
#     sys.exit(1)
#
# # Get Cursor
# cur = conn.cursor()
#
# try:
#     cur.execute("INSERT INTO employees (first_name, last_name, date_time) values (?,?,?)", ("Maria", "db", '2021-07-06 08:30:00'))
#
#     df.to_sql('ema_cross',conn,index=False)
#     conn.commit()
#     print(f"Last row id: {cur.lastrowid}")
# except mariadb.Error as e:
#     print(f"Error: {e}")
# some_name = "Maria"
# cur.execute("SELECT first_name,last_name, date_time FROM employees WHERE first_name=?", (some_name,))
# # cur.execute("SELECT first_name, last_name from employees")
#
#
# for first_name, last_name, date_time in cur:
#     print(f"First name: {first_name}, Last Name: {last_name}, Date Time: {date_time}")
#
#
# conn.close()