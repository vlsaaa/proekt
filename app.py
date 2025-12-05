from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
os.system('chcp 65001')
import db
import sys
import io
import uuid
from db import get_db

from werkzeug.utils import secure_filename

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

# Создаем Flask приложение
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

db.init_app(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB limit
app.config['DATABASE'] = 'database.db'

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
    """Сохраняем метаданные видео в базу данных"""
    print(f"Saving metadata: {data}")
    
    try:
        database = db.get_db()
        database.execute(
            'INSERT INTO videos (title, description, filename, file_path, file_size, upload_date, user_id)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?)',
            (data.get('title'), data.get('description'), data.get('filename'), data.get('file_path'),
             data.get('file_size'), datetime.now(), 1)  # временно используем user_id = 1
        )
        database.commit()
        print("Метаданные видео сохранены в базу данных")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении в базу данных: {e}")
        return False

def save_video(file, user_email=None, title=None, description=None):
    """Сохраняем видео файл и его метаданные"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        try:
            # Сохраняем файл
            file.save(file_path)
            
            # Получаем размер файла
            file_size = os.path.getsize(file_path)
            
            # Используем переданное название или имя файла
            video_title = title if title else filename.rsplit('.', 1)[0]
            
            # Сохраняем метаданные
            save_video_metadata(
                title=video_title,
                description=description,
                filename=unique_filename,
                file_path=file_path,
                file_size=file_size,
                user_email=user_email
            )
            
            return {
                'success': True,
                'filename': unique_filename,
                'title': video_title,
                'size': file_size,
                'path': file_path
            }
            
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return {'success': False, 'error': str(e)}
    
    return {'success': False, 'error': 'Недопустимый файл'}

# Обработка кнопки "Загрузить видео"
@app.route('/upload', methods=['POST'])
def upload_video():
    # Обработка загрузки файла
    if 'video' in request.files:
        file = request.files['video']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'Файл не выбран'
            }), 400
        
        # Получаем дополнительные данные
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        user_email = request.form.get('user_email', 'Неизвестный пользователь')
        
        # Сохраняем видео
        result = save_video(file, user_email, title, description)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f'Видео "{result["title"]}" успешно загружено пользователем {user_email}!',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'filename': result['filename'],
                'title': result['title'],
                'size': result['size'],
                'user': user_email
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Ошибка загрузки: {result.get("error", "Неизвестная ошибка")}',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }), 400
    
    # Обработка JSON запроса (старый функционал)
    if request.is_json:
        data = request.get_json()
        user_email = data.get('user', 'Неизвестный пользователь')
        print(f"Пользователь {user_email} нажал кнопку Загрузить видео!")
        
        return jsonify({
            'success': True,
            'message': f'Сервер получил запрос на загрузку видео от {user_email}!',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user': user_email,
            'note': 'Для загрузки файлов используйте форму'
        })
    
    return jsonify({
        'success': False,
        'message': 'Не удалось обработать запрос на загрузку видео',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), 400

# Обработка кнопки "Вывод информации"
@app.route('/info', methods=['POST'])
def get_info():
    data = request.get_json()
    user_email = data.get('user', 'Неизвестный пользователь')
    
    print(f"Пользователь {user_email} нажал кнопку Вывод информации!")
    
    # Получаем информацию о загруженных видео из базы данных
    video_count = 0
    total_size = 0
    try:
        database = db.get_db()
        # Получаем количество видео
        video_count = database.execute('SELECT COUNT(*) FROM videos').fetchone()[0]
        # Получаем общий размер всех видео
        total_size_result = database.execute('SELECT SUM(file_size) FROM videos').fetchone()[0]
        total_size = total_size_result if total_size_result else 0
    except Exception as e:
        print(f"Ошибка при получении информации из базы данных: {e}")
    
    #Отправляем ответ обратно
    return jsonify({
        'success': True,
        'message': f'Сервер получил запрос на вывод информации от {user_email}!',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'server_status': 'Flask работает отлично!',
        'user': user_email,
        'video_count': video_count,
        'total_size_mb': round(total_size / (1024 * 1024), 2) if total_size else 0,
        'system_info': {
            'upload_folder': UPLOAD_FOLDER,
            'max_file_size': '500MB',
            'allowed_formats': list(ALLOWED_EXTENSIONS)
        }
    })

# Новый endpoint для получения списка видео
@app.route('/videos', methods=['GET'])
def get_videos():
    try:
        database = db.get_db()
        videos = database.execute(
            'SELECT title, description, filename, file_size, upload_date FROM videos ORDER BY upload_date DESC'
        ).fetchall()
        
        video_list = []
        for video in videos:
            video_list.append({
                'title': video['title'],
                'description': video['description'],
                'filename': video['filename'],
                'file_size': video['file_size'],
                'upload_date': video['upload_date']
            })
        
        return jsonify({
            'success': True,
            'videos': video_list,
            'count': len(video_list)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Endpoint для проверки авторизации
@app.route('/auth/status', methods=['POST'])
def auth_status():
    data = request.get_json()
    user_email = data.get('email')
    
    if user_email:
        return jsonify({
            'success': True,
            'authenticated': True,
            'user': user_email,
            'message': f'Пользователь {user_email} авторизован'
        })
    else:
        return jsonify({
            'success': False,
            'authenticated': False,
            'message': 'Пользователь не авторизован'
        })

@app.route('/api/videos/processed')
def get_processed_videos():
    """Получить список обработанных видео"""
    try:
        db = get_db()
        
        # Ищем обработанные видео
        videos = db.execute("""
            SELECT id, title, filename, 
                   people_entered, people_exited, queue_length,
                   alert_message, processed_at
            FROM videos 
            WHERE status = 'processed'
            ORDER BY processed_at DESC
            LIMIT 50
        """).fetchall()
        
        result = []
        for video in videos:
            result.append({
                'id': video['id'],
                'title': video['title'],
                'filename': video['filename'],
                'stats': {
                    'entered': video['people_entered'],
                    'exited': video['people_exited'],
                    'inside': video['people_entered'] - video['people_exited'],
                    'queue': video['queue_length']
                },
                'alert': video['alert_message'],
                'processed_at': video['processed_at']
            })
        
        return jsonify({
            'success': True,
            'videos': result,
            'count': len(result),
            'message': 'Список обработанных видео'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/processing/status')
def get_processing_status():
    """Получить статус обработки видео"""
    return jsonify({
        'success': True,
        'ml_integration': True,
        'endpoints': {
            'processed_videos': '/api/videos/processed',
            'processing_status': '/api/processing/status'
        },
        'instructions': {
            'start_worker': 'python run_worker.py',
            'check_results': 'GET /api/videos/processed'
        },
        'note': 'ML воркер работает в отдельном терминале'
    })

# Запускаем сервер
if __name__ == '__main__':
    print("=== Запускаем Flask сервер ===")
    print("Сайт будет доступен по адресу: http://localhost:5000")
    print("Для остановки сервера нажмите Ctrl+C")
    print("Функционал авторизации активен")
    print("База данных подключена")
    print("Функционал загрузки видео активен")
    app.run(debug=True)