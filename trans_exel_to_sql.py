import pandas as pd
import sqlite3

# 1. Подключаемся к базе данных (если файла .db нет, он создастся автоматически)
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# 2. Загружаем Excel-файл в DataFrame pandas
df = pd.read_excel("data.xlsx")  # Укажите правильное имя файла

# 3. Записываем данные в базу (замените 'students' на нужное имя)
df.to_sql("doc_app_student", conn, if_exists="replace", index=False)

# 4. Закрываем соединение
conn.close()

print("Данные успешно загружены в SQLite!")
