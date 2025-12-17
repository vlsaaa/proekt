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
            showMessage(` ${data.message} | ${data.server_status} (${data.timestamp})`, 'blue');
            
        } catch (error) {
            showMessage('❌ Ошибка соединения с сервером', 'red');
            console.error('Ошибка:', error);
        }
    });
    
    // Проверяем статус авторизации при загрузке страницы
    checkAuthStatus();
});
