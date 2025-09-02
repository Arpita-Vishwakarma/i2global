# 📝 NotesApp

A full-stack **Notes Taking Application** with user authentication and complete CRUD operations for notes, featuring a handcrafted UI. This project is designed to run locally using Docker and provides a seamless experience for managing personal notes securely.

### Prerequisites
- **Docker** and **Docker Compose** (if running with containers).
- **Python 3.10+** and **pip** (if running locally without Docker).
- **Node.js** (only if you’re working on the frontend separately).

---

## 🔧 Setup Instructions

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd i2global
```
#### 2. Create a virtual environment
```bash
python -m venv venv
```

#### 3. Activate Virtual Environment
Activate the virtual environment depending on your operating system:
```bash
# For Linux or macOS:
source venv/bin/activate

# For Windows (PowerShell):
venv\Scripts\Activate.ps1

# For Windows (Command Prompt):
venv\Scripts\activate.bat
```

#### 4. Install dependencies
```bash
pip install -r requirements.txt
```
#### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
#### 6. Collect static files
```bash
python manage.py collectstatic --noinput
```
#### 7. Run the development server
```bash
python manage.py runserver
```


## 🚀 Features

- 🔐 **User Authentication**: Secure Sign Up, Sign In, and Profile management using JWT.
- 📝 **Notes Management**: Create, view, edit, and delete notes with a clean, intuitive interface.
- 🎨 **Handcrafted UI**: Custom-built components using only Tailwind CSS utilities (no prebuilt UI libraries).
- ⚡ **REST API**: Powered by Django REST Framework for robust backend functionality.
- 🗂️ **Organized Structure**: Clear separation of backend and frontend codebases.
- 🐳 **Dockerized**: Runs locally with Docker and Docker Compose for easy setup.

## 📸 Screenshots

### 🏠 Home Page
![Home Page](./screenshots/Home.png)

### 🔑 Sign In Page
![Sign In](./screenshots/Sign%20In.png)

### 🆕 Sign Up Page
![Sign Up](./screenshots/Sign%20Up.png)

### 📒 Notes List Page
![Notes List](./screenshots/Notes%20list.png)

## 🛠️ Tech Stack

### Backend
- **Django 5.x**: Python web framework for rapid development.
- **Django REST Framework**: For building scalable REST APIs.
- **JWT Authentication**: Using `djangorestframework-simplejwt` for secure user sessions.
- **MySQL**: Database managed via Docker.

### Frontend
- **HTML**: Structure and markup of web pages.
- **CSS**: Styling and layout of the website.
- **JavaScript**: Adding interactivity and basic frontend logic.

> ⚡ Note: The frontend is currently in development. Next.js or other frameworks may be added later.

### DevOps
- **Docker + Docker Compose**: Containerized setup for consistent development and deployment.


