# mini-project1
I-m-holo

미니프로젝트1/
├── app.py
├── db.py              👈 여기로 이동하려는 것
├── auth.py            👈 여기서 db.py를 불러옴
├── templates/
│   ├── login.html
│   └── register.html


#MySQL root 계정으로

CREATE USER 'proj-1'@'localhost' IDENTIFIED BY 'admin';
CREATE DATABASE `proj-1` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
GRANT ALL PRIVILEGES ON `proj-1`.* TO 'proj-1'@'localhost';
FLUSH PRIVILEGES;

#workbench 에서 계정 생성

host='127.0.0.1',
port=3306,
user='proj-1',
passwd='admin',
database='proj-1'

#이후 회원가입 정보 MySQL에서 확인 가능

USE `proj-1`;
SELECT * FROM users;
