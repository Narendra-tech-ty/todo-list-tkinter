"""
Advanced To-Do List App
Part 1 : MySQL Connection + Database Functions
"""

import sys
import tkinter as tk
from tkinter import messagebox,ttk
import mysql.connector

# -----------------------------
# Loading Splash Screen
# -----------------------------

splash = tk.Tk()
splash.overrideredirect(True)
splash.configure(bg="black")

splash_width = 300
splash_height = 150

screen_w = splash.winfo_screenwidth()
screen_h = splash.winfo_screenheight()

x = (screen_w - splash_width) // 2
y = (screen_h - splash_height) // 2

splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")

splash_title = tk.Label(
    splash,
    text="📝 To-Do List",
    font=("Segoe UI", 16, "bold"),
    fg="orange",
    bg="black"
)

splash_title.pack(pady=(30, 10))

loading_label = tk.Label(
    splash,
    text="Loading",
    font=("Arial", 12),
    fg="lightgreen",
    bg="black"
)

loading_label.pack()

loading_frames = ["Loading", "Loading.", "Loading..", "Loading..."]
loading_index = [0]

def animate_loading():

    loading_label.config(
        text=loading_frames[loading_index[0] % len(loading_frames)]
    )

    loading_index[0] += 1

    splash.after(300, animate_loading)

animate_loading()

splash.after(1500, splash.destroy)

splash.mainloop()

# -----------------------------
# MySQL Connection
# -----------------------------

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tododb"
    )

    cursor = conn.cursor()

except mysql.connector.Error as e:
    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(
        "Database Error",
        f"Could not connect to MySQL.\n\n{e}"
    )

    root.destroy()
    sys.exit()

# -----------------------------
# Check Required Columns
# -----------------------------

cursor.execute("""
SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA='tododb'
AND TABLE_NAME='tasks'
""")

columns = []

for col in cursor.fetchall():
    columns.append(col[0])

if "priority" not in columns:
    cursor.execute("""
    ALTER TABLE tasks
    ADD priority VARCHAR(10)
    DEFAULT 'Medium'
    """)

if "due_date" not in columns:
    cursor.execute("""
    ALTER TABLE tasks
    ADD due_date VARCHAR(20)
    DEFAULT ''
    """)

if "completed" not in columns:
    cursor.execute("""
    ALTER TABLE tasks
    ADD completed TINYINT(1)
    DEFAULT 0
    """)

conn.commit()

# -----------------------------
# Database Functions
# -----------------------------

def add_task_db(task, priority, due_date):

    sql = """
    INSERT INTO tasks
    (task, priority, due_date, completed)
    VALUES (%s,%s,%s,0)
    """

    values = (task, priority, due_date)

    cursor.execute(sql, values)
    conn.commit()


def get_all_tasks():

    cursor.execute("""
    SELECT id,
           task,
           priority,
           due_date,
           completed
    FROM tasks
    """)

    return cursor.fetchall()


def update_task_db(task_id, task, priority, due_date):

    sql = """
    UPDATE tasks
    SET task=%s,
        priority=%s,
        due_date=%s
    WHERE id=%s
    """

    values = (
        task,
        priority,
        due_date,
        task_id
    )

    cursor.execute(sql, values)
    conn.commit()


def complete_task_db(task_id, completed):

    sql = """
    UPDATE tasks
    SET completed=%s
    WHERE id=%s
    """

    cursor.execute(sql, (completed, task_id))
    conn.commit()


def delete_task_db(task_id):

    cursor.execute(
        "DELETE FROM tasks WHERE id=%s",
        (task_id,)
    )

    conn.commit()


def clear_all_db():

    cursor.execute(
        "DELETE FROM tasks"
    )

    conn.commit()

# -----------------------------
# Variables
# -----------------------------

task_list = []
task_ids = []

selected_task_id = None

# -----------------------------
# GUI FUNCTIONS
# -----------------------------

def format_task(task, priority, due_date, completed):

    if completed == 1:
        mark = "☑"
    else:
        mark = "☐"

    if due_date == "":
        return f"{mark} {task} [{priority}]"
    else:
        return f"{mark} {task} | 📅 {due_date} [{priority}]"


# -----------------------------
# Refresh Task List
# -----------------------------

