import random
import os
import json
from datetime import datetime

class MLService:
    """
    Сервис для ML‑обработки видео.

    ВАЖНО ДЛЯ ML-ИНЖЕНЕРА:
    - Здесь сейчас стоит ЗАГЛУШКА (random).
    - Тебе нужно заменить random-логику на вызов настоящей модели, но
      СТАРАТЬСЯ СОХРАНИТЬ тот же интерфейс (ключи в возвращаемом dict).

    Минимальный набор полей, который ждёт остальной код:
      success: bool               — удалось ли обработать видео
      entered_count: int          — уникальных людей вошло в кадр
      exited_count: int           — уникальных людей вышло из кадра
      queue_length: int           — уникальных людей в очереди
      queue_threshold: int        — порог очереди, после которого алерт
      threshold_exceeded: bool    — превышен ли порог очереди (важно для фронта!)
      alert_level: str            — 'HIGH' / 'LOW' и т.п.
      alert_message: str          — человекочитаемое сообщение
      recommended_action: str     — что рекомендовано сделать (например, 'open_extra_cashier')
      processing_time: float      — время обработки (секунды)
      processed_at: str           — ISO‑строка времени обработки
      is_mock_data: bool          — можно убрать/ставить False, когда будет реальная модель
      confidence: float           — уверенность модели (0..1)

    Если структура сильно изменится, нужно будет обновить:
      - ml_integration/video_worker.py  (места, где берутся поля из ml_results)
      - app.py (/api/videos/processed)  (формирование ответа API)
    """
    
    def __init__(self):
        """
        ИНИЦИАЛИЗАЦИЯ РЕАЛЬНОЙ МОДЕЛИ (для ML-щика):
        ------------------------------------------
        Здесь удобное место, чтобы:
          - загрузить веса модели (torch.load / tf.keras.models.load_model / onnxruntime и т.п.);
          - инициализировать устройство (CPU / GPU);
          - подготовить любые константы/параметры.

        Пример (псевдокод):

            import torch
            self.model = torch.load("weights.pt", map_location="cpu")
            self.model.eval()

        Сейчас заглушке это не нужно, поэтому метод пустой.
        """
        pass
    
    def process_video(self, video_path):
        """
        Главный метод: принимает путь к видеофайлу и возвращает dict с результатами.

        ТУТ НУЖНО ВСТАВИТЬ РЕАЛЬНЫЙ PIPELINE:
          1. Проверить, что файл существует.
          2. Открыть видео (cv2.VideoCapture / ffmpeg / своя обёртка).
          3. Прогнать кадры через модель, посчитать:
             - entered_count: уникальных людей вошло в кадр
             - exited_count: уникальных людей вышло из кадра
             - queue_length: уникальных людей в очереди
          4. Собрать ответ в виде dict (см. описание в docstring класса).
        """
        print(f"[ML Service] Обрабатываю видео: {video_path}")
        
        if not os.path.exists(video_path):
            return {
                "success": False,
                "error": f"Файл не найден: {video_path}",
                "processed_at": datetime.now().isoformat()
            }
        
        # Генерируем данные: уникальных людей вошло в кадр, вышло из кадра, в очереди
        entered = random.randint(5, 25)
        exited = random.randint(3, 20)
        queue = random.randint(0, 15)
        
        # Порог очереди (можно вынести в конфиг или передавать как параметр)
        THRESHOLD = 5
        
        # Определяем, превышен ли порог (важно для фронта!)
        threshold_exceeded = queue > THRESHOLD
        
        if threshold_exceeded:
            alert_level = "HIGH"
            alert_message = f"ТРЕВОГА! Уникальных людей в очереди: {queue} (порог: {THRESHOLD})"
            action = "open_extra_cashier"
        else:
            alert_level = "LOW"
            alert_message = f"Норма. Уникальных людей в очереди: {queue}"
            action = "none"
        
        return {
            "success": True,
            "entered_count": entered,
            "exited_count": exited,
            "queue_length": queue,
            "queue_threshold": THRESHOLD,
            "threshold_exceeded": threshold_exceeded,  # Важно: фронт будет проверять это поле
            "alert_level": alert_level,
            "alert_message": alert_message,
            "recommended_action": action,
            "processing_time": round(random.uniform(1.5, 4.5), 2),
            "processed_at": datetime.now().isoformat(),
            "is_mock_data": True, 
            "confidence": round(random.uniform(0.85, 0.98), 3)
        }
