import tkinter as tk

class SplashScreen:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.progress = 0

        self.root.overrideredirect(True)
        w, h = 700, 430
        x = (root.winfo_screenwidth() - w) // 2
        y = (root.winfo_screenheight() - h) // 2
        root.geometry(f"{w}x{h}+{x}+{y}")
        root.configure(bg="#172554")

        box = tk.Frame(root, bg="#172554")
        box.pack(fill="both", expand=True)

        tk.Label(
            box, text="✓", font=("Segoe UI", 42, "bold"),
            bg="#2563eb", fg="white", width=2
        ).pack(pady=(75, 18))

        tk.Label(
            box, text="TASKFLOW", font=("Segoe UI", 38, "bold"),
            bg="#172554", fg="white"
        ).pack()

        tk.Label(
            box, text="Organize. Prioritize. Complete.",
            font=("Segoe UI", 13), bg="#172554", fg="#bfdbfe"
        ).pack(pady=(8, 35))

        self.canvas = tk.Canvas(
            box, width=380, height=8,
            bg="#172554", highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.create_rectangle(
            0, 0, 380, 8, fill="#334e7d", outline=""
        )
        self.bar = self.canvas.create_rectangle(
            0, 0, 0, 8, fill="#60a5fa", outline=""
        )

        self.percent = tk.Label(
            box, text="0%", font=("Segoe UI", 10, "bold"),
            bg="#172554", fg="#bfdbfe"
        )
        self.percent.pack(pady=14)

        self.message = tk.Label(
            box, text="Starting TaskFlow...",
            font=("Segoe UI", 9), bg="#172554", fg="#94a3b8"
        )
        self.message.pack()

        self.animate()

    def animate(self):
        if self.progress <= 100:
            self.percent.config(text=f"{self.progress}%")
            self.canvas.coords(
                self.bar, 0, 0, 3.8 * self.progress, 8
            )

            if self.progress < 25:
                msg = "Starting TaskFlow..."
            elif self.progress < 50:
                msg = "Preparing interface..."
            elif self.progress < 75:
                msg = "Connecting to database..."
            elif self.progress < 100:
                msg = "Loading application..."
            else:
                msg = "Ready!"

            self.message.config(text=msg)
            self.progress += 2
            self.root.after(25, self.animate)
        else:
            self.root.after(350, self.finish)

    def finish(self):
        self.root.destroy()
        self.callback()
