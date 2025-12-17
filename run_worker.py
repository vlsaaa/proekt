"""
Запуск видео-воркера
Запускайте в отдельном терминале: python run_worker.py
"""

import sys
import os
import argparse
import sqlite3

from colorama import Fore, Style, init as colorama_init


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def import_worker():
    try:
        from ml_integration.video_worker import VideoWorker
        print(f"{Fore.GREEN}ML модули загружены успешно{Style.RESET_ALL}")
        return VideoWorker
    except ImportError as e:
        print(f"{Fore.RED}Ошибка импорта: {e}{Style.RESET_ALL}")
        print("\nРешение: Создайте структуру:")
        print("  ml_integration/")
        print("  ├── __init__.py")
        print("  ├── ml_service.py")
        print("  └── video_worker.py")
        sys.exit(1)


def check_database(db_path: str) -> bool:
    """Проверка наличия БД и таблицы videos."""
    if not os.path.exists(db_path):
        print(f"База данных {db_path} не найдена.")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='videos'")
        row = cur.fetchone()
        conn.close()
        if not row:
            print(f"В базе {db_path} нет таблицы 'videos'.")
            return False
    except Exception as e:
        print(f"Ошибка при проверке БД {db_path}: {e}")
        return False

    return True


def parse_args() -> argparse.Namespace:
    """Парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Запуск ML видео-воркера")
    parser.add_argument(
        "--db-path",
        default="database.db",
        help="Путь к файлу базы данных (по умолчанию: database.db)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Интервал проверки новых видео в секундах (по умолчанию: 10)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Не спрашивать подтверждение, даже если БД отсутствует или некорректна",
    )
    return parser.parse_args()


def main():
    # Инициализируем цветной вывод (важно для Windows)
    colorama_init(autoreset=True)

    args = parse_args()

    print("=" * 50)
    print(f"{Fore.CYAN}ЗАПУСК СИСТЕМЫ ML ОБРАБОТКИ ВИДЕО{Style.RESET_ALL}")
    print("=" * 50)
    print(f"Файл БД: {Fore.YELLOW}{args.db_path}{Style.RESET_ALL}")
    print(f"Интервал проверки: {Fore.YELLOW}{args.interval} сек.{Style.RESET_ALL}")

    db_ok = check_database(args.db_path)
    if not db_ok and not args.force:
        print(f"{Fore.RED}   Сначала убедитесь, что создана БД и таблица 'videos'.{Style.RESET_ALL}")
        print("   Возможные варианты:")
        print("     - запустить create_db.py")
        print("     - или инициализировать БД через Flask и scheme.sql")
        response = input(f"\n{Fore.YELLOW}Всё равно запустить воркер? (y/n): {Style.RESET_ALL}")
        if response.lower() != "y":
            print(f"{Fore.MAGENTA}Завершение работы...{Style.RESET_ALL}")
            return

    VideoWorker = import_worker()
    worker = VideoWorker(db_path=args.db_path)

    try:
        worker.run_continuous(interval=args.interval)
    except KeyboardInterrupt:
        print(f"\n{Fore.MAGENTA}Воркер завершил работу{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
