import sqlite3, tkinter as tk
from tkinter import messagebox

DB = "usuarios.db"

# Base de datos

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS usuarios (usuario TEXT UNIQUE, password TEXT)")
    c.execute("SELECT COUNT(*) FROM usuarios")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO usuarios VALUES ('admin','admin123'),('profe','profe123')")
    conn.commit()
    conn.close()


def check(u, p):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE usuario=? AND password=?", (u, p))
    r = c.fetchone() is not None
    conn.close()
    return r


class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("380x420")
        self.configure(bg="#F4F6FF")
        self.resizable(False, False)

        f = tk.Frame(self, bg="#F4F6FF", padx=30, pady=20)
        f.pack(fill="both", expand=True)

        # icono estilo power
        icon = tk.Canvas(f, width=200, height=200, bg="#F4F6FF", highlightthickness=0)
        icon.pack(pady=(0, 15))

        icon.create_oval(20, 20, 180, 180, outline="#0100FA", width=10, fill="#F4F6FF")
        icon.create_rectangle(90, 50, 110, 120, fill="#0100FA", outline="#0100FA")
        icon.create_arc(40, 40, 160, 160, start=200, extent=120, fill="", outline="#0100FA", width=12, style="arc")

        tk.Label(f, text="Iniciar sesión", font=("Arial", 20, "bold"), fg="#0100FA", bg="#F4F6FF").pack(pady=(0, 15))

        card = tk.Frame(f, bg="white", padx=20, pady=20)
        card.pack(fill="x")

        tk.Label(card, text="Usuario", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 3))
        self.u = tk.Entry(card, font=("Arial", 11), bg="#F7F8FF")
        self.u.pack(fill="x", pady=(0, 12))

        tk.Label(card, text="Contraseña", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 3))
        self.p = tk.Entry(card, font=("Arial", 11), bg="#F7F8FF", show="*")
        self.p.pack(fill="x", pady=(0, 15))

        tk.Button(card, text="Entrar", bg="#0100FA", fg="white", font=("Arial", 11, "bold"), bd=0, pady=8, command=self.login).pack(fill="x")

        self.u.bind("<Return>", lambda e: self.login())
        self.p.bind("<Return>", lambda e: self.login())

    def login(self):
        u, p = self.u.get().strip(), self.p.get().strip()
        if not u or not p:
            messagebox.showwarning("Error", "Completa los campos")
            return
        if check(u, p):
            self.destroy()
            Welcome(u).mainloop()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")


class Welcome(tk.Tk):
    def __init__(self, u):
        super().__init__()
        self.title("Bienvenido")
        self.geometry("350x250")
        self.configure(bg="#F4F6FF")
        self.resizable(False, False)

        f = tk.Frame(self, bg="#F4F6FF", padx=30, pady=30)
        f.pack(fill="both", expand=True)

        tk.Label(f, text=f"¡Bienvenido, {u}!", font=("Arial", 20, "bold"), fg="#0100FA", bg="#F4F6FF").pack(pady=20)
        tk.Label(f, text="Sesión iniciada correctamente", font=("Arial", 12), fg="#1B1B1B", bg="#F4F6FF").pack(pady=10)
        tk.Button(f, text="Cerrar sesión", bg="#0100FA", fg="white", font=("Arial", 10, "bold"), bd=0, pady=8, command=lambda: self.destroy() or Login().mainloop()).pack(pady=20)


if __name__ == "__main__":
    init_db()
    Login().mainloop()
