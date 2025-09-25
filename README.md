# 📝 Notes App (FastAPI + PostgreSQL + [Optional Django UI])

This is a **note-taking application** where users can create, store, and share notes securely.  
The backend is powered by **FastAPI** with **PostgreSQL** as the database.  

Additionally, there is a lightweight **Django frontend** (optional) that demonstrates how the FastAPI backend can be consumed by a real web interface.  
If you prefer, you can interact **directly with the API** through Swagger UI without using Django.

---

## 🚀 Features
- 🔐 Authentication with JWT (FastAPI)  
- 📝 Notes CRUD (Create, Read, Update, Delete)  
- 👥 Share notes with other users  
- 🌐 Interactive Swagger API docs  
- 🖥 Optional Django UI for testing via simple forms  
- 🗄 PostgreSQL for persistence  

---

## ⚡ Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/) — backend API  
- [PostgreSQL](https://www.postgresql.org/) — database  
- [Django](https://www.djangoproject.com/) — optional frontend  
- [Requests](https://docs.python-requests.org/) — API calls from Django → FastAPI  
- [Uvicorn](https://www.uvicorn.org/) — ASGI server  

---

## 📦 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/felixmokayabeatz/notes_app.git
cd notes_app
```

## 2️⃣ Create and Acticvate the virtual environment
#### On windows example

```bash
# Create
python -m venv notes_app_v_env
# Activate
notes_app_v_env\Scripts\activate
```

#### On Linux/macOS
```bash
# Create
python3 -m venv notes_app_v_env

# Activate
source notes_app_v_env/bin/activate
```

## 3️⃣ Install the Depedencies/Packages

```bash
pip install -r requirements.txt
```

## 4️⃣ Create and connect the datababse (PostgreSQL)

First, make sure you have downloaded PostgreSQL from [the official website](https://www.postgresql.org/download/).  
## Database Setup  
### a) Using the terminal

```bash

# This is the default Super user, if you set another use that.
psql -U postgres

# Create User and update your .env accordingly
CREATE USER felix_test WITH PASSWORD '1234';

# Create Databases
CREATE DATABASE felix_notes_app_db OWNER felix_test; # For FastAPI
CREATE DATABASE felix_notes_app_db_django OWNER felix_test; # For Django

# Give Privileges
GRANT ALL PRIVILEGES ON DATABASE felix_notes_app_db TO felix_test;
GRANT ALL PRIVILEGES ON DATABASE felix_notes_app_db_django TO felix_test;

#Exit from postgres terminal
\q
```

### b) Using PgAdmin (I reccommend this for people with less experince with postgres on terminal)

Download PgAdmin from [the official website](https://www.pgadmin.org/download/) and use it to create dbs and users just like above but with a GUI





## 2️⃣ Run FastAPI Backend

## Open a terminal and start the backend FastAPI with the following command:
```bash
uvicorn app.main:app --reload
```

### Runs on http://127.0.0.1:8000

### Visit Swagger docs👇
```bash
http://127.0.0.1:8000/docs/
```

### 3️⃣ (Optional) Run Django Frontend

### Open another terminal (keep FastAPI running in the first one)
### Apply the migrations to use default tables like sessions

```bash
python manage.py migrate
```
### Start Django:
```bash
python manage.py runserver 8001
```

### Runs on 👉 http://127.0.0.1:8001

Visit login page👇:

```bash
http://127.0.0.1:8001/login/
```
### 👉 Important: Always run Django and FastAPI in separate terminals at the same time on diffrent ports.