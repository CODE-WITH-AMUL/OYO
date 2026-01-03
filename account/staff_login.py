import bcrypt
import json
import os
import tkinter as tk
from tkinter import messagebox


# ---------------------------
# Paths & storage
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
STAFF_FILE = os.path.join(DATA_DIR, "staff.json")

os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------
# Helpers
# ---------------------------
def load_staff():
    """Load stored staff credentials (if any)."""
    if os.path.exists(STAFF_FILE):
        with open(STAFF_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_staff(username, hashed_password):
    """Save staff username and hashed password."""
    with open(STAFF_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "username": username,
                "password": hashed_password.decode("utf-8"),
            },
            f,
            indent=4
        )


# ---------------------------
# Authentication logic
# ---------------------------
class LoginStaff:

    @staticmethod
    def authenticate(username_input: str, password_input: str):
        if not username_input or not password_input:
            return False, "Username and password are required"

        staff = load_staff()
        password_bytes = password_input.encode("utf-8")

        # First-time setup
        if not staff:
            hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
            save_staff(username_input, hashed_password)
            return True, "First-time setup complete!"

        if username_input != staff.get("username"):
            return False, "Invalid username"

        stored_hash_bytes = staff["password"].encode("utf-8")
        if bcrypt.checkpw(password_bytes, stored_hash_bytes):
            return True, "Login successful"
        else:
            return False, "Invalid password"


# ---------------------------
# Tkinter UI
# ---------------------------
class LoginUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HMS Staff Login")
        self.geometry("350x280")
        self.resizable(False, False)

        tk.Label(self, text="Staff Login", font=("Arial", 18)).pack(pady=15)

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(
            self,
            text="Login",
            bg="green",
            fg="white",
            width=15,
            command=self.login
        ).pack(pady=15)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        success, message = LoginStaff.authenticate(username, password)

        if success:
            messagebox.showinfo("Success", message)
            self.destroy()  # close login window
            # Here you can open Dashboard window
        else:
            messagebox.showerror("Login Failed", message)


# ---------------------------
# Run (CLI or GUI)
# ---------------------------
if __name__ == "__main__":
    # Comment ONE of the following depending on what you want

    # ---- GUI MODE ----
    app = LoginUI()
    app.mainloop()

    # ---- CLI MODE ----
    # print("=== Staff Login (Test) ===")
    # u = input("Username: ")
    # p = input("Password: ")
    # ok, msg = LoginStaff.authenticate(u, p)
    # print(msg)
