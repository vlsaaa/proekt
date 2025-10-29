// Ждем пока вся страница загрузится
document.addEventListener('DOMContentLoaded', function() {
    // Находим элементы на странице
    const uploadBtn = document.getElementById('uploadBtn');
    const infoBtn = document.getElementById('infoBtn');
    const messageElement = document.getElementById('message');
    
    // Показываем стартовое сообщение
    messageElement.textContent = 'Готов к работе! Нажмите любую кнопку.';
    messageElement.style.color = '#666';
    
    // Функция для показа сообщений
    function showMessage(text, color) {
        messageElement.textContent = text;
        messageElement.style.color = color;
        messageElement.style.borderColor = color;
    }
    
    // Обработчик для кнопки "Загрузить видео"
    uploadBtn.addEventListener('click', async function() {
        showMessage(' Отправляем запрос на сервер...', 'orange');
        
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
            showMessage(' Ошибка соединения с сервером', 'red');
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
            showMessage(' Ошибка соединения с сервером', 'red');
            console.error('Ошибка:', error);
        }
    });
});