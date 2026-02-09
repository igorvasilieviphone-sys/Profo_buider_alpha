import sqlite3
conn = sqlite3.connect('careers.db')
conn.execute('UPDATE careers SET embedding = NULL')
conn.commit()
conn.close()
print("База очищена, теперь можно запускать генерацию заново!")