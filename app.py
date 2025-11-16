from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import sys
import io
import uuid
from werkzeug.utils import secure_filename
from ml_client import ml_client  # Импортируем ML клиент
import db

os.system('chcp 65001')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

app = Flask(__name__)
db.init_app(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB limit

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    try:
        # Проверяем, есть ли файл в запросе
        if 'video' not in request.files:
            return jsonify({
                'success': False,
                'message': 'Файл не найден в запросе',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'Файл не выбран',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }), 400
        
        if file and allowed_file(file.filename):
            # Сохраняем файл
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            
            print(f"✅ Видео сохранено: {unique_filename}")
            
            # ОТПРАВЛЯЕМ В ML МИКРОСЕРВИС
            ml_response = ml_client.process_video(file)
            
            if ml_response['success']:
                return jsonify({
                    'success': True,
                    'message': 'Видео успешно обработано ML!',
                    'ml_result': ml_response['ml_result'],
                    'filename': unique_filename,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Видео сохранено, но ML сервис недоступен',
                    'error': ml_response['error'],
                    'filename': unique_filename,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
        else:
            return jsonify({
                'success': False,
                'message': 'Недопустимый формат файла',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }), 400
            
    except Exception as e:
        print(f"❌ Ошибка при загрузке: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Ошибка сервера: {str(e)}',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/info', methods=['POST'])
def get_info():
    try:
        # ПРОВЕРЯЕМ СТАТУС ML СЕРВИСА
        ml_status = ml_client.get_ml_info()
        
        server_info = {
            'flask_status': '✅ Flask сервер работает',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ml_service': ml_status
        }
        
        return jsonify({
            'success': True,
            'message': 'Информация о системе',
            'server_status': server_info['flask_status'],
            'ml_status': ml_status['ml_status'],
            'details': ml_status['details'],
            'timestamp': server_info['timestamp']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка при получении информации: {str(e)}',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

# Новый endpoint для проверки здоровья
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'main_flask_server',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=== Запускаем основной Flask сервер ===")
    print("Сайт будет доступен по адресу: http://localhost:5000")
    print("Ожидается ML сервис на: http://localhost:8000")
    print("Для остановки сервера нажмите Ctrl+C")
    app.run(debug=True, host='0.0.0.0', port=5000)