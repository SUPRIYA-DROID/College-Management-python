"""
Login System Module
College Management System - ProjectsHUB

Handles user authentication and login functionality.
"""

from config.settings import COLORS, FONTS, BUTTON_STYLE
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from datetime import datetime
import sys
from pathlib import Path

# Add config to path
sys.path.append(str(Path(__file__).parent.parent.parent))


class LoginSystem:
    """Modern Login System with enhanced UI and security"""

    def __init__(self, parent, db_manager, on_success_callback):
        self.parent = parent
        self.db_manager = db_manager
        self.on_success_callback = on_success_callback
        self.login_attempts = 0
        self.max_attempts = 3

        self.setup_ui()

    def setup_ui(self):
        """Create modern login interface"""
        # Main container
        self.main_frame = tk.Frame(self.parent, bg=COLORS['background'])
        self.main_frame.pack(fill='both', expand=True)

        # Center container
        self.center_frame = tk.Frame(
            self.main_frame, bg=COLORS['surface'], relief='solid', bd=1)
        self.center_frame.place(
            relx=0.5, rely=0.5, anchor='center', width=450, height=500)

        # Add shadow effect
        shadow_frame = tk.Frame(self.main_frame, bg='#CCCCCC')
        shadow_frame.place(relx=0.5, rely=0.5,
                           anchor='center', width=454, height=504)
        self.center_frame.lift()

        # Header section
        self.create_header()

        # Login form section
        self.create_login_form()

        # Footer section
        self.create_footer()

        # Bind Enter key to login
        self.parent.bind('<Return>', lambda event: self.attempt_login())

    def create_header(self):
        """Create header section with title and branding"""
        header_frame = tk.Frame(
            self.center_frame, bg=COLORS['primary'], height=120)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Title
        title_label = tk.Label(
            header_frame,
            text="College Management System",
            font=FONTS['title'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary']
        )
        title_label.pack(pady=(20, 5))

        # Powered by ProjectsHUB
        subtitle_label = tk.Label(
            header_frame,
            text="Powered by ProjectsHUB",
            font=FONTS['small'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary']
        )
        subtitle_label.pack()

        # Welcome message
        welcome_label = tk.Label(
            header_frame,
            text="Welcome! Please sign in to continue",
            font=FONTS['body'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary']
        )
        welcome_label.pack(pady=(10, 0))

    def create_login_form(self):
        """Create login form with username and password fields"""
        form_frame = tk.Frame(self.center_frame, bg=COLORS['surface'])
        form_frame.pack(fill='both', expand=True, padx=40, pady=40)

        # Username field
        username_label = tk.Label(
            form_frame,
            text="Username:",
            font=FONTS['subheading'],
            bg=COLORS['surface'],
            fg=COLORS['on_surface']
        )
        username_label.pack(anchor='w', pady=(0, 5))

        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(
            form_frame,
            textvariable=self.username_var,
            font=FONTS['body'],
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightcolor=COLORS['primary']
        )
        self.username_entry.pack(fill='x', pady=(0, 20), ipady=8)

        # Password field
        password_label = tk.Label(
            form_frame,
            text="Password:",
            font=FONTS['subheading'],
            bg=COLORS['surface'],
            fg=COLORS['on_surface']
        )
        password_label.pack(anchor='w', pady=(0, 5))

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            form_frame,
            textvariable=self.password_var,
            font=FONTS['body'],
            show='*',
            relief='solid',
            bd=1,
            highlightthickness=2,
            highlightcolor=COLORS['primary']
        )
        self.password_entry.pack(fill='x', pady=(0, 30), ipady=8)

        # Login button
        self.login_button = tk.Button(
            form_frame,
            text="Sign In",
            command=self.attempt_login,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            activebackground=COLORS['secondary'],
            activeforeground=COLORS['on_secondary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2'
        )
        self.login_button.pack(fill='x', pady=(0, 15))

        # Status label for error messages
        self.status_label = tk.Label(
            form_frame,
            text="",
            font=FONTS['small'],
            bg=COLORS['surface'],
            fg=COLORS['danger']
        )
        self.status_label.pack()

        # Set focus to username field
        self.username_entry.focus()

    def create_footer(self):
        """Create footer section with additional information"""
        footer_frame = tk.Frame(
            self.center_frame, bg=COLORS['light'], height=60)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)

        # Default credentials info
        info_label = tk.Label(
            footer_frame,
            text="Default Login: admin / admin",
            font=FONTS['small'],
            bg=COLORS['light'],
            fg=COLORS['on_surface']
        )
        info_label.pack(pady=20)

    def attempt_login(self):
        """Handle login attempt"""
        username = self.username_var.get().strip()
        password = self.password_var.get()

        # Validate input
        if not username or not password:
            self.show_error("Please enter both username and password")
            return

        # Check maximum attempts
        if self.login_attempts >= self.max_attempts:
            self.show_error(
                "Maximum login attempts exceeded. Please restart the application.")
            self.login_button.configure(state='disabled')
            return

        # Authenticate user
        if self.authenticate_user(username, password):
            self.on_login_success(username)
        else:
            self.login_attempts += 1
            remaining = self.max_attempts - self.login_attempts
            if remaining > 0:
                self.show_error(
                    f"Invalid credentials. {remaining} attempts remaining.")
            else:
                self.show_error("Maximum login attempts exceeded.")
                self.login_button.configure(state='disabled')

    def authenticate_user(self, username, password):
        """Authenticate user credentials against database"""
        try:
            cursor = self.db_manager.execute_query(
                "SELECT user_id, username, password_hash, full_name, email, role FROM users WHERE username = ?",
                (username,)
            )
            user = cursor.fetchone()

            if user and self.db_manager.verify_password(password, user['password_hash']):
                # Update last login
                self.db_manager.execute_and_commit(
                    "UPDATE users SET last_login = ? WHERE user_id = ?",
                    (datetime.now().isoformat(), user['user_id'])
                )
                self.user_data = dict(user)
                return True
            return False

        except Exception as e:
            self.show_error(f"Authentication error: {str(e)}")
            return False

    def on_login_success(self, username):
        """Handle successful login"""
        self.show_success("Login successful! Loading dashboard...")
        self.parent.after(
            1000, lambda: self.on_success_callback(self.user_data))

    def show_error(self, message):
        """Display error message"""
        self.status_label.configure(text=message, fg=COLORS['danger'])

    def show_success(self, message):
        """Display success message"""
        self.status_label.configure(text=message, fg=COLORS['success'])

    def reset_form(self):
        """Reset login form"""
        self.username_var.set("")
        self.password_var.set("")
        self.status_label.configure(text="")
        self.login_attempts = 0
        self.login_button.configure(state='normal')
        self.username_entry.focus()
