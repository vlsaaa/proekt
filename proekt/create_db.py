import sqlite3
import os
import argparse


def parse_args():
    """Парсер аргументов для создания БД.

    По умолчанию поведение остаётся прежним:
    - создаётся/пересоздаётся файл database.db в корне проекта.
    """
    parser = argparse.ArgumentParser(description="Создание базы данных для ML системы")
    parser.add_argument(
        "--db-path",
        default="database.db",
        help="Путь к файлу БД (по умолчанию: database.db)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    db_path = args.db_path

    print("=" * 50)
    print("СОЗДАНИЕ БАЗЫ ДАННЫХ ДЛЯ ML СИСТЕМЫ")
    print("=" * 50)
    print(f"Файл БД: {db_path}")

    # Старое поведение: если файл существует — удаляем и создаём с нуля
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️  Удалён старый {db_path}")

    # Открываем соединение с новой БД
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Создаю таблицы из scheme.sql...")

    # Читаем схему из единого файла scheme.sql,
    # чтобы не было дублирования структуры в коде.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scheme_path = os.path.join(base_dir, "scheme.sql")

    if not os.path.exists(scheme_path):
        conn.close()
        print(f"\nОШИБКА: Не найден файл схемы {scheme_path}")
        return

    with open(scheme_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)
    conn.commit()

    # Диагностика: какие таблицы созданы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\nТаблицы в базе: {[t[0] for t in tables]}")

    # Диагностика структуры videos (если она есть)
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='videos'"
    )
    has_videos = cursor.fetchone() is not None

    if has_videos:
        cursor.execute("PRAGMA table_info(videos)")
        columns = cursor.fetchall()
        print(f"\nСтруктура таблицы 'videos':")
        print("   Всего колонок:", len(columns))
        for col in columns:
            print(f"   • {col[1]} ({col[2]})")
    else:
        print("\nВНИМАНИЕ: Таблица 'videos' не найдена в созданной БД.")

    conn.close()

    size = os.path.getsize(db_path)
    print(f"\n📏 Размер файла: {size} байт")

    if size > 0:
        print("\n" + "=" * 50)
        print("БАЗА ДАННЫХ УСПЕШНО СОЗДАНА!")
        print("Теперь можно запускать:")
        print("   1. python app.py          (Flask сервер)")
        print("   2. python run_worker.py   (ML воркер)")
        print("=" * 50)
    else:
        print("\nОШИБКА: Файл пустой!")


if __name__ == "__main__":
    main()
