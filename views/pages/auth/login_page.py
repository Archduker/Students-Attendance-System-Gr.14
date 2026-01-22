import customtkinter as ctk

class LoginPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill="both")

        title = ctk.CTkLabel(
            self,
            text="Student Attendance System",
            font=("Segoe UI", 24, "bold")
        )
        title.pack(pady=30)

        self.username_entry = ctk.CTkEntry(
            self,
            placeholder_text="Username"
        )
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Password",
            show="*"
        )
        self.password_entry.pack(pady=10)

        login_btn = ctk.CTkButton(
            self,
            text="Login",
            command=self.login
        )
        login_btn.pack(pady=20)

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            text_color="red"
        )
        self.error_label.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        print("Username:", username)
        print("Password:", password)

        if not username or not password:
            self.error_label.configure(text="Please enter username and password")
        else:
            self.error_label.configure(text="Login clicked!")
