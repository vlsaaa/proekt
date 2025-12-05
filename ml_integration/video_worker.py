import time
import sqlite3
import json
from datetime import datetime

from .ml_service import MLService

class VideoWorker:
    """Воркер для обработки видео через ML"""
    
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.ml_service = MLService()
        self.running = True
        print("Видео-воркер инициализирован")
    
    def get_db_connection(self):
        """Подключение к базе данных"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_unprocessed_videos(self):
        """Получить видео для обработки"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, file_path, filename, title 
            FROM videos 
            WHERE status IS NULL OR status = 'uploaded' OR status = ''
            ORDER BY upload_date ASC
            LIMIT 2
        """)
        
        videos = cursor.fetchall()
        conn.close()
        
        return videos
    
    def update_video_status(self, video_id, status, ml_results=None):
        """Обновить статус видео в БД"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        if status == "processing":
            cursor.execute("""
                UPDATE videos 
                SET status = 'processing'
                WHERE id = ?
            """, (video_id,))
        
        elif status == "processed" and ml_results:
            entered = ml_results['entered_count'] if isinstance(ml_results, dict) else 0
            exited = ml_results['exited_count'] if isinstance(ml_results, dict) else 0
            queue = ml_results['queue_length'] if isinstance(ml_results, dict) else 0
            alert_level = ml_results['alert_level'] if isinstance(ml_results, dict) else 'LOW'
            alert_message = ml_results['alert_message'] if isinstance(ml_results, dict) else ''
            
            cursor.execute("""
                UPDATE videos 
                SET status = 'processed',
                    processed_at = ?,
                    people_entered = ?,
                    people_exited = ?,
                    queue_length = ?,
                    alert_level = ?,
                    alert_message = ?,
                    ml_results = ?
                WHERE id = ?
            """, (
                datetime.now(),
                entered,
                exited,
                queue,
                alert_level,
                alert_message,
                json.dumps(ml_results, ensure_ascii=False) if ml_results else '{}',
                video_id
            ))
        
        elif status == "failed":
            cursor.execute("""
                UPDATE videos 
                SET status = 'failed'
                WHERE id = ?
            """, (video_id,))
        
        conn.commit()
        conn.close()
    
    def process_video(self, video):
        """Обработать одно видео"""
        video_id = video['id']
        video_path = video['file_path']
        filename = video['filename']
        title = video['title'] if 'title' in video.keys() and video['title'] else filename
        
        print(f"\n🎬 Обрабатываю видео #{video_id}: {title}")
        print(f"   📁 Файл: {filename}")
        
        try:
            self.update_video_status(video_id, "processing")
            
            print(f"   🤖 Отправляю в ML сервис...")
            ml_results = self.ml_service.process_video(video_path)
            
            # Проверяем тип ml_results
            if not isinstance(ml_results, dict):
                print(f"ML сервис вернул не словарь: {type(ml_results)}")
                self.update_video_status(video_id, "failed")
                return False
            
            if not ml_results.get('success', True):
                print(f"ML ошибка: {ml_results.get('error', 'Unknown error')}")
                self.update_video_status(video_id, "failed")
                return False
            
            print(f"   💾 Сохраняю результаты в БД...")
            self.update_video_status(video_id, "processed", ml_results)
            
            print(f"ГОТОВО!")
            print(f"   📊 Результаты:")
            print(f"Вошло: {ml_results.get('entered_count', 0)} человек")
            print(f"Вышло: {ml_results.get('exited_count', 0)} человек")
            print(f"Внутри: {ml_results.get('current_inside', 0)} человек")
            print(f"Очередь: {ml_results.get('queue_length', 0)} человек")
            print(f"      ⚠️  Алерт: {ml_results.get('alert_message', '')}")
            
            return True
            
        except Exception as e:
            print(f"ОШИБКА: {e}")
            self.update_video_status(video_id, "failed")
            return False
    
    def run_once(self):
        """Выполнить одну итерацию проверки"""
        videos = self.get_unprocessed_videos()
        
        if videos:
            print(f"\nНайдено {len(videos)} видео для обработки")
            for video in videos:
                self.process_video(video)
            return True
        else:
            return False
    
    def run_continuous(self, interval=10):
        """Запустить непрерывную работу"""
        print("\n" + "="*50)
        print("ЗАПУСКАЮ ВИДЕО-ВОРКЕР")
        print("="*50)
        print("Воркер будет проверять новые видео каждые 10 секунд")
        print("Для остановки нажмите Ctrl+C")
        print("="*50)
        
        processed_count = 0
        
        try:
            while self.running:
                if self.run_once():
                    processed_count += 1
                
                print(f"\n⏳ Следующая проверка через {interval} секунд...")
                
                for i in range(interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print(f"\nВоркер остановлен. Обработано видео: {processed_count}")
            self.running = False
            
        except Exception as e:
            print(f"\nОшибка в воркере: {e}")
            import traceback
            traceback.print_exc()  # ← Покажет полную трассировку ошибки
            print("🔄 Перезапуск через 30 секунд...")
            time.sleep(30)
            self.run_continuous(interval)
