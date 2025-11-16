import requests
import json
from datetime import datetime

class MLClient:
    def __init__(self, ml_service_url="http://localhost:8000"):
        self.ml_service_url = ml_service_url
    
    def process_video(self, video_data):
        """
        Отправляет видео в ML микросервис для обработки
        """
        try:
            # Отправляем запрос к ML сервису
            response = requests.post(
                f"{self.ml_service_url}/process_video",
                files={'video': video_data},
                timeout=30  # Таймаут 30 секунд
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'ml_result': response.json(),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': f"ML service error: {response.status_code}",
                    'timestamp': datetime.now().isoformat()
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Connection to ML service failed: {str(e)}",
                'timestamp': datetime.now().isoformat()
            }
    
    def get_ml_info(self):
        """
        Получает информацию о статусе ML микросервиса
        """
        try:
            response = requests.get(
                f"{self.ml_service_url}/health",
                timeout=5
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'ml_status': 'available',
                    'details': response.json(),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': True,
                    'ml_status': 'unavailable',
                    'details': f"Status: {response.status_code}",
                    'timestamp': datetime.now().isoformat()
                }
                
        except requests.exceptions.RequestException:
            return {
                'success': True,
                'ml_status': 'offline',
                'details': 'ML service is not responding',
                'timestamp': datetime.now().isoformat()
            }

# Создаем глобальный клиент ML
ml_client = MLClient()