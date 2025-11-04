from flask import Flask, render_template, request, jsonify #, flash, redirect, url_for
from datetime import datetime
import os
os.system('chcp 65001')
import db
import sys
import io
import uuid
from werkzeug.utils import secure_filename

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

# Создаем Flask приложение
app = Flask(__name__)

db.init_app(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB limit

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Проверка расширения файла
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Главная страница
@app.route('/')
def home():
    return render_template('index.html')

def save_video_metadata(**data):
    # Save to database - implement your DB logic here
    print(f"Saving metadata: {data}")

def save_video(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add unique identifier to avoid name conflicts
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        file.save(file_path)
        
        # Save metadata to database
        save_video_metadata(
            title=filename,
            filename=unique_filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path)
        )
        return unique_filename

# Обработка кнопки "Загрузить видео"
@app.route('/upload', methods=['POST'])
def upload_video():
    # Получаем данные из запроса
    data = request.get_json()
    print("Кто-то нажал кнопку Загрузить видео!")
    
    if 'video' not in request.files:
        return jsonify({'error': 'No video file'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    save_video(file)

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
    
    #Отправляем ответ обратно
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
