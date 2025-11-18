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
    
    // Показываем стартовое сообщение
    messageElement.textContent = 'Готов к работе! Нажмите любую кнопку.';
    messageElement.style.color = '#666';
    
    // Функция для показа сообщений
    function showMessage(text, color) {
        messageElement.textContent = text;
        messageElement.style.color = color;
        messageElement.style.borderColor = color;
    }
    
    // Функция для проверки валидности формы
    function checkFormValidity() {
        const emailValid = emailInput.value.trim() !== '' && 
                          emailInput.checkValidity();
        const phoneValid = phoneInput.value.trim() !== '' && 
                          phoneInput.checkValidity();
        
        // Разблокируем кнопку только если оба поля заполнены корректно
        submitAuth.disabled = !(emailValid && phoneValid);
    }
    
    // Открытие модального окна
    authBtn.addEventListener('click', function() {
        authModal.style.display = 'flex';
        // Очищаем форму при открытии
        authForm.reset();
        submitAuth.disabled = true;
    });
    
    // Закрытие модального окна через крестик
    closeModal.addEventListener('click', function() {
        authModal.style.display = 'none';
    });
    
    // Закрытие модального окна при клике на затемненную область
    authModal.addEventListener('click', function(event) {
        if (event.target === authModal) {
            authModal.style.display = 'none';
        }
    });
    
    // Проверка формы при вводе данных
    emailInput.addEventListener('input', checkFormValidity);
    phoneInput.addEventListener('input', checkFormValidity);
    
    // Обработка отправки формы авторизации
    authForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем стандартную отправку формы
        
        const email = emailInput.value.trim();
        const phone = phoneInput.value.trim();
        
        showMessage('🔐 Проходим авторизацию...', 'orange');
        
        // Имитация процесса авторизации
        setTimeout(function() {
            // Закрываем модальное окно
            authModal.style.display = 'none';
            
            // Показываем сообщение об успешной авторизации
            showMessage(`✅ Успешная авторизация! Добро пожаловать, ${email}`, 'green');
            
            // Меняем текст кнопки авторизации
            authBtn.textContent = '👤 Выйти';
            authBtn.style.background = 'linear-gradient(45deg, #dc3545, #c82333)';
            
            console.log(`Авторизация: Email - ${email}, Телефон - ${phone}`);
        }, 1500);
    });
    
    // Обработчик для кнопки "Загрузить видео"
    uploadBtn.addEventListener('click', async function() {
        showMessage('📹 Отправляем запрос на сервер...', 'orange');
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    action: 'upload',
                    button: 'uploadBtn'
                })
            });
            
            const data = await response.json();
            showMessage(` ${data.message} (${data.timestamp})`, 'green');
            
        } catch (error) {
            showMessage('❌ Ошибка соединения с сервером', 'red');
            console.error('Ошибка:', error);
        }
    });
    
    // Обработчик для кнопки "Вывод информации"
    infoBtn.addEventListener('click', async function() {
        showMessage('⌛ Запрашиваем информацию...', 'orange');
        
        try {
            const response = await fetch('/info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    action: 'getInfo',
                    button: 'infoBtn'
                })
            });
            
            const data = await response.json();
            showMessage(` ${data.message} | ${data.server_status} (${data.timestamp})`, 'blue');
            
        } catch (error) {
            showMessage('❌ Ошибка соединения с сервером', 'red');
            console.error('Ошибка:', error);
        }
    });
});