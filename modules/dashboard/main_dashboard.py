"""
Main Dashboard Module
College Management System - ProjectsHUB

Main dashboard interface with navigation to all system modules.
"""

from config.settings import COLORS, FONTS, BUTTON_STYLE
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
from pathlib import Path

# Add config to path
sys.path.append(str(Path(__file__).parent.parent.parent))


class MainDashboard:
    """Modern Main Dashboard with navigation and system overview"""

    def __init__(self, parent, db_manager, user_data, on_logout_callback):
        self.parent = parent
        self.db_manager = db_manager
        self.user_data = user_data
        self.on_logout_callback = on_logout_callback

        self.setup_ui()
        self.load_dashboard_data()

    def setup_ui(self):
        """Create modern dashboard interface"""
        # Main container
        self.main_frame = tk.Frame(self.parent, bg=COLORS['background'])
        self.main_frame.pack(fill='both', expand=True)

        # Header
        self.create_header()

        # Navigation sidebar
        self.create_sidebar()

        # Content area
        self.create_content_area()

    def create_header(self):
        """Create header with title and user info"""
        header_frame = tk.Frame(
            self.main_frame, bg=COLORS['primary'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Left side - Title
        title_frame = tk.Frame(header_frame, bg=COLORS['primary'])
        title_frame.pack(side='left', fill='y', padx=20)

        title_label = tk.Label(
            title_frame,
            text="College Management System",
            font=FONTS['title'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary']
        )
        title_label.pack(anchor='w', pady=(15, 0))

        subtitle_label = tk.Label(
            title_frame,
            text="Powered by ProjectsHUB",
            font=FONTS['small'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary']
        )
        subtitle_label.pack(anchor='w')

        # Right side - User info and logout
        user_frame = tk.Frame(header_frame, bg=COLORS['primary'])
        user_frame.pack(side='right', fill='y', padx=20)

        welcome_label = tk.Label(
            user_frame,
            text=f"Welcome, {self.user_data['full_name']}",
            font=FONTS['subheading'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary']
        )
        welcome_label.pack(side='top', anchor='e', pady=(10, 0))

        logout_button = tk.Button(
            user_frame,
            text="Logout",
            command=self.confirm_logout,
            font=FONTS['body'],
            bg=COLORS['secondary'],
            fg=COLORS['on_secondary'],
            activebackground=COLORS['danger'],
            relief='flat',
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        logout_button.pack(side='top', anchor='e', pady=(5, 10))

    def create_sidebar(self):
        """Create navigation sidebar"""
        self.sidebar_frame = tk.Frame(
            self.main_frame, bg=COLORS['dark'], width=250)
        self.sidebar_frame.pack(side='left', fill='y')
        self.sidebar_frame.pack_propagate(False)

        # Navigation buttons
        nav_buttons = [
            ("Dashboard", "dashboard", self.show_dashboard),
            ("Student Management", "students", self.show_student_management),
            ("Library System", "library", self.show_library_system),
            ("Fee Management", "fees", self.show_fee_management),
            ("Academic Records", "academics", self.show_academic_records),
            ("Reports", "reports", self.show_reports),
            ("Settings", "settings", self.show_settings),
        ]

        for text, key, command in nav_buttons:
            button = tk.Button(
                self.sidebar_frame,
                text=text,
                command=command,
                font=FONTS['menu'],
                bg=COLORS['dark'],
                fg=COLORS['light'],
                activebackground=COLORS['primary'],
                activeforeground=COLORS['on_primary'],
                relief='flat',
                bd=0,
                anchor='w',
                padx=20,
                pady=15,
                cursor='hand2'
            )
            button.pack(fill='x', pady=1)

            # Store button reference for highlighting
            setattr(self, f"{key}_button", button)

        # Highlight dashboard button initially
        self.dashboard_button.configure(
            bg=COLORS['primary'], fg=COLORS['on_primary'])

    def create_content_area(self):
        """Create main content area"""
        self.content_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        self.content_frame.pack(side='right', fill='both', expand=True)

        # Show dashboard by default
        self.show_dashboard()

    def clear_content(self):
        """Clear content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def highlight_nav_button(self, active_button):
        """Highlight active navigation button"""
        nav_buttons = [
            self.dashboard_button, self.students_button, self.library_button,
            self.fees_button, self.academics_button, self.reports_button,
            self.settings_button
        ]

        for button in nav_buttons:
            if button == active_button:
                button.configure(bg=COLORS['primary'], fg=COLORS['on_primary'])
            else:
                button.configure(bg=COLORS['dark'], fg=COLORS['light'])

    def show_dashboard(self):
        """Show dashboard overview"""
        self.clear_content()
        self.highlight_nav_button(self.dashboard_button)

        # Dashboard title
        title_label = tk.Label(
            self.content_frame,
            text="Dashboard Overview",
            font=FONTS['title'],
            bg=COLORS['background'],
            fg=COLORS['on_background']
        )
        title_label.pack(pady=20)

        # Statistics cards
        stats_frame = tk.Frame(self.content_frame, bg=COLORS['background'])
        stats_frame.pack(fill='x', padx=20, pady=10)

        # Create statistics cards
        self.create_stats_cards(stats_frame)

        # Quick actions
        actions_frame = tk.Frame(self.content_frame, bg=COLORS['background'])
        actions_frame.pack(fill='x', padx=20, pady=20)

        actions_label = tk.Label(
            actions_frame,
            text="Quick Actions",
            font=FONTS['heading'],
            bg=COLORS['background'],
            fg=COLORS['on_background']
        )
        actions_label.pack(anchor='w', pady=(0, 10))

        # Quick action buttons
        buttons_frame = tk.Frame(actions_frame, bg=COLORS['background'])
        buttons_frame.pack(fill='x')

        quick_actions = [
            ("Add New Student", self.show_student_management),
            ("Issue Book", self.show_library_system),
            ("Record Payment", self.show_fee_management),
            ("Add Marks", self.show_academic_records)
        ]

        for i, (text, command) in enumerate(quick_actions):
            button = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                font=FONTS['button'],
                bg=COLORS['accent'],
                fg=COLORS['on_primary'],
                activebackground=COLORS['primary'],
                relief='flat',
                bd=0,
                padx=20,
                pady=10,
                cursor='hand2'
            )
            button.grid(row=i//2, column=i % 2, padx=10, pady=5, sticky='ew')

        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

    def create_stats_cards(self, parent):
        """Create statistics cards for dashboard"""
        try:
            # Get statistics from database
            stats = self.get_dashboard_statistics()

            cards_data = [
                ("Total Students", stats['total_students'], COLORS['primary']),
                ("Active Students",
                 stats['active_students'], COLORS['success']),
                ("Total Books", stats['total_books'], COLORS['secondary']),
                ("Issued Books", stats['issued_books'], COLORS['warning'])
            ]

            for i, (title, value, color) in enumerate(cards_data):
                card_frame = tk.Frame(parent, bg=color, relief='solid', bd=1)
                card_frame.grid(row=0, column=i, padx=10, pady=5, sticky='ew')

                title_label = tk.Label(
                    card_frame,
                    text=title,
                    font=FONTS['body'],
                    bg=color,
                    fg=COLORS['on_primary']
                )
                title_label.pack(pady=(15, 5))

                value_label = tk.Label(
                    card_frame,
                    text=str(value),
                    font=FONTS['title'],
                    bg=color,
                    fg=COLORS['on_primary']
                )
                value_label.pack(pady=(0, 15))

            # Configure grid weights
            for i in range(4):
                parent.grid_columnconfigure(i, weight=1)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to load dashboard statistics: {str(e)}")

    def get_dashboard_statistics(self):
        """Get statistics for dashboard"""
        stats = {}

        # Total students
        cursor = self.db_manager.execute_query("SELECT COUNT(*) FROM students")
        stats['total_students'] = cursor.fetchone()[0]

        # Active students
        cursor = self.db_manager.execute_query(
            "SELECT COUNT(*) FROM students WHERE status = 'active'")
        stats['active_students'] = cursor.fetchone()[0]

        # Total books
        cursor = self.db_manager.execute_query(
            "SELECT COUNT(*) FROM library_books")
        stats['total_books'] = cursor.fetchone()[0]

        # Issued books
        cursor = self.db_manager.execute_query(
            "SELECT COUNT(*) FROM library_transactions WHERE status = 'issued'")
        stats['issued_books'] = cursor.fetchone()[0]

        return stats

    def show_student_management(self):
        """Show student management module"""
        self.clear_content()
        self.highlight_nav_button(self.students_button)

        try:
            # Import and create student management system
            sys.path.append(str(Path(__file__).parent.parent))
            from student_management.student_system import StudentManagement

            student_system = StudentManagement(
                self.content_frame, self.db_manager)

        except Exception as e:
            placeholder = tk.Label(
                self.content_frame,
                text=f"Error loading Student Management:\n{str(e)}",
                font=FONTS['heading'],
                bg=COLORS['background'],
                fg=COLORS['danger']
            )
            placeholder.pack(expand=True)

    def show_library_system(self):
        """Show library management module"""
        self.clear_content()
        self.highlight_nav_button(self.library_button)

        try:
            # Import and create library management system
            sys.path.append(str(Path(__file__).parent.parent))
            from library_system.library_management import LibrarySystem

            library_system = LibrarySystem(
                self.content_frame, self.db_manager)

        except Exception as e:
            placeholder = tk.Label(
                self.content_frame,
                text=f"Error loading Library Management:\n{str(e)}",
                font=FONTS['heading'],
                bg=COLORS['background'],
                fg=COLORS['danger']
            )
            placeholder.pack(expand=True)

    def show_fee_management(self):
        """Show fee management module"""
        self.clear_content()
        self.highlight_nav_button(self.fees_button)

        try:
            # Import and create fee management system
            sys.path.append(str(Path(__file__).parent.parent))
            from fee_management.fee_system import FeeSystem

            fee_system = FeeSystem(
                self.content_frame, self.db_manager)

        except Exception as e:
            placeholder = tk.Label(
                self.content_frame,
                text=f"Error loading Fee Management:\n{str(e)}",
                font=FONTS['heading'],
                bg=COLORS['background'],
                fg=COLORS['danger']
            )
            placeholder.pack(expand=True)

    def show_academic_records(self):
        """Show academic records module"""
        self.clear_content()
        self.highlight_nav_button(self.academics_button)

        try:
            # Import and create academic records system
            sys.path.append(str(Path(__file__).parent.parent))
            from academic_records.marksheet_system import MarksheetSystem

            marksheet_system = MarksheetSystem(
                self.content_frame, self.db_manager)

        except Exception as e:
            placeholder = tk.Label(
                self.content_frame,
                text=f"Error loading Academic Records:\n{str(e)}",
                font=FONTS['heading'],
                bg=COLORS['background'],
                fg=COLORS['danger']
            )
            placeholder.pack(expand=True)

    def show_reports(self):
        """Show reports module"""
        self.clear_content()
        self.highlight_nav_button(self.reports_button)

        try:
            # Import and create reports system
            sys.path.append(str(Path(__file__).parent.parent))
            from reports.reports_system import ReportsSystem

            reports_system = ReportsSystem(
                self.content_frame, self.db_manager)

        except Exception as e:
            placeholder = tk.Label(
                self.content_frame,
                text=f"Error loading Reports System:\n{str(e)}",
                font=FONTS['heading'],
                bg=COLORS['background'],
                fg=COLORS['danger']
            )
            placeholder.pack(expand=True)

    def show_settings(self):
        """Show settings module"""
        self.clear_content()
        self.highlight_nav_button(self.settings_button)

        try:
            # Import and create settings system
            sys.path.append(str(Path(__file__).parent.parent))
            from settings.settings_system import SettingsSystem

            settings_system = SettingsSystem(
                self.content_frame, self.db_manager)

        except Exception as e:
            placeholder = tk.Label(
                self.content_frame,
                text=f"Error loading Settings System:\n{str(e)}",
                font=FONTS['heading'],
                bg=COLORS['background'],
                fg=COLORS['danger']
            )
            placeholder.pack(expand=True)

    def load_dashboard_data(self):
        """Load dashboard data"""
        # This method will be expanded to load real-time data
        pass

    def confirm_logout(self):
        """Confirm logout action"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.on_logout_callback()
