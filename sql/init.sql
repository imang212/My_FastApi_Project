CREATE USER 'patrik'@'%' IDENTIFIED BY 'patrik123';
GRANT ALL PRIVILEGES ON Interesting_Places.* TO 'patrik'@'%';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS tasks_db;
USE tasks_db;

CREATE TABLE IF NOT EXISTS tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'NEW',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status (status)
);

-- testing tasks insert
INSERT INTO tasks (title, description, status) VALUES
    ('Nakoupit potraviny', 'Mléko, chléb, vejce, sýr', 'NEW'),
    ('Dokončit projekt', 'Dodělat webový úkolníček pro kurz', 'NEW'),
    ('Zavolat lékaři', 'Objednat se na kontrolu', 'COMPLETE'),
    ('Uklidit byt', 'Vysát, vytřít, utřít prach', 'NEW');


