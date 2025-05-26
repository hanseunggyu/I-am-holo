# mini-project1 <br>
I-m-holo <br>

미니프로젝트1/ <br>
├── app.py <br>
├── db.py              👈 여기로 이동하려는 것 <br>
├── auth.py            👈 여기서 db.py를 불러옴 <br>
├── templates/ <br>
│   ├── login.html <br>
│   └── register.html <br>


#MySQL root 계정으로 <br>

CREATE USER 'proj-1'@'localhost' IDENTIFIED BY 'admin'; <br>
CREATE DATABASE `proj-1` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci; <br>
GRANT ALL PRIVILEGES ON `proj-1`.* TO 'proj-1'@'localhost'; <br>
FLUSH PRIVILEGES; <br>

#workbench 에서 계정 생성 <br>

host='127.0.0.1', <br>
port=3306, <br>
user='proj-1', <br>
passwd='admin', <br>
database='proj-1' <br>

#이후 회원가입 정보 MySQL에서 확인 가능 <br>

USE `proj-1`; <br>
SELECT * FROM users; <br>
