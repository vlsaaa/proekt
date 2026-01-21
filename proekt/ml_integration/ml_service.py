import random
import os
import json
from datetime import datetime

class MLService:
    
    
    def __init__(self):
     
        pass
    
    def process_video(self, video_path):
        
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
