import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import db_connection

class TaskForm:
    def __init__(self, parent, refresh_callback, existing=None):
        self.refresh_callback = refresh_callback
        self.existing = existing

        self.window = tk.Toplevel(parent)
        self.window.title("Edit Task" if existing else "Add New Task")
        self.window.geometry("460x420")
        self.window.resizable(False, False)
        self.window.configure(bg="#f8fafc")
        self.window.transient(parent)
        self.window.grab_set()

        self.build()

    def build(self):
        heading = "Edit Task" if self.existing else "Add New Task"

        tk.Label(
            self.window, text=heading,
            font=("Segoe UI", 21, "bold"),
            bg="#f8fafc", fg="#172554"
        ).pack(anchor="w", padx=30, pady=(25, 20))

        form = tk.Frame(self.window, bg="#f8fafc")
        form.pack(fill="both", expand=True, padx=30)

        tk.Label(
            form, text="Task Title *",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fafc", fg="#334155"
        ).pack(anchor="w")

        self.title_entry = tk.Entry(
            form, font=("Segoe UI", 11), relief="solid", bd=1
        )
        self.title_entry.pack(fill="x", ipady=7, pady=(5, 15))

        tk.Label(
            form, text="Due Date *  (YYYY-MM-DD)",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fafc", fg="#334155"
        ).pack(anchor="w")

        self.date_entry = tk.Entry(
            form, font=("Segoe UI", 11), relief="solid", bd=1
        )
        self.date_entry.pack(fill="x", ipady=7, pady=(5, 15))

        tk.Label(
            form, text="Priority",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fafc", fg="#334155"
        ).pack(anchor="w")

        self.priority = tk.StringVar(value="Medium")
        ttk.Combobox(
            form, textvariable=self.priority,
            values=["Low", "Medium", "High"], state="readonly"
        ).pack(fill="x", pady=(5, 15))

        self.status = tk.StringVar(value="Pending")

        if self.existing:
            task_id, data = self.existing
            title, due_date, priority, status = data

            self.title_entry.insert(0, title)
            self.date_entry.insert(0, due_date.strftime("%Y-%m-%d"))
            self.priority.set(priority)
            self.status.set(status)

            tk.Label(
                form, text="Status",
                font=("Segoe UI", 10, "bold"),
                bg="#f8fafc", fg="#334155"
            ).pack(anchor="w")

            ttk.Combobox(
                form, textvariable=self.status,
                values=["Pending", "Completed"], state="readonly"
            ).pack(fill="x", pady=(5, 15))

        buttons = tk.Frame(form, bg="#f8fafc")
        buttons.pack(fill="x")

        tk.Button(
            buttons, text="Cancel", command=self.window.destroy,
            font=("Segoe UI", 10, "bold"),
            bg="#e2e8f0", fg="#334155",
            relief="flat", padx=20, pady=9
        ).pack(side="right", padx=(8, 0))

        tk.Button(
            buttons, text="Save Task", command=self.save,
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb", fg="white",
            activebackground="#1d4ed8",
            relief="flat", padx=20, pady=9
        ).pack(side="right")

        self.title_entry.focus()

    def save(self):
        title = self.title_entry.get().strip()
        date_text = self.date_entry.get().strip()

        if not title:
            messagebox.showwarning(
                "Missing Title", "Please enter a task title.",
                parent=self.window
            )
            return

        try:
            date_value = datetime.strptime(
                date_text, "%Y-%m-%d"
            ).date()
        except ValueError:
            messagebox.showwarning(
                "Invalid Date",
                "Use YYYY-MM-DD, for example 2026-09-15.",
                parent=self.window
            )
            return

        try:
            conn = db_connection()
            cur = conn.cursor()

            if self.existing:
                cur.execute("""
                    UPDATE tasks
                    SET title=%s, due_date=%s,
                        priority=%s, status=%s
                    WHERE id=%s
                """, (
                    title, date_value, self.priority.get(),
                    self.status.get(), self.existing[0]
                ))
            else:
                cur.execute("""
                    INSERT INTO tasks
                    (title, due_date, priority, status)
                    VALUES (%s, %s, %s, 'Pending')
                """, (title, date_value, self.priority.get()))

            conn.commit()
            cur.close()
            conn.close()

            self.window.destroy()
            self.refresh_callback()

        except Exception as e:
            messagebox.showerror(
                "Database Error", str(e), parent=self.window
            )
