from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

# Создаем Flask приложение
app = Flask(__name__)

# Главная страница
@app.route('/')
def home():
    return render_template('index.html')

# Обработка кнопки "Загрузить видео"
@app.route('/upload', methods=['POST'])
def upload_video():
    # Получаем данные из запроса
    data = request.get_json()
    print("Кто-то нажал кнопку Загрузить видео!")
    
    # Отправляем ответ обратно
    return jsonify({
        'success': True,
        'message': 'Сервер получил запрос на загрузку видео!',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

# Обработка кнопки "Вывод информации"
@app.route('/info', methods=['POST'])
def get_info():
    data = request.get_json()
    print("Кто-то нажал кнопку Вывод информации!")
    
    return jsonify({
        'success': True,
        'message': 'Сервер получил запрос на вывод информации!',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'server_status': 'Flask работает отлично!'
    })

# Запускаем сервер
if __name__ == '__main__':
    print("=== Запускаем Flask сервер ===")
    print("Сайт будет доступен по адресу: http://localhost:5000")
    print("Для остановки сервера нажмите Ctrl+C")
    app.run(debug=True)