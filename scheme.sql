DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS videos;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE videos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    filename VARCHAR(255),
    file_path VARCHAR(500),  -- Path to actual file
    file_size BIGINT,
    mime_type VARCHAR(50),
    upload_date DATETIME,
    user_id INT,
    duration INT,  -- in seconds
    thumbnail_path VARCHAR(500),
    FOREIGN KEY (user_id) REFERENCES user (id)
);