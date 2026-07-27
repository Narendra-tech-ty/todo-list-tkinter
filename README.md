# 📝 Advanced To-Do List App

A desktop To-Do List application built with **Python (Tkinter)** for the GUI and **MySQL** (via XAMPP) for data storage.

## ✨ Features

- Add, edit, delete, and complete tasks
- Set task priority (Low / Medium / High) with color-coded display
- Add due dates to tasks
- Live search to filter tasks as you type
- Task counter showing total, pending, and completed tasks
- Dark theme UI
- Animated loading splash screen on startup

## 🛠 Tech Stack

- **Python 3** — core language
- **Tkinter** — GUI framework
- **MySQL** — database (via XAMPP)
- **mysql-connector-python** — Python-MySQL connection

## 📦 Requirements

- Python 3.x
- XAMPP (with MySQL running)
- `mysql-connector-python` package

Install the required package:
```
pip install mysql-connector-python
```

## ⚙️ Setup

1. Start **XAMPP** and make sure **MySQL** is running.
2. Create a database named `tododb` (via phpMyAdmin or MySQL CLI).
3. Create a `tasks` table (the app will auto-add missing columns like `priority`, `due_date`, and `completed` if the base table exists).
4. Update the database connection details in the script if needed:
   ```python
   host="localhost"
   user="root"
   password=""
   database="tododb"
   ```
5. Run the app:
   ```
   python todo_app.py
   ```

## 📸 Preview

*(Add a screenshot of the app here once you have one)*

## 👨‍💻 Developed By

**Narendra Sarvaiya**
