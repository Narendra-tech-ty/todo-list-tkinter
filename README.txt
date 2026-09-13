TASKFLOW
========

College-level To-Do List using Python, Tkinter, MySQL and XAMPP.

FILES
-----
main.py          - Starts the program
database.py      - MySQL connection/database setup
splash.py        - Animated splash screen
dashboard.py     - Main dashboard
task_form.py     - Add/Edit task window
requirements.txt - Required package

SETUP
-----
1. Start MySQL in XAMPP.
2. Open a terminal in this folder.
3. Run:
   pip install -r requirements.txt
4. Run:
   python main.py

The program automatically creates:
Database: taskflow_db
Table: tasks

DEFAULT MYSQL
-------------
Host: localhost
Port: 3306
User: root
Password: empty

If your XAMPP MySQL has a password, edit MYSQL_PASSWORD
in database.py.

FEATURES
--------
- Attractive animated splash screen
- Add task
- View tasks
- Edit task
- Delete task
- Complete/undo task
- Pending/Completed status
- Low/Medium/High priority
- Due date
- Search
- Status filter
- Priority filter
- Dashboard statistics
- MySQL storage
- No login
