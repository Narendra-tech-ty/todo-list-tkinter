import tkinter as tk
from tkinter import ttk, messagebox
from database import db_connection
from task_form import TaskForm

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskFlow - Task Manager")
        self.root.geometry("1100x700")
        self.root.minsize(950, 600)
        self.root.configure(bg="#f4f7fb")

        self.search_var = tk.StringVar()
        self.status_filter = tk.StringVar(value="All Tasks")
        self.priority_filter = tk.StringVar(value="All Priorities")

        self.setup_style()
        self.build_ui()
        self.load_tasks()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background="white",
            foreground="#1f2937",
            fieldbackground="white",
            rowheight=42,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#eef2f7",
            foreground="#334155",
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )
        style.map(
            "Treeview",
            background=[("selected", "#dbeafe")],
            foreground=[("selected", "#172554")]
        )

    def build_ui(self):
        sidebar = tk.Frame(self.root, bg="#172554", width=225)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        brand = tk.Frame(sidebar, bg="#172554")
        brand.pack(fill="x", padx=20, pady=(30, 42))

        tk.Label(
            brand, text="✓", font=("Segoe UI", 22, "bold"),
            bg="#2563eb", fg="white", width=2
        ).pack(side="left")

        tk.Label(
            brand, text="TaskFlow",
            font=("Segoe UI", 22, "bold"),
            bg="#172554", fg="white"
        ).pack(side="left", padx=9)

        self.sidebar_button(sidebar, "📊  Dashboard", self.show_all, True)
        self.sidebar_button(sidebar, "📋  All Tasks", self.show_all)
        self.sidebar_button(
            sidebar, "⏳  Pending",
            lambda: self.set_status("Pending")
        )
        self.sidebar_button(
            sidebar, "✅  Completed",
            lambda: self.set_status("Completed")
        )

        tk.Label(
            sidebar, text="TaskFlow\nPython • Tkinter • MySQL",
            font=("Segoe UI", 9), bg="#172554", fg="#94a3b8",
            justify="left"
        ).pack(side="bottom", anchor="w", padx=20, pady=20)

        main = tk.Frame(self.root, bg="#f4f7fb")
        main.pack(side="right", fill="both", expand=True)

        header = tk.Frame(main, bg="#f4f7fb")
        header.pack(fill="x", padx=30, pady=(28, 10))

        title_box = tk.Frame(header, bg="#f4f7fb")
        title_box.pack(side="left")

        tk.Label(
            title_box, text="Dashboard",
            font=("Segoe UI", 28, "bold"),
            bg="#f4f7fb", fg="#172554"
        ).pack(anchor="w")

        tk.Label(
            title_box, text="Organize. Prioritize. Complete.",
            font=("Segoe UI", 10),
            bg="#f4f7fb", fg="#64748b"
        ).pack(anchor="w")

        tk.Button(
            header, text="＋  Add Task", command=self.add_task,
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb", fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat", cursor="hand2",
            padx=18, pady=10
        ).pack(side="right")

        stats = tk.Frame(main, bg="#f4f7fb")
        stats.pack(fill="x", padx=30, pady=10)

        self.total = self.stat_card(stats, "TOTAL TASKS")
        self.pending = self.stat_card(stats, "PENDING")
        self.completed = self.stat_card(stats, "COMPLETED")
        self.overdue = self.stat_card(stats, "OVERDUE")

        controls = tk.Frame(main, bg="#f4f7fb")
        controls.pack(fill="x", padx=30, pady=(12, 12))

        search_frame = tk.Frame(
            controls, bg="white",
            highlightbackground="#d8dee9", highlightthickness=1
        )
        search_frame.pack(
            side="left", fill="x", expand=True, padx=(0, 10)
        )

        tk.Label(
            search_frame, text="🔍",
            bg="white", fg="#64748b"
        ).pack(side="left", padx=(12, 4))

        search = tk.Entry(
            search_frame, textvariable=self.search_var,
            font=("Segoe UI", 10), bg="white",
            fg="#1f2937", relief="flat", bd=0
        )
        search.pack(side="left", fill="x", expand=True, ipady=9)
        search.bind("<KeyRelease>", lambda e: self.load_tasks())

        self.status_box = ttk.Combobox(
            controls, textvariable=self.status_filter,
            values=["All Tasks", "Pending", "Completed"],
            state="readonly", width=15
        )
        self.status_box.pack(side="left", padx=5)
        self.status_box.bind(
            "<<ComboboxSelected>>", lambda e: self.load_tasks()
        )

        self.priority_box = ttk.Combobox(
            controls, textvariable=self.priority_filter,
            values=["All Priorities", "Low", "Medium", "High"],
            state="readonly", width=16
        )
        self.priority_box.pack(side="left", padx=5)
        self.priority_box.bind(
            "<<ComboboxSelected>>", lambda e: self.load_tasks()
        )

        tk.Button(
            controls, text="↻", command=self.refresh,
            font=("Segoe UI", 13, "bold"),
            bg="white", fg="#475569",
            relief="flat", cursor="hand2", padx=10
        ).pack(side="left", padx=(8, 0))

        table_frame = tk.Frame(
            main, bg="white",
            highlightbackground="#e2e8f0",
            highlightthickness=1
        )
        table_frame.pack(
            fill="both", expand=True,
            padx=30, pady=(0, 15)
        )

        columns = ("id", "title", "due", "priority", "status")
        self.tree = ttk.Treeview(
            table_frame, columns=columns,
            show="headings", selectmode="browse"
        )

        headings = {
            "id": "ID", "title": "TASK",
            "due": "DUE DATE", "priority": "PRIORITY",
            "status": "STATUS"
        }
        widths = {
            "id": 55, "title": 380, "due": 150,
            "priority": 130, "status": 140
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(
                col, width=widths[col],
                anchor="w" if col == "title" else "center"
            )

        self.tree.tag_configure("High", foreground="#dc2626")
        self.tree.tag_configure("Medium", foreground="#d97706")
        self.tree.tag_configure("Low", foreground="#16a34a")
        self.tree.tag_configure("Completed", foreground="#16a34a")

        scroll = ttk.Scrollbar(
            table_frame, orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(
            side="left", fill="both", expand=True,
            padx=8, pady=8
        )
        scroll.pack(side="right", fill="y", pady=8)

        self.tree.bind("<Double-1>", lambda e: self.edit_task())

        actions = tk.Frame(main, bg="#f4f7fb")
        actions.pack(fill="x", padx=30, pady=(0, 25))

        self.action_button(actions, "✏ Edit", self.edit_task)
        self.action_button(actions, "🗑 Delete", self.delete_task)
        self.action_button(
            actions, "✓ Complete / Undo",
            self.toggle_complete
        )

    def sidebar_button(self, parent, text, command, active=False):
        tk.Button(
            parent, text=text, command=command,
            font=("Segoe UI", 11),
            bg="#2563eb" if active else "#172554",
            fg="white", activebackground="#1e40af",
            activeforeground="white",
            anchor="w", relief="flat", bd=0,
            cursor="hand2", padx=20, pady=13
        ).pack(fill="x", padx=12, pady=3)

    def stat_card(self, parent, title):
        card = tk.Frame(
            parent, bg="white", height=90,
            highlightbackground="#e2e8f0",
            highlightthickness=1
        )
        card.pack(
            side="left", fill="both",
            expand=True, padx=5
        )
        card.pack_propagate(False)

        inner = tk.Frame(card, bg="white")
        inner.pack(fill="both", expand=True, padx=15, pady=12)

        tk.Label(
            inner, text=title,
            font=("Segoe UI", 9, "bold"),
            bg="white", fg="#64748b"
        ).pack(anchor="w")

        value = tk.Label(
            inner, text="0",
            font=("Segoe UI", 22, "bold"),
            bg="white", fg="#1e293b"
        )
        value.pack(anchor="w")
        return value

    def action_button(self, parent, text, command):
        tk.Button(
            parent, text=text, command=command,
            font=("Segoe UI", 9, "bold"),
            bg="white", fg="#334155",
            activebackground="#e2e8f0",
            relief="flat", cursor="hand2",
            padx=14, pady=8
        ).pack(side="left", padx=(0, 8))

    def load_tasks(self):
        try:
            conn = db_connection()
            cur = conn.cursor()

            query = """
                SELECT id, title, due_date, priority, status
                FROM tasks WHERE 1=1
            """
            params = []

            search = self.search_var.get().strip()
            status = self.status_filter.get()
            priority = self.priority_filter.get()

            if search:
                query += " AND title LIKE %s"
                params.append("%" + search + "%")

            if status in ("Pending", "Completed"):
                query += " AND status=%s"
                params.append(status)

            if priority in ("Low", "Medium", "High"):
                query += " AND priority=%s"
                params.append(priority)

            query += """
                ORDER BY
                CASE WHEN status='Pending' THEN 0 ELSE 1 END,
                due_date ASC, id DESC
            """

            cur.execute(query, tuple(params))
            rows = cur.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for row in rows:
                task_id, title, due_date, priority, status = row
                tag = "Completed" if status == "Completed" else priority

                self.tree.insert(
                    "", "end",
                    values=(
                        task_id, title,
                        due_date.strftime("%d %b %Y"),
                        priority, status
                    ),
                    tags=(tag,)
                )

            cur.close()
            conn.close()
            self.update_statistics()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def update_statistics(self):
        try:
            conn = db_connection()
            cur = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM tasks")
            total = cur.fetchone()[0]

            cur.execute(
                "SELECT COUNT(*) FROM tasks WHERE status='Pending'"
            )
            pending = cur.fetchone()[0]

            cur.execute(
                "SELECT COUNT(*) FROM tasks WHERE status='Completed'"
            )
            completed = cur.fetchone()[0]

            cur.execute("""
                SELECT COUNT(*) FROM tasks
                WHERE status='Pending' AND due_date < CURDATE()
            """)
            overdue = cur.fetchone()[0]

            self.total.config(text=str(total))
            self.pending.config(text=str(pending))
            self.completed.config(text=str(completed))
            self.overdue.config(text=str(overdue))

            cur.close()
            conn.close()
        except Exception:
            pass

    def add_task(self):
        TaskForm(self.root, self.load_tasks)

    def edit_task(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showinfo(
                "Select Task", "Please select a task to edit."
            )
            return

        task_id = self.tree.item(selected[0], "values")[0]

        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT title, due_date, priority, status
                FROM tasks WHERE id=%s
            """, (task_id,))
            task = cur.fetchone()
            cur.close()
            conn.close()

            if task:
                TaskForm(
                    self.root, self.load_tasks,
                    (task_id, task)
                )
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def delete_task(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showinfo(
                "Select Task", "Please select a task to delete."
            )
            return

        values = self.tree.item(selected[0], "values")
        task_id, title = values[0], values[1]

        if not messagebox.askyesno(
            "Delete Task", f'Delete "{title}"?'
        ):
            return

        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM tasks WHERE id=%s",
                (task_id,)
            )
            conn.commit()
            cur.close()
            conn.close()
            self.load_tasks()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def toggle_complete(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showinfo(
                "Select Task", "Please select a task first."
            )
            return

        values = self.tree.item(selected[0], "values")
        task_id = values[0]
        new_status = (
            "Pending" if values[4] == "Completed"
            else "Completed"
        )

        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute(
                "UPDATE tasks SET status=%s WHERE id=%s",
                (new_status, task_id)
            )
            conn.commit()
            cur.close()
            conn.close()
            self.load_tasks()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def set_status(self, status):
        self.status_filter.set(status)
        self.load_tasks()

    def show_all(self):
        self.search_var.set("")
        self.status_filter.set("All Tasks")
        self.priority_filter.set("All Priorities")
        self.load_tasks()

    def refresh(self):
        self.load_tasks()
