# 💍 Wedding Task Manager

A full-stack web application built with Flask for managing wedding tasks, vendors, and timelines.

## 🔗 Live Demo
**[https://wedding-task-manager.onrender.com](https://wedding-task-manager.onrender.com)**

## 🛠️ Tech Stack
- **Backend:** Python, Flask, SQLAlchemy
- **Database:** SQLite
- **Frontend:** Jinja2, Bootstrap 5, HTML/CSS
- **Auth:** Flask-Login, Werkzeug password hashing
- **Deployment:** Render (Gunicorn WSGI)

## ✨ Features
- ✅ User Registration & Login with hashed passwords
- ✅ Full CRUD — Create, Read, Update, Delete tasks
- ✅ Task assignment and status tracking (Pending/Done)
- ✅ Flash messages and form validation
- ✅ REST API endpoints (GET, POST, PUT, DELETE)
- ✅ Responsive UI with Bootstrap 5
- ✅ Protected routes — login required

## 📡 REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks |
| GET | `/api/tasks/<id>` | Get single task |
| POST | `/api/tasks` | Create new task |
| PUT | `/api/tasks/<id>` | Update task |
| DELETE | `/api/tasks/<id>` | Delete task |

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/poulsamiksha7/Wedding-Task-Manager.git
cd Wedding-Task-Manager

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit `http://127.0.0.1:5000`

## 📁 Project Structure
wedding-task-manager/
├── app.py              # Main Flask application
├── requirements.txt    # Dependencies
├── Procfile           # Deployment config
├── templates/         # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── tasks.html
│   ├── add_task.html
│   └── edit_task.html
└── static/
└── css/
└── style.css
## 👩‍💻 Developer
**Samiksha Poul** — MCA Final Year
- GitHub: [@poulsamiksha7](https://github.com/poulsamiksha7)
- LinkedIn: [samiksha-poul](https://linkedin.com/in/samiksha-poul)
- 
