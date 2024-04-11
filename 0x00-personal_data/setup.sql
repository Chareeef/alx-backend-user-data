-- setup mysql server
-- configure permissions
CREATE DATABASE IF NOT EXISTS my_db;
DROP USER IF EXISTS 'ych'@'localhost';
CREATE USER IF NOT EXISTS 'ych'@'localhost' IDENTIFIED BY 'mlmlml';
GRANT ALL PRIVILEGES ON my_db.* TO 'ych'@'localhost';

USE my_db;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    email VARCHAR(256)
);

INSERT INTO users(email) VALUES ("bob@dylan.com");
INSERT INTO users(email) VALUES ("bib@dylan.com");
