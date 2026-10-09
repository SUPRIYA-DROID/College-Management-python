"""
College Management System - Main Application
Powered by ProjectsHUB

A comprehensive college management system with modern GUI interface.
This is the main entry point for the application.
"""

from modules.dashboard.main_dashboard import MainDashboard
from modules.authentication.login import LoginSystem
from config.database import DatabaseManager
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent / "modules"))


class CollegeManagementApp:
    """Main Application Class for College Management System"""

    def __init__(self):
        self.root = tk.Tk()
        self.current_user = None
        self.db_manager = None

        # Initialize application
        self._setup_application()
        self._initialize_database()

    def _setup_application(self):
        """Configure main application window"""
        self.root.title("College Management System - ProjectsHUB")
        self.root.geometry("1200x700")
        self.root.minsize(800, 600)

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        # Custom color scheme
        self.root.configure(bg='#f0f0f0')

        # Center window on screen
        self._center_window()

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _center_window(self):
        """Center the application window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _initialize_database(self):
        """Initialize database connection"""
        try:
            self.db_manager = DatabaseManager()
            self.db_manager.initialize_database()
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Failed to initialize database:\n{str(e)}\n\nApplication will exit."
            )
            self.root.destroy()
            sys.exit(1)

    def _on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            if self.db_manager:
                self.db_manager.close_connection()
            self.root.destroy()

    def show_login(self):
        """Display login window"""
        # Clear main window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create login system
        login_system = LoginSystem(
            self.root, self.db_manager, self._on_login_success)

    def _on_login_success(self, user_data):
        """Handle successful login"""
        self.current_user = user_data
        self.show_dashboard()

    def show_dashboard(self):
        """Display main dashboard"""
        # Clear login window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create dashboard
        dashboard = MainDashboard(
            self.root,
            self.db_manager,
            self.current_user,
            self._on_logout
        )

    def _on_logout(self):
        """Handle user logout"""
        self.current_user = None
        self.show_login()

    def run(self):
        """Start the application"""
        self.show_login()
        self.root.mainloop()


def main():
    """Main function to start the application"""
    try:
        app = CollegeManagementApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        messagebox.showerror(
            "Fatal Error", f"Application encountered a fatal error:\n{e}")
    finally:
        print("College Management System closed")


if __name__ == "__main__":
    main()
