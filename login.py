import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# -----------------------------
# Base de datos
# -----------------------------
DB_NAME = "usuarios.db"

def crear_tabla():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # Insertar usuarios por defecto si no existen
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (?, ?)", ("admin", "admin123"))
        cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (?, ?)", ("profe", "profe123"))
    
    conn.commit()
    conn.close()

def validar_usuario(usuario, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ? AND password = ?", (usuario, password))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

# -----------------------------
# Ventana Login
# -----------------------------
class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inicio de sesión")
        self.geometry("420x420")
        self.configure(bg="#F4F6FF")
        self.resizable(False, False)

        # Color principal
        self.primary = "#0100FA"
        self.primary_dark = "#0000C7"
        self.bg = "#F4F6FF"
        self.card = "#FFFFFF"
        self.text = "#1B1B1B"

        self.crear_ui()

    def crear_ui(self):
        # Contenedor principal
        container = tk.Frame(self, bg=self.bg, padx=30, pady=30)
        container.pack(fill="both", expand=True)

        # Logo / título
        title = tk.Label(
            container,
            text="Iniciar sesión",
            bg=self.bg,
            fg=self.primary,
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(10, 25))

        # Tarjeta del formulario
        card = tk.Frame(container, bg=self.card, padx=25, pady=25, bd=0)
        card.pack(fill="x", ipady=8)

        # Usuario
        tk.Label(card, text="Usuario", bg=self.card, fg=self.text, font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        self.usuario_entry = tk.Entry(
            card,
            font=("Arial", 12),
            bd=1,
            relief="solid",
            bg="#F7F8FF"
        )
        self.usuario_entry.pack(fill="x", pady=(0, 15))

        # Contraseña
        tk.Label(card, text="Contraseña", bg=self.card, fg=self.text, font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 5))
        self.password_entry = tk.Entry(
            card,
            font=("Arial", 12),
            bd=1,
            relief="solid",
            bg="#F7F8FF",
            show="*"
        )
        self.password_entry.pack(fill="x", pady=(0, 20))

        # Botón login
        btn_login = tk.Button(
            card,
            text="Entrar",
            bg=self.primary,
            fg="white",
            font=("Arial", 12, "bold"),
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.login
        )
        btn_login.pack(fill="x")

        # Enter en campos
        self.usuario_entry.bind("<Return>", lambda event: self.login())
        self.password_entry.bind("<Return>", lambda event: self.login())

    def login(self):
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Campos vacíos", "Debes completar usuario y contraseña.")
            return

        if validar_usuario(usuario, password):
            self.destroy()
            PantallaLogueado(usuario).mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# -----------------------------
# Ventana logueado
# -----------------------------
class PantallaLogueado(tk.Tk):
    def __init__(self, usuario):
        super().__init__()
        self.title("Bienvenido")
        self.geometry("450x300")
        self.configure(bg="#F4F6FF")
        self.resizable(False, False)

        container = tk.Frame(self, bg="#F4F6FF", padx=30, pady=30)
        container.pack(fill="both", expand=True)

        lbl = tk.Label(
            container,
            text=f"¡Bienvenido, {usuario}!",
            bg="#F4F6FF",
            fg="#0100FA",
            font=("Arial", 24, "bold")
        )
        lbl.pack(pady=(30, 20))

        lbl2 = tk.Label(
            container,
            text="Has iniciado sesión correctamente.",
            bg="#F4F6FF",
            fg="#1B1B1B",
            font=("Arial", 14)
        )
        lbl2.pack(pady=10)

        btn = tk.Button(
            container,
            text="Cerrar sesión",
            bg="#0100FA",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.cerrar_sesion
        )
        btn.pack(pady=25)

    def cerrar_sesion(self):
        self.destroy()
        app = LoginApp()
        app.mainloop()

# -----------------------------
# Inicio
# -----------------------------
if __name__ == "__main__":
    crear_tabla()
    app = LoginApp()
    app.mainloop()
