-- 데이터베이스 초기화 스크립트
CREATE DATABASE IF NOT EXISTS ooop_db;
USE ooop_db;

-- 사용자 테이블 생성
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 샘플 데이터 삽입
INSERT INTO users (name, email) VALUES 
('홍길동', 'hong@example.com'),
('김철수', 'kim@example.com'),
('이영희', 'lee@example.com');
