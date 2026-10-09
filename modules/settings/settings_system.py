"""
Settings System
College Management System - ProjectsHUB

Simple but comprehensive system configuration and user management.
"""

from utils.validators import validate_email, validate_phone
from config.settings import COLORS, FONTS
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
import json
import os
import sys
from pathlib import Path

# Add config to path
sys.path.append(str(Path(__file__).parent.parent.parent))


class SettingsSystem:
    """Simple Settings and Configuration System"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager

        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        """Create settings interface"""
        # Main container
        self.main_frame = tk.Frame(self.parent, bg=COLORS['background'])
        self.main_frame.pack(fill='both', expand=True)

        # Header
        self.create_header()

        # Content with tabs
        self.create_tabs()

    def create_header(self):
        """Create header section"""
        header_frame = tk.Frame(
            self.main_frame, bg=COLORS['surface'], height=60)
        header_frame.pack(fill='x', padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="System Settings",
            font=FONTS['title'],
            bg=COLORS['surface'],
            fg=COLORS['on_surface']
        )
        title_label.pack(side='left', pady=15)

    def create_tabs(self):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)

        # General settings tab
        self.general_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.general_frame, text="General Settings")
        self.create_general_settings_tab()

        # User management tab
        self.users_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.users_frame, text="User Management")
        self.create_user_management_tab()

        # College info tab
        self.college_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.college_frame, text="College Information")
        self.create_college_info_tab()

        # Backup & restore tab
        self.backup_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.backup_frame, text="Backup & Restore")
        self.create_backup_tab()

    def create_general_settings_tab(self):
        """Create general settings tab"""
        # Application settings
        app_settings_frame = tk.LabelFrame(
            self.general_frame, text="Application Settings", font=FONTS['subheading'])
        app_settings_frame.pack(fill='x', padx=10, pady=10)

        settings_form = tk.Frame(app_settings_frame)
        settings_form.pack(padx=20, pady=20)

        # Auto-save interval
        tk.Label(settings_form, text="Auto-save interval (minutes):",
                 font=FONTS['body']).grid(row=0, column=0, sticky='w', pady=5)
        self.auto_save_var = tk.StringVar(value="5")
        auto_save_entry = tk.Entry(
            settings_form, textvariable=self.auto_save_var, font=FONTS['body'], width=10)
        auto_save_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # Session timeout
        tk.Label(settings_form, text="Session timeout (minutes):",
                 font=FONTS['body']).grid(row=1, column=0, sticky='w', pady=5)
        self.session_timeout_var = tk.StringVar(value="30")
        timeout_entry = tk.Entry(
            settings_form, textvariable=self.session_timeout_var, font=FONTS['body'], width=10)
        timeout_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Default semester
        tk.Label(settings_form, text="Default semester:", font=FONTS['body']).grid(
            row=2, column=0, sticky='w', pady=5)
        self.default_semester_var = tk.StringVar(value="1")
        semester_combo = ttk.Combobox(settings_form, textvariable=self.default_semester_var,
                                      values=["1", "2", "3", "4", "5", "6", "7", "8"], width=8)
        semester_combo.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Theme settings
        theme_frame = tk.LabelFrame(
            self.general_frame, text="Appearance Settings", font=FONTS['subheading'])
        theme_frame.pack(fill='x', padx=10, pady=10)

        theme_form = tk.Frame(theme_frame)
        theme_form.pack(padx=20, pady=20)

        # Font size
        tk.Label(theme_form, text="Font size:", font=FONTS['body']).grid(
            row=0, column=0, sticky='w', pady=5)
        self.font_size_var = tk.StringVar(value="12")
        font_size_combo = ttk.Combobox(theme_form, textvariable=self.font_size_var,
                                       values=["10", "11", "12", "13", "14", "16"], width=8)
        font_size_combo.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # Window size
        tk.Label(theme_form, text="Default window size:", font=FONTS['body']).grid(
            row=1, column=0, sticky='w', pady=5)
        self.window_size_var = tk.StringVar(value="1024x768")
        window_size_combo = ttk.Combobox(theme_form, textvariable=self.window_size_var,
                                         values=["800x600", "1024x768", "1280x720", "1366x768", "1920x1080"], width=12)
        window_size_combo.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Save general settings button
        save_general_btn = tk.Button(
            self.general_frame,
            text="Save General Settings",
            command=self.save_general_settings,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            padx=20, pady=10
        )
        save_general_btn.pack(pady=20)

    def create_user_management_tab(self):
        """Create user management tab"""
        # Current users display
        users_list_frame = tk.LabelFrame(
            self.users_frame, text="Current Users", font=FONTS['subheading'])
        users_list_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Users treeview
        users_tree_frame = tk.Frame(users_list_frame)
        users_tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.users_tree = ttk.Treeview(users_tree_frame, columns=(
            'username', 'role', 'created'), show='headings')
        self.users_tree.heading('username', text='Username')
        self.users_tree.heading('role', text='Role')
        self.users_tree.heading('created', text='Created Date')

        self.users_tree.column('username', width=150)
        self.users_tree.column('role', width=100)
        self.users_tree.column('created', width=120)

        users_scrollbar = ttk.Scrollbar(
            users_tree_frame, orient='vertical', command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=users_scrollbar.set)

        self.users_tree.pack(side='left', fill='both', expand=True)
        users_scrollbar.pack(side='right', fill='y')

        # User management buttons
        user_buttons_frame = tk.Frame(users_list_frame)
        user_buttons_frame.pack(fill='x', padx=10, pady=10)

        add_user_btn = tk.Button(
            user_buttons_frame,
            text="Add User",
            command=self.add_user,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            padx=15, pady=8
        )
        add_user_btn.pack(side='left', padx=5)

        edit_user_btn = tk.Button(
            user_buttons_frame,
            text="Edit User",
            command=self.edit_user,
            font=FONTS['button'],
            bg=COLORS['accent'],
            fg=COLORS['on_primary'],
            padx=15, pady=8
        )
        edit_user_btn.pack(side='left', padx=5)

        delete_user_btn = tk.Button(
            user_buttons_frame,
            text="Delete User",
            command=self.delete_user,
            font=FONTS['button'],
            bg=COLORS['danger'],
            fg=COLORS['on_primary'],
            padx=15, pady=8
        )
        delete_user_btn.pack(side='left', padx=5)

        refresh_users_btn = tk.Button(
            user_buttons_frame,
            text="Refresh",
            command=self.refresh_users,
            font=FONTS['button'],
            bg=COLORS['secondary'],
            fg=COLORS['on_primary'],
            padx=15, pady=8
        )
        refresh_users_btn.pack(side='right', padx=5)

        self.refresh_users()

    def create_college_info_tab(self):
        """Create college information tab"""
        # College details form
        college_frame = tk.LabelFrame(
            self.college_frame, text="College Information", font=FONTS['subheading'])
        college_frame.pack(fill='x', padx=10, pady=10)

        form_frame = tk.Frame(college_frame)
        form_frame.pack(padx=20, pady=20)

        # College name
        tk.Label(form_frame, text="College Name:", font=FONTS['body']).grid(
            row=0, column=0, sticky='w', pady=5)
        self.college_name_var = tk.StringVar(value="Sample College")
        college_name_entry = tk.Entry(
            form_frame, textvariable=self.college_name_var, font=FONTS['body'], width=40)
        college_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # College address
        tk.Label(form_frame, text="Address:", font=FONTS['body']).grid(
            row=1, column=0, sticky='w', pady=5)
        self.college_address_var = tk.StringVar(value="College Address")
        college_address_entry = tk.Entry(
            form_frame, textvariable=self.college_address_var, font=FONTS['body'], width=40)
        college_address_entry.grid(
            row=1, column=1, padx=10, pady=5, sticky='w')

        # College phone
        tk.Label(form_frame, text="Phone:", font=FONTS['body']).grid(
            row=2, column=0, sticky='w', pady=5)
        self.college_phone_var = tk.StringVar(value="")
        college_phone_entry = tk.Entry(
            form_frame, textvariable=self.college_phone_var, font=FONTS['body'], width=20)
        college_phone_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # College email
        tk.Label(form_frame, text="Email:", font=FONTS['body']).grid(
            row=3, column=0, sticky='w', pady=5)
        self.college_email_var = tk.StringVar(value="")
        college_email_entry = tk.Entry(
            form_frame, textvariable=self.college_email_var, font=FONTS['body'], width=40)
        college_email_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        # College website
        tk.Label(form_frame, text="Website:", font=FONTS['body']).grid(
            row=4, column=0, sticky='w', pady=5)
        self.college_website_var = tk.StringVar(value="")
        college_website_entry = tk.Entry(
            form_frame, textvariable=self.college_website_var, font=FONTS['body'], width=40)
        college_website_entry.grid(
            row=4, column=1, padx=10, pady=5, sticky='w')

        # Academic year settings
        academic_frame = tk.LabelFrame(
            self.college_frame, text="Academic Settings", font=FONTS['subheading'])
        academic_frame.pack(fill='x', padx=10, pady=10)

        academic_form = tk.Frame(academic_frame)
        academic_form.pack(padx=20, pady=20)

        # Current academic year
        tk.Label(academic_form, text="Current Academic Year:",
                 font=FONTS['body']).grid(row=0, column=0, sticky='w', pady=5)
        self.academic_year_var = tk.StringVar(value="2024-25")
        academic_year_entry = tk.Entry(
            academic_form, textvariable=self.academic_year_var, font=FONTS['body'], width=15)
        academic_year_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # Grading system
        tk.Label(academic_form, text="Grading System:", font=FONTS['body']).grid(
            row=1, column=0, sticky='w', pady=5)
        self.grading_system_var = tk.StringVar(value="Letter Grade")
        grading_combo = ttk.Combobox(academic_form, textvariable=self.grading_system_var,
                                     values=["Letter Grade", "Percentage", "GPA"], width=15)
        grading_combo.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Save college info button
        save_college_btn = tk.Button(
            self.college_frame,
            text="Save College Information",
            command=self.save_college_info,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            padx=20, pady=10
        )
        save_college_btn.pack(pady=20)

    def create_backup_tab(self):
        """Create backup and restore tab"""
        # Database backup section
        backup_frame = tk.LabelFrame(
            self.backup_frame, text="Database Backup", font=FONTS['subheading'])
        backup_frame.pack(fill='x', padx=10, pady=10)

        backup_info = tk.Label(
            backup_frame,
            text="Create a backup of your database to protect your data.",
            font=FONTS['body'],
            wraplength=400,
            justify='left'
        )
        backup_info.pack(padx=20, pady=10)

        backup_buttons = tk.Frame(backup_frame)
        backup_buttons.pack(padx=20, pady=10)

        create_backup_btn = tk.Button(
            backup_buttons,
            text="Create Backup",
            command=self.create_backup,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            padx=20, pady=10
        )
        create_backup_btn.pack(side='left', padx=5)

        schedule_backup_btn = tk.Button(
            backup_buttons,
            text="Schedule Backup",
            command=self.schedule_backup,
            font=FONTS['button'],
            bg=COLORS['secondary'],
            fg=COLORS['on_primary'],
            padx=20, pady=10
        )
        schedule_backup_btn.pack(side='left', padx=5)

        # Database restore section
        restore_frame = tk.LabelFrame(
            self.backup_frame, text="Database Restore", font=FONTS['subheading'])
        restore_frame.pack(fill='x', padx=10, pady=10)

        restore_info = tk.Label(
            restore_frame,
            text="Restore your database from a previous backup. WARNING: This will overwrite current data.",
            font=FONTS['body'],
            wraplength=400,
            justify='left',
            fg=COLORS['danger']
        )
        restore_info.pack(padx=20, pady=10)

        restore_backup_btn = tk.Button(
            restore_frame,
            text="Restore from Backup",
            command=self.restore_backup,
            font=FONTS['button'],
            bg=COLORS['warning'],
            fg=COLORS['on_primary'],
            padx=20, pady=10
        )
        restore_backup_btn.pack(padx=20, pady=10)

        # System maintenance section
        maintenance_frame = tk.LabelFrame(
            self.backup_frame, text="System Maintenance", font=FONTS['subheading'])
        maintenance_frame.pack(fill='x', padx=10, pady=10)

        maintenance_buttons = tk.Frame(maintenance_frame)
        maintenance_buttons.pack(padx=20, pady=20)

        optimize_btn = tk.Button(
            maintenance_buttons,
            text="Optimize Database",
            command=self.optimize_database,
            font=FONTS['button'],
            bg=COLORS['accent'],
            fg=COLORS['on_primary'],
            padx=15, pady=8
        )
        optimize_btn.grid(row=0, column=0, padx=5, pady=5)

        clear_logs_btn = tk.Button(
            maintenance_buttons,
            text="Clear Logs",
            command=self.clear_logs,
            font=FONTS['button'],
            bg=COLORS['secondary'],
            fg=COLORS['on_primary'],
            padx=15, pady=8
        )
        clear_logs_btn.grid(row=0, column=1, padx=5, pady=5)

        reset_settings_btn = tk.Button(
            maintenance_buttons,
            text="Reset Settings",
            command=self.reset_settings,
            font=FONTS['button'],
            bg=COLORS['danger'],
            fg=COLORS['on_primary'],
            padx=15, pady=8
        )
        reset_settings_btn.grid(row=1, column=0, padx=5, pady=5)

        system_info_btn = tk.Button(
            maintenance_buttons,
            text="System Info",
            command=self.show_system_info,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            padx=15, pady=8
        )
        system_info_btn.grid(row=1, column=1, padx=5, pady=5)

    def load_settings(self):
        """Load application settings"""
        settings_file = Path(__file__).parent.parent.parent / \
            "config" / "app_settings.json"

        try:
            if settings_file.exists():
                with open(settings_file, 'r') as f:
                    settings = json.load(f)

                # Load general settings
                self.auto_save_var.set(settings.get('auto_save_interval', '5'))
                self.session_timeout_var.set(
                    settings.get('session_timeout', '30'))
                self.default_semester_var.set(
                    settings.get('default_semester', '1'))
                self.font_size_var.set(settings.get('font_size', '12'))
                self.window_size_var.set(
                    settings.get('window_size', '1024x768'))

                # Load college info
                college_info = settings.get('college_info', {})
                self.college_name_var.set(
                    college_info.get('name', 'Sample College'))
                self.college_address_var.set(college_info.get('address', ''))
                self.college_phone_var.set(college_info.get('phone', ''))
                self.college_email_var.set(college_info.get('email', ''))
                self.college_website_var.set(college_info.get('website', ''))
                self.academic_year_var.set(
                    college_info.get('academic_year', '2024-25'))
                self.grading_system_var.set(
                    college_info.get('grading_system', 'Letter Grade'))

        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_general_settings(self):
        """Save general application settings"""
        try:
            settings_file = Path(__file__).parent.parent.parent / \
                "config" / "app_settings.json"

            # Load existing settings or create new
            settings = {}
            if settings_file.exists():
                with open(settings_file, 'r') as f:
                    settings = json.load(f)

            # Update general settings
            settings.update({
                'auto_save_interval': self.auto_save_var.get(),
                'session_timeout': self.session_timeout_var.get(),
                'default_semester': self.default_semester_var.get(),
                'font_size': self.font_size_var.get(),
                'window_size': self.window_size_var.get(),
                'last_updated': datetime.now().isoformat()
            })

            # Ensure config directory exists
            settings_file.parent.mkdir(exist_ok=True)

            # Save settings
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=4)

            messagebox.showinfo(
                "Success", "General settings saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def save_college_info(self):
        """Save college information"""
        try:
            # Validate inputs
            if not validate_email(self.college_email_var.get()) and self.college_email_var.get():
                messagebox.showerror(
                    "Error", "Please enter a valid email address")
                return

            if not validate_phone(self.college_phone_var.get()) and self.college_phone_var.get():
                messagebox.showerror(
                    "Error", "Please enter a valid phone number")
                return

            settings_file = Path(__file__).parent.parent.parent / \
                "config" / "app_settings.json"

            # Load existing settings or create new
            settings = {}
            if settings_file.exists():
                with open(settings_file, 'r') as f:
                    settings = json.load(f)

            # Update college info
            settings['college_info'] = {
                'name': self.college_name_var.get(),
                'address': self.college_address_var.get(),
                'phone': self.college_phone_var.get(),
                'email': self.college_email_var.get(),
                'website': self.college_website_var.get(),
                'academic_year': self.academic_year_var.get(),
                'grading_system': self.grading_system_var.get(),
                'last_updated': datetime.now().isoformat()
            }

            # Ensure config directory exists
            settings_file.parent.mkdir(exist_ok=True)

            # Save settings
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=4)

            messagebox.showinfo(
                "Success", "College information saved successfully!")

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to save college information: {str(e)}")

    def refresh_users(self):
        """Refresh users list"""
        try:
            # Clear existing items
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)

            # Get users from database
            cursor = self.db_manager.execute_query(
                "SELECT username, role, created_at FROM users ORDER BY username")
            users = cursor.fetchall()

            for user in users:
                self.users_tree.insert('', 'end', values=(
                    user['username'],
                    user['role'],
                    user['created_at'][:10] if user['created_at'] else 'N/A'
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh users: {str(e)}")

    def add_user(self):
        """Add new user"""
        dialog = UserDialog(self.parent, "Add User")
        if dialog.result:
            try:
                username, password, role = dialog.result

                # Check if username already exists
                cursor = self.db_manager.execute_query(
                    "SELECT username FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Username already exists")
                    return

                # Add user to database
                from config.database import DatabaseManager
                db_manager = DatabaseManager()
                success = db_manager.create_user(username, password, role)

                if success:
                    messagebox.showinfo("Success", "User added successfully!")
                    self.refresh_users()
                else:
                    messagebox.showerror("Error", "Failed to add user")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add user: {str(e)}")

    def edit_user(self):
        """Edit selected user"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user to edit")
            return

        item = self.users_tree.item(selection[0])
        username = item['values'][0]
        current_role = item['values'][1]

        # Simple role change dialog
        new_role = simpledialog.askstring("Edit User",
                                          f"Enter new role for {username}:",
                                          initialvalue=current_role)

        if new_role and new_role != current_role:
            try:
                self.db_manager.execute_query(
                    "UPDATE users SET role = ? WHERE username = ?",
                    (new_role, username)
                )
                messagebox.showinfo(
                    "Success", "User role updated successfully!")
                self.refresh_users()
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to update user: {str(e)}")

    def delete_user(self):
        """Delete selected user"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return

        item = self.users_tree.item(selection[0])
        username = item['values'][0]

        if username == 'admin':
            messagebox.showerror("Error", "Cannot delete admin user")
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{username}'?"):
            try:
                self.db_manager.execute_query(
                    "DELETE FROM users WHERE username = ?", (username,))
                messagebox.showinfo("Success", "User deleted successfully!")
                self.refresh_users()
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to delete user: {str(e)}")

    def create_backup(self):
        """Create database backup"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")],
                initialname=f"college_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            )

            if filename:
                # Simple file copy for SQLite database
                import shutil
                db_path = Path(__file__).parent.parent.parent / \
                    "config" / "college_management.db"
                shutil.copy2(db_path, filename)

                messagebox.showinfo(
                    "Success", f"Backup created successfully: {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}")

    def restore_backup(self):
        """Restore database from backup"""
        if not messagebox.askyesno("Confirm Restore",
                                   "This will overwrite all current data. Are you sure you want to continue?"):
            return

        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Database files", "*.db"), ("All files", "*.*")],
                title="Select backup file to restore"
            )

            if filename:
                # Simple file copy for SQLite database
                import shutil
                db_path = Path(__file__).parent.parent.parent / \
                    "config" / "college_management.db"
                shutil.copy2(filename, db_path)

                messagebox.showinfo(
                    "Success", "Database restored successfully! Please restart the application.")

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to restore backup: {str(e)}")

    def schedule_backup(self):
        """Schedule automatic backups"""
        messagebox.showinfo(
            "Feature", "Automatic backup scheduling will be implemented in a future version.")

    def optimize_database(self):
        """Optimize database performance"""
        try:
            self.db_manager.execute_query("VACUUM")
            self.db_manager.execute_query("ANALYZE")
            messagebox.showinfo("Success", "Database optimized successfully!")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to optimize database: {str(e)}")

    def clear_logs(self):
        """Clear application logs"""
        try:
            log_files = ['app.log', 'error.log', 'debug.log']
            for log_file in log_files:
                log_path = Path(__file__).parent.parent.parent / \
                    "logs" / log_file
                if log_path.exists():
                    log_path.unlink()

            messagebox.showinfo(
                "Success", "Application logs cleared successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear logs: {str(e)}")

    def reset_settings(self):
        """Reset all settings to defaults"""
        if messagebox.askyesno("Confirm Reset", "This will reset all settings to defaults. Continue?"):
            try:
                settings_file = Path(
                    __file__).parent.parent.parent / "config" / "app_settings.json"
                if settings_file.exists():
                    settings_file.unlink()

                # Reset form values
                self.auto_save_var.set("5")
                self.session_timeout_var.set("30")
                self.default_semester_var.set("1")
                self.font_size_var.set("12")
                self.window_size_var.set("1024x768")

                self.college_name_var.set("Sample College")
                self.college_address_var.set("")
                self.college_phone_var.set("")
                self.college_email_var.set("")
                self.college_website_var.set("")
                self.academic_year_var.set("2024-25")
                self.grading_system_var.set("Letter Grade")

                messagebox.showinfo("Success", "Settings reset successfully!")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to reset settings: {str(e)}")

    def show_system_info(self):
        """Show system information"""
        try:
            import platform
            import sys

            info_text = f"""
System Information
==================
Operating System: {platform.system()} {platform.release()}
Python Version: {sys.version.split()[0]}
Database: SQLite

Application Information
=====================
Version: 1.0.0
Developer: ProjectsHUB
Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Database Statistics
==================
"""

            # Get database statistics
            cursor = self.db_manager.execute_query(
                "SELECT COUNT(*) as count FROM students")
            student_count = cursor.fetchone()['count']

            cursor = self.db_manager.execute_query(
                "SELECT COUNT(*) as count FROM users")
            user_count = cursor.fetchone()['count']

            cursor = self.db_manager.execute_query(
                "SELECT COUNT(*) as count FROM library_books")
            book_count = cursor.fetchone()['count'] if cursor.fetchone() else 0

            info_text += f"Total Students: {student_count}\n"
            info_text += f"Total Users: {user_count}\n"
            info_text += f"Total Books: {book_count}\n"

            # Show in a new window
            info_window = tk.Toplevel(self.parent)
            info_window.title("System Information")
            info_window.geometry("400x350")
            info_window.configure(bg=COLORS['background'])

            text_widget = tk.Text(info_window, font=FONTS['body'], wrap='word')
            text_widget.pack(fill='both', expand=True, padx=20, pady=20)
            text_widget.insert(tk.END, info_text)
            text_widget.config(state='disabled')

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to get system information: {str(e)}")


