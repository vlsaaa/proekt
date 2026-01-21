// Ждем пока вся страница загрузится
document.addEventListener('DOMContentLoaded', function() {
    // Находим элементы на странице
    const uploadBtn = document.getElementById('uploadBtn');
    const infoBtn = document.getElementById('infoBtn');
    const messageElement = document.getElementById('message');
    
    // Элементы для авторизации
    const authBtn = document.getElementById('authBtn');
    const authModal = document.getElementById('authModal');
    const closeModal = document.getElementById('closeModal');
    const authForm = document.getElementById('authForm');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const submitAuth = document.getElementById('submitAuth');
    
    // Модальное окно для загрузки видео
    const uploadModal = document.createElement('div');
    uploadModal.className = 'modal-overlay';
    uploadModal.id = 'uploadModal';
    uploadModal.style.display = 'none';
    
    uploadModal.innerHTML = `
        <div class="modal-content">
            <button class="modal-close upload-close">×</button>
            <h2 class="modal-title">Загрузить видео</h2>
            
            <form id="uploadForm">
                <div class="form-group">
                    <label for="videoTitle">Название видео:</label>
                    <input type="text" id="videoTitle" name="videoTitle" 
                           placeholder="Введите название видео" required>
                </div>
                
                <div class="form-group">
                    <label for="videoFile">Выберите видео файл:</label>
                    <input type="file" id="videoFile" name="videoFile" 
                           accept=".mp4,.avi,.mov,.mkv" required>
                    <small style="display: block; margin-top: 5px; color: #666;">
                        Поддерживаемые форматы: MP4, AVI, MOV, MKV. Максимальный размер: 500MB
                    </small>
                </div>
                
                <div class="form-group">
                    <label for="videoDescription">Описание (необязательно):</label>
                    <textarea id="videoDescription" name="videoDescription" 
                              rows="3" placeholder="Добавьте описание видео"></textarea>
                </div>
                
                <div id="uploadProgress" style="display: none; margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span>Загрузка...</span>
                        <span id="progressPercent">0%</span>
                    </div>
                    <div style="height: 10px; background: #f0f0f0; border-radius: 5px; overflow: hidden;">
                        <div id="progressBar" style="height: 100%; background: #007bff; width: 0%; transition: width 0.3s;"></div>
                    </div>
                </div>
                
                <button type="submit" id="submitUpload" class="submit-btn">
                    📤 Загрузить видео
                </button>
            </form>
        </div>
    `;
    
    document.body.appendChild(uploadModal);
    
    // Переменная для хранения данных пользователя
    let currentUser = null;
    
    // Показываем стартовое сообщение
    messageElement.textContent = 'Готов к работе! Нажмите любую кнопку.';
    messageElement.style.color = '#666';
    
    // Функция для показа сообщений
    function showMessage(text, color) {
        messageElement.textContent = text;
        messageElement.style.color = color;
        messageElement.style.borderColor = color;
    }
    
    // Функция для проверки валидности формы авторизации
    function checkFormValidity() {
        const emailValid = emailInput.value.trim() !== '' && 
                          emailInput.checkValidity();
        const phoneValid = phoneInput.value.trim() !== '' && 
                          phoneInput.checkValidity();
        
        submitAuth.disabled = !(emailValid && phoneValid);
    }
    
    // Функция для входа пользователя
    function loginUser(email, phone) {
        currentUser = {
            email: email,
            phone: phone,
            loginTime: new Date()
        };
        
        authModal.style.display = 'none';
        showMessage(`✅ Успешная авторизация! Добро пожаловать, ${email}`, 'green');
        
        authBtn.textContent = '👤 Выйти';
        authBtn.style.background = 'linear-gradient(45deg, #dc3545, #c82333)';
        authBtn.title = `Войти как: ${email}`;
        
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        console.log(`Пользователь авторизован: Email - ${email}, Телефон - ${phone}`);
    }
    
    // Функция для выхода пользователя
    function logoutUser() {
        if (currentUser) {
            showMessage(`👋 До свидания, ${currentUser.email}!`, 'blue');
        } else {
            showMessage('👋 Вы вышли из системы!', 'blue');
        }
        
        currentUser = null;
        authBtn.textContent = '🔐 Авторизоваться';
        authBtn.style.background = 'linear-gradient(45deg, #28a745, #20c997)';
        authBtn.title = 'Авторизоваться в системе';
        
        localStorage.removeItem('currentUser');
        console.log('Пользователь вышел из системы');
    }
    
    // Функция для проверки авторизации при загрузке страницы
    function checkAuthStatus() {
        const savedUser = localStorage.getItem('currentUser');
        if (savedUser) {
            currentUser = JSON.parse(savedUser);
            authBtn.textContent = '👤 Выйти';
            authBtn.style.background = 'linear-gradient(45deg, #dc3545, #c82333)';
            authBtn.title = `Войти как: ${currentUser.email}`;
            showMessage(`✅ Вы авторизованы как ${currentUser.email}`, 'green');
        }
    }
    
    // Функция для отображения загрузки видео
    function showUploadProgress(percent) {
        const progressBar = document.getElementById('progressBar');
        const progressPercent = document.getElementById('progressPercent');
        const uploadProgress = document.getElementById('uploadProgress');
        
        uploadProgress.style.display = 'block';
        progressBar.style.width = percent + '%';
        progressPercent.textContent = percent + '%';
    }
    
    // Функция для загрузки видео на сервер
    async function uploadVideo(formData) {
        try {
            showUploadProgress(0);
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Ошибка загрузки');
            }
            
            const data = await response.json();
            
            // Имитация прогресса загрузки
            for (let i = 0; i <= 100; i += 10) {
                setTimeout(() => showUploadProgress(i), i * 10);
            }
            
            setTimeout(() => {
                showMessage(`✅ ${data.message}`, 'green');
                uploadModal.style.display = 'none';
                document.getElementById('uploadForm').reset();
                document.getElementById('uploadProgress').style.display = 'none';
            }, 1000);
            
            return data;
            
        } catch (error) {
            showMessage(`❌ Ошибка загрузки: ${error.message}`, 'red');
            console.error('Ошибка загрузки:', error);
            document.getElementById('uploadProgress').style.display = 'none';
            return null;
        }
    }
    
    // Обработчик для кнопки авторизации/выхода
    authBtn.addEventListener('click', function() {
        if (currentUser) {
            logoutUser();
        } else {
            authModal.style.display = 'flex';
            authForm.reset();
            submitAuth.disabled = true;
        }
    });
    
    // Закрытие модального окна авторизации через крестик
    closeModal.addEventListener('click', function() {
        authModal.style.display = 'none';
    });
    
    // Закрытие модального окна загрузки видео
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('upload-close')) {
            uploadModal.style.display = 'none';
        }
    });
    
    // Закрытие модальных окон при клике на затемненную область
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal-overlay')) {
            event.target.style.display = 'none';
        }
    });
    
    // Проверка формы авторизации при вводе данных
    emailInput.addEventListener('input', checkFormValidity);
    phoneInput.addEventListener('input', checkFormValidity);
    
    // Обработка отправки формы авторизации
    authForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const email = emailInput.value.trim();
        const phone = phoneInput.value.trim();
        
        showMessage('🔐 Проходим авторизацию...', 'orange');
        
        setTimeout(function() {
            loginUser(email, phone);
        }, 1500);
    });
    
    // Обработчик для кнопки "Загрузить видео"
    uploadBtn.addEventListener('click', function() {
        if (!currentUser) {
            showMessage('❌ Сначала авторизуйтесь!', 'red');
            authModal.style.display = 'flex';
            return;
        }
        
        uploadModal.style.display = 'flex';
        document.getElementById('uploadForm').reset();
        document.getElementById('uploadProgress').style.display = 'none';
    });
    
    // Обработка отправки формы загрузки видео
    document.getElementById('uploadForm').addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const title = document.getElementById('videoTitle').value.trim();
        const fileInput = document.getElementById('videoFile');
        const description = document.getElementById('videoDescription').value.trim();
        
        if (!fileInput.files.length) {
            showMessage('❌ Пожалуйста, выберите видео файл', 'red');
            return;
        }
        
        const file = fileInput.files[0];
        
        // Проверка размера файла (500MB)
        if (file.size > 500 * 1024 * 1024) {
            showMessage('❌ Файл слишком большой. Максимальный размер: 500MB', 'red');
            return;
        }
        
        showMessage('📹 Начинаем загрузку видео...', 'orange');
        
        const formData = new FormData();
        formData.append('video', file);
        formData.append('title', title);
        formData.append('description', description);
        formData.append('user_email', currentUser.email);
        
        await uploadVideo(formData);
    });
    
    // Обработчик для кнопки "Вывод информации"
    infoBtn.addEventListener('click', async function() {
        if (!currentUser) {
            showMessage('❌ Сначала авторизуйтесь!', 'red');
            authModal.style.display = 'flex';
            return;
        }
        
        showMessage('⌛ Запрашиваем информацию...', 'orange');
        
        try {
            const response = await fetch('/info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    action: 'getInfo',
                    button: 'infoBtn',
                    user: currentUser.email
                })
            });
            
            const data = await response.json();
            
            showMlResults();
            
            showMessage(`✅ ${data.message} | Обработано видео: ${data.video_count || 0}`, 'green');
            
        } catch (error) {
            showMessage('❌ Ошибка соединения с сервером', 'red');
            console.error('Ошибка:', error);
        }
    });
    
    // Проверяем статус авторизации при загрузке страницы
    checkAuthStatus();
    initMlModal();
});
// Глобальные переменные для ML
let mlProcessedVideos = [];

