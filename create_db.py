# create_db.py - ОБНОВЛЁННАЯ ВЕРСИЯ
import sqlite3
import os

print("="*50)
print("СОЗДАНИЕ БАЗЫ ДАННЫХ ДЛЯ ML СИСТЕМЫ")
print("="*50)

# Удаляем старую БД если есть
if os.path.exists("database.db"):
    os.remove("database.db")
    print("🗑️  Удалён старый database.db")

# Создаём новую базу
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

print("📝 Создаю таблицы...")

# 1. Таблица пользователей
cursor.execute("""
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    phone TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
print("   ✅ Таблица 'user' создана")

# 2. Таблица видео с ВСЕМИ полями для ML
cursor.execute("""
CREATE TABLE videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Основные поля (от Полины)
    title TEXT NOT NULL,
    description TEXT,
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    
    -- ПОЛЯ ДЛЯ ML ОБРАБОТКИ (от тебя)
    status TEXT DEFAULT 'uploaded',      -- uploaded, processing, processed, failed
    processed_at DATETIME,               -- когда обработано ML
    people_entered INTEGER,              -- сколько вошло (от ML)
    people_exited INTEGER,               -- сколько вышло (от ML)
    queue_length INTEGER,                -- длина очереди (от ML)
    alert_level TEXT,                    -- уровень алерта: HIGH, LOW
    alert_message TEXT,                  -- сообщение алерта
    ml_results TEXT,                     -- сырые данные от ML (JSON)
    
    FOREIGN KEY (user_id) REFERENCES user (id)
)
""")
print("   ✅ Таблица 'videos' создана со всеми ML полями")

conn.commit()

# Проверяем что создалось
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"\n📊 Таблицы в базе: {[t[0] for t in tables]}")

# Показываем структуру videos
cursor.execute("PRAGMA table_info(videos)")
columns = cursor.fetchall()
print(f"\n📝 Структура таблицы 'videos':")
print("   Всего колонок:", len(columns))
for col in columns:
    print(f"   • {col[1]} ({col[2]})")

conn.close()

# Проверяем размер
size = os.path.getsize("database.db")
print(f"\n📏 Размер файла: {size} байт")

if size > 0:
    print("\n" + "="*50)
    print("🎉 БАЗА ДАННЫХ УСПЕШНО СОЗДАНА!")
    print("Теперь можно запускать:")
    print("   1. python app.py          (Flask сервер)")
    print("   2. python run_worker.py   (ML воркер)")
    print("="*50)
else:
    print("\n❌ ОШИБКА: Файл пустой!")