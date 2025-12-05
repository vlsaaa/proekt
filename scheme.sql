DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS videos;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
-- ========== ДОБАВЛЕНИЕ ПОЛЕЙ ДЛЯ ML ОБРАБОТКИ ==========

-- Добавляем колонки для хранения результатов ML
ALTER TABLE videos ADD COLUMN status VARCHAR(20) DEFAULT 'uploaded';
ALTER TABLE videos ADD COLUMN processed_at DATETIME;
ALTER TABLE videos ADD COLUMN people_entered INTEGER;
ALTER TABLE videos ADD COLUMN people_exited INTEGER;
ALTER TABLE videos ADD COLUMN queue_length INTEGER;
ALTER TABLE videos ADD COLUMN alert_level VARCHAR(10);
ALTER TABLE videos ADD COLUMN alert_message TEXT;
ALTER TABLE videos ADD COLUMN ml_results TEXT;