from core.database import DatabaseHandler
from core.auth import AuthService
from ui.screens import LoginScreen, RegisterScreen, MainScreen
import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Financeiro")
        self.geometry("1280x720")
        self.iconbitmap("assets/icon.ico")

        self.db = DatabaseHandler()
        self.auth = AuthService(self.db)

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.screens = {
            "login": LoginScreen(self.container, self),
            "register": RegisterScreen(self.container, self),
            "main": MainScreen(self.container, self)
        }

        self.show_screen("login")

    def show_screen(self, name):
        for screen in self.screens.values():
            screen.pack_forget()
        self.screens[name].pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
