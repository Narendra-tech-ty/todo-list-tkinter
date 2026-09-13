import tkinter as tk
from tkinter import messagebox
from database import setup_database
from splash import SplashScreen
from dashboard import Dashboard

def start_app():
    try:
        setup_database()
    except Exception as e:
        messagebox.showerror(
            "MySQL Connection Error",
            "Could not connect to XAMPP MySQL.\n\n"
            "Make sure MySQL is running in XAMPP.\n\n"
            f"Error: {e}"
        )
        return

    root = tk.Tk()
    Dashboard(root)
    root.mainloop()

if __name__ == "__main__":
    splash_root = tk.Tk()
    SplashScreen(splash_root, start_app)
    splash_root.mainloop()
