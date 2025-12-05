"""
Запуск видео-воркера
Запускайте в отдельном терминале: python run_worker.py
"""

import sys
import os


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ml_integration.video_worker import VideoWorker
    print("✅ ML модули загружены успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("\nРешение: Создайте структуру:")
    print("  ml_integration/")
    print("  ├── __init__.py")
    print("  ├── ml_service.py")
    print("  └── video_worker.py")
    sys.exit(1)

def main():
    print("=" * 50)
    print("ЗАПУСК СИСТЕМЫ ML ОБРАБОТКИ ВИДЕО")
    print("=" * 50)
    

    if not os.path.exists("database.db"):
        print("База данных database.db не найдена!")
        print("   Сначала запустите Flask сервер (python app.py)")
        print("   и загрузите хотя бы одно видео через сайт")
        response = input("\nВсё равно запустить воркер? (y/n): ")
        if response.lower() != 'y':
            print("Завершение работы...")
            return
    

    worker = VideoWorker(db_path="database.db")
    
    try:
        worker.run_continuous(interval=10)
    except KeyboardInterrupt:
        print("\nВоркер завершил работу")

if __name__ == "__main__":
    main()