class UserDialog:
    """Simple dialog for adding/editing users"""

    def __init__(self, parent, title):
        self.result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x200")
        self.dialog.configure(bg=COLORS['background'])
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.geometry(
            "+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        self.create_form()

    def create_form(self):
        """Create user form"""
        main_frame = tk.Frame(self.dialog, bg=COLORS['background'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Username
        tk.Label(main_frame, text="Username:", font=FONTS['body'], bg=COLORS['background']).grid(
            row=0, column=0, sticky='w', pady=5)
        self.username_var = tk.StringVar()
        tk.Entry(main_frame, textvariable=self.username_var,
                 font=FONTS['body'], width=20).grid(row=0, column=1, padx=10, pady=5)

        # Password
        tk.Label(main_frame, text="Password:", font=FONTS['body'], bg=COLORS['background']).grid(
            row=1, column=0, sticky='w', pady=5)
        self.password_var = tk.StringVar()
        tk.Entry(main_frame, textvariable=self.password_var,
                 font=FONTS['body'], width=20, show="*").grid(row=1, column=1, padx=10, pady=5)

        # Role
        tk.Label(main_frame, text="Role:", font=FONTS['body'], bg=COLORS['background']).grid(
            row=2, column=0, sticky='w', pady=5)
        self.role_var = tk.StringVar(value="user")
        role_combo = ttk.Combobox(main_frame, textvariable=self.role_var, values=[
                                  "admin", "user", "teacher"], width=18)
        role_combo.grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        button_frame = tk.Frame(main_frame, bg=COLORS['background'])
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ok_btn = tk.Button(
            button_frame,
            text="OK",
            command=self.ok_clicked,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            padx=20, pady=5
        )
        ok_btn.pack(side='left', padx=5)

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel_clicked,
            font=FONTS['button'],
            bg=COLORS['secondary'],
            fg=COLORS['on_primary'],
            padx=20, pady=5
        )
        cancel_btn.pack(side='left', padx=5)

    def ok_clicked(self):
        """Handle OK button click"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return

        self.result = (username, password, role)
        self.dialog.destroy()

    def cancel_clicked(self):
        """Handle Cancel button click"""
        self.dialog.destroy()
