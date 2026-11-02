import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = BASE_DIR / "bot_database.db"

def init_db():
    """Создает таблицу и заполняет её базовыми темами, если базы еще нет"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            title TEXT,
            description TEXT
        )
    """)
    
    default_topics = [
        (
            "data_types", 
            "Типы данных", 
            "Типы данных в C++ включают:\n- int (целые числа)\n- float (числа с плавающей точкой)\n- char (символы)\n- bool (логические значения)\n- string (строки)"
        ),
        (
            "conditional_operators", 
            "Условные операторы", 
            "Условные операторы в C++ включают:\n- if (если)\n- else (иначе)\n- switch (выбор)"
        ),
        (
            "loops", 
            "Циклы", 
            "Циклы в C++ включают:\n- for (для)\n- while (пока)\n- do-while (сделай-пока)"
        ),
        (
            "functions", 
            "Функции", 
            "Функции в C++ позволяют разбивать код на логические блоки:\n- Определение: void myFunction() { ... }\n- Вызов: myFunction();"
        ),
        (
            "pointers", 
            "Указатели", 
            "Указатели — это переменные, хранящие адрес памяти другой переменной:\n- Объявление: int* ptr;\n- Взятие адреса: ptr = &var;"
        )
    ]
    
    cursor.execute("SELECT COUNT(*) FROM topics")
    count = cursor.fetchone()[0]
    
    # Если база пустая — принудительно заполняем
    if count == 0:
        cursor.executemany("INSERT OR IGNORE INTO topics (code, title, description) VALUES (?, ?, ?)", default_topics)
        conn.commit()
        print("База данных была ПУСТОЙ. Успешно добавлено 5 тем!")
    else:
        print(f"База данных уже содержит темы. Количество записей: {count}")
        
    conn.close()

def get_topics_from_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT code, title FROM topics")
    topics = cursor.fetchall()
    conn.close()
    return topics

def get_topic_description(topic_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM topics WHERE code = ?", (topic_code,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Тема не найдена."


        
