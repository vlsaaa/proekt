// В обработчике uploadBtn добавьте:
const fileInput = document.createElement('input');
fileInput.type = 'file';
fileInput.accept = 'video/*';
fileInput.onchange = async function(e) {
    const file = e.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('video', file);
        
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        // ... остальной код
    }
};
fileInput.click();