def refresh_task_list():

    task_list.clear()
    task_ids.clear()
    task_listbox.delete(0, tk.END)

    tasks = get_all_tasks()

    print(tasks)

    total = len(tasks)
    completed = 0

    for row in tasks:

        task_list.append(row)

        task_id = row[0]
        task = row[1]
        priority = row[2]
        due_date = row[3]
        done = row[4]

        task_ids.append(task_id)

        task_listbox.insert(
            tk.END,
            format_task(task, priority, due_date, done)
        )

        index = task_listbox.size() - 1

        if done == 1:
            task_listbox.itemconfig(index, fg="gray")
            completed += 1

        elif priority == "High":
            task_listbox.itemconfig(index, fg="red")

        elif priority == "Medium":
            task_listbox.itemconfig(index, fg="yellow")

        else:
            task_listbox.itemconfig(index, fg="light blue")

    pending = total - completed

    count_label.config(
        text=f"Total : {total}   Pending : {pending}   Done : {completed}"
    )

    search_task()

    print("Listbox size:", task_listbox.size())


# -----------------------------
# Search Task
# -----------------------------

def search_task(event=None):

    search = search_var.get().strip()

    # Ignore placeholder
    if search == "🔍 Search Tasks":
        search = ""

    search = search.lower()

    task_listbox.delete(0, tk.END)
    task_ids.clear()

    for row in task_list:

        task_id = row[0]
        task = row[1]
        priority = row[2]
        due_date = row[3]
        done = row[4]

        if search == "" or search in task.lower():

            task_ids.append(task_id)

            task_listbox.insert(
                tk.END,
                format_task(task, priority, due_date, done)
            )

            index = task_listbox.size() - 1

            if done == 1:
                task_listbox.itemconfig(index, fg="gray")
            elif priority == "High":
                task_listbox.itemconfig(index, fg="red")
            elif priority == "Medium":
                task_listbox.itemconfig(index, fg="yellow")
            else:
                task_listbox.itemconfig(index, fg="cyan")
                
# -----------------------------
# Add Task
# -----------------------------

def add_task():

    task = task_entry.get().strip()
    priority = priority_var.get()
    due_date = due_entry.get().strip()

    if due_date == "" or due_date == "YYYY-MM-DD":
        due_date = ""

    if task == "":
        messagebox.showwarning(
            "Warning",
            "Please enter a task."
        )
        return

    add_task_db(task, priority, due_date)

    task_entry.delete(0, tk.END)
    due_entry.delete(0, tk.END)

    priority_var.set("Medium")

    task_entry.focus()

    refresh_task_list()

    messagebox.showinfo(
    "Success",
    "Task added successfully."
)


# -----------------------------
# Edit Task
# -----------------------------

def edit_task():

    global selected_task_id

    selected = task_listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a task first."
        )
        return

    index = selected[0]
    selected_task_id = task_ids[index]

    for row in task_list:

        if row[0] == selected_task_id:

            task_entry.delete(0, tk.END)
            task_entry.insert(0, row[1])

            priority_var.set(row[2])

            due_entry.delete(0, tk.END)
            due_entry.insert(0, row[3])

            break

    add_button.config(
        text="💾 Save",
        command=save_task
    )


# -----------------------------
# Save Edited Task
# -----------------------------

def save_task():

    global selected_task_id

    task = task_entry.get().strip()
    priority = priority_var.get()
    due_date = due_entry.get().strip()

    if task == "":
        messagebox.showwarning(
            "Warning",
            "Task cannot be empty."
        )
        return

    update_task_db(
        selected_task_id,
        task,
        priority,
        due_date
    )

    cancel_edit()

    refresh_task_list()


# -----------------------------
# Cancel Edit
# -----------------------------

def cancel_edit():

    global selected_task_id

    selected_task_id = None

    task_entry.delete(0, tk.END)
    due_entry.delete(0, tk.END)

    priority_var.set("Medium")

    add_button.config(
        text="➕ Add Task",
        command=add_task
    )


# -----------------------------
# Toggle Complete
# -----------------------------

def toggle_complete():

    selected = task_listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a task first."
        )
        return

    index = selected[0]
    task_id = task_ids[index]

    for row in task_list:

        if row[0] == task_id:

            if row[4] == 1:
                complete_task_db(task_id, 0)
            else:
                complete_task_db(task_id, 1)

            break

    refresh_task_list()


