import random
import os
import json
from datetime import datetime

class MLService:
    """Заглушка для ML обработки видео"""
    
    def process_video(self, video_path):
        """
        Имитация работы ML модели.
        Позже заменится на вызов реальной ML от Ани.
        """
        print(f"[ML Service] Обрабатываю видео: {video_path}")
        
        # 1. Проверяем существует ли файл
        if not os.path.exists(video_path):
            return {
                "success": False,
                "error": f"Файл не найден: {video_path}",
                "processed_at": datetime.now().isoformat()
            }
        
        # 2. Генерируем реалистичные тестовые данные
        entered = random.randint(5, 25)
        exited = random.randint(3, 20)
        current = max(0, entered - exited)
        queue = random.randint(0, 15)
        
        # 3. Порог для алерта
        THRESHOLD = 5
        
        # 4. Определяем уровень алерта
        if queue > THRESHOLD:
            alert_level = "HIGH"
            alert_message = f"🚨 ТРЕВОГА! Очередь {queue} человек (порог: {THRESHOLD})"
            action = "open_extra_cashier"
        else:
            alert_level = "LOW"
            alert_message = f"✅ Норма. Очередь {queue} человек"
            action = "none"
        
        # 5. Возвращаем результат
        return {
            "success": True,
            "entered_count": entered,
            "exited_count": exited,
            "current_inside": current,
            "queue_length": queue,
            "queue_threshold": THRESHOLD,
            "threshold_exceeded": queue > THRESHOLD,
            "alert_level": alert_level,
            "alert_message": alert_message,
            "recommended_action": action,
            "processing_time": round(random.uniform(1.5, 4.5), 2),
            "processed_at": datetime.now().isoformat(),
            "is_mock_data": True,  # Флаг что это тестовые данные
            "confidence": round(random.uniform(0.85, 0.98), 3)
        }