// Показать ML результаты
function showMlResults() {
    document.getElementById('mlResultsModal').style.display = 'flex';
    loadMlStats();
    loadMlStatus();
}

// Закрыть ML модальное окно
function closeMlResults() {
    document.getElementById('mlResultsModal').style.display = 'none';
}

// Переключение вкладок
function switchMlTab(tabName) {
    // Убираем активный класс у всех вкладок
    document.querySelectorAll('.ml-tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelectorAll('.ml-tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Активируем выбранную вкладку
    const tabId = `ml${tabName.charAt(0).toUpperCase() + tabName.slice(1)}Tab`;
    const contentId = `ml${tabName.charAt(0).toUpperCase() + tabName.slice(1)}Content`;
    
    document.getElementById(tabId).classList.add('active');
    document.getElementById(contentId).classList.add('active');
    
    // Загружаем данные если нужно
    if (tabName === 'stats') {
        loadMlStats();
    } else if (tabName === 'videos') {
        loadMlVideos();
    } else if (tabName === 'status') {
        loadMlStatus();
    }
}

// Загрузка статистики ML
async function loadMlStats() {
    try {
        const response = await fetch('/api/videos/processed');
        const data = await response.json();
        
        if (!data.success) {
            document.getElementById('mlStatsGrid').innerHTML = `
                <div class="ml-stat-card">
                    <div class="ml-stat-label">Ошибка загрузки</div>
                    <div class="ml-stat-value">⚠️</div>
                </div>
            `;
            return;
        }
        
        mlProcessedVideos = data.videos || [];
        const totalVideos = mlProcessedVideos.length;
        const highAlerts = mlProcessedVideos.filter(v => 
            v.stats.threshold_exceeded || v.stats.alert_level === 'HIGH'
        ).length;
        const totalQueue = mlProcessedVideos.reduce((sum, v) => sum + (v.stats.queue || 0), 0);
        const avgQueue = totalVideos > 0 ? Math.round(totalQueue / totalVideos) : 0;
        const maxQueue = Math.max(...mlProcessedVideos.map(v => v.stats.queue || 0), 0);
        
        document.getElementById('mlStatsGrid').innerHTML = `
            <div class="ml-stat-card">
                <div class="ml-stat-label">Обработано видео</div>
                <div class="ml-stat-value">${totalVideos}</div>
                <div style="color: #888; font-size: 12px;">системой компьютерного зрения</div>
            </div>
            <div class="ml-stat-card ${highAlerts > 0 ? 'alert' : 'success'}">
                <div class="ml-stat-label">Обнаружено инцидентов</div>
                <div class="ml-stat-value">${highAlerts}</div>
                <div style="color: #888; font-size: 12px;">превышение порога очереди</div>
            </div>
            <div class="ml-stat-card">
                <div class="ml-stat-label">Средняя очередь</div>
                <div class="ml-stat-value">${avgQueue}</div>
                <div style="color: #888; font-size: 12px;">уникальных людей</div>
            </div>
            <div class="ml-stat-card warning">
                <div class="ml-stat-label">Максимальная очередь</div>
                <div class="ml-stat-value">${maxQueue}</div>
                <div style="color: #888; font-size: 12px;">человек в кадре</div>
            </div>
        `;
    } catch (error) {
        console.error('Ошибка загрузки ML статистики:', error);
        document.getElementById('mlStatsGrid').innerHTML = `
            <div class="ml-stat-card">
                <div class="ml-stat-label">Ошибка соединения</div>
                <div class="ml-stat-value">❌</div>
                <div style="color: #888; font-size: 12px;">с сервером анализа</div>
            </div>
        `;
    }
}

// Загрузка видео ML
async function loadMlVideos() {
    const container = document.getElementById('mlVideosContainer');
    
    if (mlProcessedVideos.length === 0) {
        try {
            const response = await fetch('/api/videos/processed');
            const data = await response.json();
            mlProcessedVideos = data.videos || [];
        } catch (error) {
            console.error('Ошибка загрузки видео:', error);
        }
    }
    
    if (mlProcessedVideos.length === 0) {
        container.innerHTML = `
            <div class="ml-no-data">
                <p>Нет обработанных видео</p>
                <p style="margin-top: 10px; font-size: 14px;">
                    Видео будут отображаться здесь после обработки системой компьютерного зрения
                </p>
            </div>
        `;
        return;
    }
    
    let tableHTML = `
        <table class="ml-videos-table">
            <thead>
                <tr>
                    <th>Название</th>
                    <th>Дата анализа</th>
                    <th>Очередь</th>
                    <th>Статус</th>
                    <th>Точность</th>
                    <th>Детали</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    mlProcessedVideos.forEach(video => {
        const queueClass = video.stats.threshold_exceeded ? 'ml-queue-high' : 'ml-queue-normal';
        const statusClass = video.stats.threshold_exceeded ? 'ml-status-high' : 'ml-status-low';
        const statusText = video.stats.threshold_exceeded ? 'ВНИМАНИЕ' : 'НОРМА';
        
        // Форматируем дату
        const date = new Date(video.processed_at);
        const formattedDate = date.toLocaleDateString('ru-RU') + ' ' + 
                              date.getHours().toString().padStart(2, '0') + ':' + 
                              date.getMinutes().toString().padStart(2, '0');
        
        // Вычисляем точность
        const confidence = Math.round((video.stats.confidence || 0.85) * 100);
        
        tableHTML += `
            <tr>
                <td><strong>${video.title || video.filename}</strong></td>
                <td>${formattedDate}</td>
                <td>
                    <span class="ml-queue-badge ${queueClass}">
                        ${video.stats.queue || 0} чел.
                    </span>
                </td>
                <td>
                    <span class="ml-status-badge ${statusClass}">
                        ${statusText}
                    </span>
                </td>
                <td>${confidence}%</td>
                <td>
                    <button class="ml-details-btn" onclick="showMlVideoDetails(${video.id})">
                        👁️ Посмотреть
                    </button>
                </td>
            </tr>
        `;
    });
    
    tableHTML += `
            </tbody>
        </table>
    `;
    
    container.innerHTML = tableHTML;
}

// Загрузка статуса ML системы
async function loadMlStatus() {
    try {
        const response = await fetch('/api/processing/status');
        const data = await response.json();
        
        let statusHTML = '';
        
        if (data.success && data.ml_integration) {
            statusHTML = `
                <div class="ml-system-info">
                    <h4 style="margin-top: 0; color: #28a745;">✅ Система компьютерного зрения активна</h4>
                    <p>Система анализа видеопотока работает в штатном режиме.</p>
                    <div style="margin-top: 15px; padding: 15px; background: #e9ecef; border-radius: 5px;">
                        <p style="margin: 0; font-size: 14px;"><strong>Доступные эндпоинты:</strong></p>
                        <ul style="margin: 10px 0 0 0; padding-left: 20px; font-size: 13px;">
                            <li><code>${data.endpoints.processed_videos}</code> - обработанные видео</li>
                            <li><code>${data.endpoints.processing_status}</code> - статус системы</li>
                        </ul>
                    </div>
                </div>
                
                <div class="ml-system-info">
                    <h4 style="margin-top: 0;">📈 Показатели системы</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-top: 10px;">
                        <div style="text-align: center;">
                            <div style="font-size: 24px; font-weight: bold; color: #007bff;">${mlProcessedVideos.length}</div>
                            <div style="font-size: 12px; color: #666;">видео обработано</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 24px; font-weight: bold; color: #28a745;">24/7</div>
                            <div style="font-size: 12px; color: #666;">рабочий режим</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 24px; font-weight: bold; color: #6f42c1;">95%</div>
                            <div style="font-size: 12px; color: #666;">точность распознавания</div>
                        </div>
                    </div>
                </div>
            `;
        } else {
            statusHTML = `
                <div class="ml-system-info">
                    <h4 style="margin-top: 0; color: #dc3545;">⚠️ Система компьютерного зрения неактивна</h4>
                    <p>Для работы системы компьютерного зрения необходимо запустить ML воркер.</p>
                    <div style="margin-top: 15px; padding: 15px; background: #f8d7da; border-radius: 5px;">
                        <p style="margin: 0; font-size: 14px;"><strong>Инструкция по запуску:</strong></p>
                        <ol style="margin: 10px 0 0 0; padding-left: 20px; font-size: 13px;">
                            <li>Откройте новый терминал</li>
                            <li>Выполните команду: <code>${data.instructions?.start_worker || 'python run_worker.py'}</code></li>
                            <li>Дождитесь запуска системы анализа</li>
                        </ol>
                    </div>
                </div>
            `;
        }
        
        document.getElementById('mlStatusInfo').innerHTML = statusHTML;
    } catch (error) {
        console.error('Ошибка загрузки статуса ML:', error);
        document.getElementById('mlStatusInfo').innerHTML = `
            <div class="ml-system-info">
                <h4 style="margin-top: 0; color: #dc3545;">❌ Ошибка соединения</h4>
                <p>Не удалось получить информацию о системе компьютерного зрения.</p>
            </div>
        `;
    }
}

// Показать детали видео
async function showMlVideoDetails(videoId) {
    try {
        const video = mlProcessedVideos.find(v => v.id === videoId);
        if (!video) return;
        
        const modal = document.getElementById('mlDetailsModal');
        const content = document.getElementById('mlDetailsContent');
        
        // Форматируем дату
        const processedDate = new Date(video.processed_at);
        const formattedDate = processedDate.toLocaleString('ru-RU');
        
        // Определяем рекомендации
        let recommendation = 'Действия не требуются';
        let recommendationColor = '#28a745';
        
        if (video.stats.threshold_exceeded) {
            recommendation = 'Рекомендуется открыть дополнительную кассу';
            recommendationColor = '#dc3545';
        } else if (video.stats.queue > 3) {
            recommendation = 'Рекомендуется наблюдение за ситуацией';
            recommendationColor = '#ffc107';
        }
        
        content.innerHTML = `
            <div style="margin-bottom: 20px;">
                <h4 style="margin: 0 0 5px 0;">${video.title || video.filename}</h4>
                <p style="color: #666; margin: 0; font-size: 14px;">Анализ выполнен: ${formattedDate}</p>
            </div>
            
            <div class="ml-detail-item">
                <span class="ml-detail-label">📊 Результаты анализа:</span>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 10px;">
                    <div style="text-align: center; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                        <div style="font-size: 20px; font-weight: bold; color: #007bff;">${video.stats.entered || 0}</div>
                        <div style="font-size: 12px; color: #666;">вошло в кадр</div>
                    </div>
                    <div style="text-align: center; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                        <div style="font-size: 20px; font-weight: bold; color: #6f42c1;">${video.stats.exited || 0}</div>
                        <div style="font-size: 12px; color: #666;">вышло из кадра</div>
                    </div>
                    <div style="text-align: center; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                        <div style="font-size: 20px; font-weight: bold; color: ${video.stats.threshold_exceeded ? '#dc3545' : '#28a745'};">${video.stats.queue || 0}</div>
                        <div style="font-size: 12px; color: #666;">в очереди</div>
                    </div>
                    <div style="text-align: center; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                        <div style="font-size: 20px; font-weight: bold; color: #fd7e14;">${video.stats.queue_threshold || 5}</div>
                        <div style="font-size: 12px; color: #666;">критический порог</div>
                    </div>
                </div>
            </div>
            
            <div class="ml-detail-item">
                <span class="ml-detail-label">🎯 Статус системы:</span>
                <div style="margin-top: 5px; display: flex; align-items: center; gap: 10px;">
                    <span class="ml-status-badge ${video.stats.threshold_exceeded ? 'ml-status-high' : 'ml-status-low'}" 
                          style="font-size: 14px; padding: 5px 15px;">
                        ${video.stats.threshold_exceeded ? '⚠️ ВНИМАНИЕ: Превышен порог очереди' : '✅ НОРМА: Очередь в пределах нормы'}
                    </span>
                    <span style="font-size: 14px; color: #666;">
                        Точность: ${Math.round((video.stats.confidence || 0.85) * 100)}%
                    </span>
                </div>
            </div>
            
            <div class="ml-detail-item">
                <span class="ml-detail-label">💡 Рекомендация системы:</span>
                <div style="margin-top: 5px; padding: 10px; background: ${recommendationColor}15; border-left: 4px solid ${recommendationColor}; border-radius: 4px;">
                    <p style="margin: 0; color: ${recommendationColor}; font-weight: bold;">${recommendation}</p>
                </div>
            </div>
            
            <div class="ml-detail-item" style="border-bottom: none;">
                <span class="ml-detail-label">📝 Аналитическое заключение:</span>
                <div style="margin-top: 5px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
                    <p style="margin: 0; color: #495057; font-size: 14px;">${video.alert || 'Система компьютерного зрения завершила анализ видеопотока. Все показатели в пределах нормы.'}</p>
                </div>
            </div>
            
            <div style="margin-top: 20px; text-align: center;">
                <p style="color: #666; font-size: 12px; margin: 0;">
                    Анализ выполнен системой компьютерного зрения
                </p>
            </div>
        `;
        
        modal.style.display = 'flex';
    } catch (error) {
        console.error('Ошибка показа деталей видео:', error);
    }
}

// Закрыть детали видео
function closeMlDetails() {
    document.getElementById('mlDetailsModal').style.display = 'none';
}

// Инициализация ML модального окна
function initMlModal() {
    // Закрытие по клику на крестик
    document.getElementById('closeMlModal').addEventListener('click', closeMlResults);
    
    // Закрытие по клику на затемненную область
    document.getElementById('mlResultsModal').addEventListener('click', function(event) {
        if (event.target === this) {
            closeMlResults();
        }
    });
    
    // Закрытие деталей по клику на затемненную область
    document.getElementById('mlDetailsModal').addEventListener('click', function(event) {
        if (event.target === this) {
            closeMlDetails();
        }
    });
}