# -----------------------------
# Delete Task
# -----------------------------

def delete_task():

    selected = task_listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select a task first."
        )
        return

    index = selected[0]
    task_id = task_ids[index]

    answer = messagebox.askyesno(
        "Delete Task",
        "Are you sure?"
    )

    if answer:
        delete_task_db(task_id)
        refresh_task_list()


# -----------------------------
# Clear All
# -----------------------------

def clear_all():

    answer = messagebox.askyesno(
        "Clear All",
        "Delete all tasks?"
    )

    if answer:
        clear_all_db()
        refresh_task_list()


# -----------------------------
# Close Window
# -----------------------------

def close_window():

    cursor.close()
    conn.close()

    window.destroy()

# -----------------------------
# COLORS
# -----------------------------

BG = "black"
PANEL = "gray20"
FG = "white"

GREEN = "green"
RED = "red"
ORANGE = "orange"
BLUE = "blue"

# -----------------------------
# MAIN WINDOW
# -----------------------------

window = tk.Tk()

window.title("📝 Advanced To-Do List")
window.configure(bg=BG)

width = 460
height = 620

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - width) // 2
y = (screen_height - height) // 2

window.geometry(f"{width}x{height}+{x}+{y}")

# -----------------------------
# MAIN FRAME
# -----------------------------

frame = tk.Frame(window, bg=BG)
frame.pack(fill="both", expand=True, padx=15, pady=15)

# -----------------------------
# TITLE
# -----------------------------

title = tk.Label(
    frame,
    text="✔ My To-Do List ✔",
    font=("Segoe UI", 22, "bold"),
    fg="orange",
    bg=BG
)

title.pack(pady=5)

welcome = tk.Label(
    frame,
    text="Manage your daily tasks easily",
    font=("Arial", 11),
    fg="lightgreen",
    bg=BG
)

welcome.pack()

# -----------------------------
# TASK COUNTER
# -----------------------------

count_label = tk.Label(
    frame,
    text="Total : 0   Pending : 0   Done : 0",
    font=("Segoe UI", 11, "bold"),
    fg="lightgreen",
    bg=BG
)

count_label.pack(pady=5)

# -----------------------------
# SEARCH BAR
# -----------------------------

search_var = tk.StringVar()

search_entry = tk.Entry(
    frame,
    textvariable=search_var,
    font=("Arial", 12),
    bg=PANEL,
    fg=FG,
    insertbackground="white"
)
search_entry.insert(0, "🔍 Search Tasks")

def clear_search(event):
    if search_entry.get() == "🔍 Search Tasks":
        search_entry.delete(0, tk.END)
        search_entry.config(fg="white")

def restore_search(event):
    if search_entry.get() == "":
        search_entry.insert(0, "🔍 Search Tasks")
        search_entry.config(fg="gray")

search_entry.bind("<FocusIn>", clear_search)
search_entry.bind("<FocusOut>", restore_search)


search_entry.pack(fill="x", pady=8)

search_entry.bind("<KeyRelease>", search_task)

# -----------------------------
# TASK ENTRY
# -----------------------------

task_entry = tk.Entry(
    frame,
    font=("Arial", 13),
    bg=PANEL,
    fg="gray",
    insertbackground="white"
)

task_entry.insert(0, "Enter your task")

def clear_task(event):
    if task_entry.get() == "Enter your task":
        task_entry.delete(0, tk.END)
        task_entry.config(fg="white")

def restore_task(event):
    if task_entry.get().strip() == "":
        task_entry.insert(0, "Enter your task")
        task_entry.config(fg="gray")

task_entry.bind("<FocusIn>", clear_task)
task_entry.bind("<FocusOut>", restore_task)

task_entry.pack(fill="x", pady=5)

task_entry.bind("<Return>", lambda event: add_task())

# -----------------------------
# PRIORITY + DUE DATE
# -----------------------------

option_frame = tk.Frame(frame, bg=BG)
option_frame.pack(fill="x", pady=5)

priority_var = tk.StringVar()
priority_var.set("Medium")

priority_box = ttk.Combobox(
    option_frame,
    textvariable=priority_var,
    values=["Low", "Medium", "High"],
    state="readonly",
    width=12
)

