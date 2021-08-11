from sqlalchemy import create_engine
import pandas as pd
from mt5monitor_dbv1.db.db_connection import DB_Connection


conn = DB_Connection().get_connection()
ema = {'time': ['2021-07-06 13:00:00', '2021-07-06 13:30:00'],
       'symbol': ['EUR', 'EUR'],
       'ema_short': ['1.46353', '1.46335'],
       'ema_long': ['1.46358', '1.46347'],
       'short_grtr_long': ['False', 'False'],
       'is_crossed': [None, None]
       }
df = pd.DataFrame(ema)

df.to_sql('ema_cross',con=conn,if_exists='replace', index=False)

df1=pd.read_sql_table('ema_cross',con=conn)

# query = 'SELECT * FROM EMA_CROSS where ema_short={}'.format('1.46353')
# print(query)
# df1=pd.read_sql_query(query,con=conn)

print(df1)
conn.close()