priority_box.pack(side="left", padx=(0, 10), ipady=3)

due_entry = tk.Entry(
    option_frame,
    width=20,
    font=("Arial", 11),
    bg=PANEL,
    fg="gray",
    insertbackground="white"
)

due_entry.insert(0, "Due Date (DD/MM/YY)")

def clear_due(event):
    if due_entry.get() == "Due Date (DD/MM/YY)":
        due_entry.delete(0, tk.END)
        due_entry.config(fg="white")

def restore_due(event):
    if due_entry.get().strip() == "":
        due_entry.insert(0, "Due Date (DD/MM/YY)")
        due_entry.config(fg="gray")

due_entry.bind("<FocusIn>", clear_due)
due_entry.bind("<FocusOut>", restore_due)

due_entry.pack(
    side="left",
    padx=10,
    ipady=3
)
# -----------------------------
# ADD / CANCEL BUTTONS
# -----------------------------

button_frame = tk.Frame(frame, bg=BG)
button_frame.pack(fill="x", pady=10)

add_button = tk.Button(
    button_frame,
    text="➕ Add Task",
    bg=GREEN,
    fg="white",
    font=("Arial", 12),
    relief="flat",
    command=add_task
)

add_button.pack(
    side="left",
    expand=True,
    fill="x",
    padx=2
)

cancel_button = tk.Button(
    button_frame,
    text="✖ Cancel",
    bg="#555555",
    fg="white",
    font=("Arial", 12),
    relief="flat",
    command=cancel_edit
)

cancel_button.pack(
    side="left",
    expand=True,
    fill="x",
    padx=2
)

# -----------------------------
# LISTBOX
# -----------------------------

list_frame = tk.Frame(frame, bg=PANEL)
list_frame.pack(
    fill="both",
    expand=True,
    pady=10
)

scrollbar = tk.Scrollbar(list_frame)

scrollbar.pack(
    side="right",
    fill="y"
)

task_listbox = tk.Listbox(
    list_frame,
    font=("Consolas", 11),
    bg=PANEL,
    fg=FG,
    selectbackground="skyblue",
    selectforeground="black",
    yscrollcommand=scrollbar.set
)

task_listbox.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.config(
    command=task_listbox.yview
)

# -----------------------------
# ACTION BUTTONS
# -----------------------------

action_frame = tk.Frame(frame, bg=BG)
action_frame.pack(fill="x", pady=10)

complete_button = tk.Button(
    action_frame,
    text="✅ Mark Done",
    bg=BLUE,
    fg="white",
    font=("Arial", 11),
    relief="flat",
    command=toggle_complete
)

complete_button.pack(
    side="left",
    expand=True,
    fill="x",
    padx=2
)

edit_button = tk.Button(
    action_frame,
    text="✏ Edit Task",
    bg="#666666",
    fg="white",
    font=("Arial", 11),
    relief="flat",
    command=edit_task
)

edit_button.pack(
    side="left",
    expand=True,
    fill="x",
    padx=2
)

delete_button = tk.Button(
    action_frame,
    text="🗑 Delete",
    bg=RED,
    fg="white",
    font=("Arial", 11),
    relief="flat",
    command=delete_task
)

delete_button.pack(
    side="left",
    expand=True,
    fill="x",
    padx=2
)

clear_button = tk.Button(
    action_frame,
    text="🧹 Clear",
    bg=ORANGE,
    fg="white",
    font=("Arial", 11),
    relief="flat",
    command=clear_all
)

clear_button.pack(
    side="left",
    expand=True,
    fill="x",
    padx=2
)

# -----------------------------
# FOOTER
# -----------------------------

footer = tk.Label(
    frame,
    text="💻 Developed by Narendra Sarvaiya",
    font=("Segoe UI", 9, "italic"),
    fg="skyblue",
    bg=BG
)

footer.pack(pady=10)

# -----------------------------
# LOAD TASKS
# -----------------------------

refresh_task_list()

# -----------------------------
# WINDOW CLOSE
# -----------------------------

window.protocol(
    "WM_DELETE_WINDOW",
    close_window
)

# -----------------------------
# RUN APPLICATION
# -----------------------------

window.mainloop()
