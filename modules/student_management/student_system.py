"""
Student Management Module
College Management System - ProjectsHUB

Handles student information management with modern UI and database operations.
"""

from config.settings import COLORS, FONTS, COURSE_OPTIONS, GENDER_OPTIONS, STUDENT_STATUS_OPTIONS
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import re
import sys
from pathlib import Path

# Add config to path
sys.path.append(str(Path(__file__).parent.parent.parent))


class StudentManagement:
    """Modern Student Management System with CRUD operations"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.selected_student = None

        self.setup_ui()
        self.load_students()

    def setup_ui(self):
        """Create student management interface"""
        # Main container
        self.main_frame = tk.Frame(self.parent, bg=COLORS['background'])
        self.main_frame.pack(fill='both', expand=True)

        # Header
        self.create_header()

        # Content area with notebook
        self.create_content_area()

    def create_header(self):
        """Create header section"""
        header_frame = tk.Frame(
            self.main_frame, bg=COLORS['surface'], height=60)
        header_frame.pack(fill='x', padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="Student Management",
            font=FONTS['title'],
            bg=COLORS['surface'],
            fg=COLORS['on_surface']
        )
        title_label.pack(side='left', pady=15)

        # Action buttons
        btn_frame = tk.Frame(header_frame, bg=COLORS['surface'])
        btn_frame.pack(side='right', pady=10)

        add_btn = tk.Button(
            btn_frame,
            text="Add Student",
            command=self.show_add_form,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        add_btn.pack(side='right', padx=(10, 0))

        refresh_btn = tk.Button(
            btn_frame,
            text="Refresh",
            command=self.load_students,
            font=FONTS['button'],
            bg=COLORS['secondary'],
            fg=COLORS['on_secondary'],
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        refresh_btn.pack(side='right', padx=(10, 0))

    def create_content_area(self):
        """Create main content area with tabs"""
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)

        # Student list tab
        self.list_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.list_frame, text="Student List")
        self.create_student_list()

        # Student form tab
        self.form_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.form_frame, text="Student Form")
        self.create_student_form()

    def create_student_list(self):
        """Create student list with search and filter"""
        # Search frame
        search_frame = tk.Frame(self.list_frame, bg=COLORS['surface'])
        search_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(
            search_frame,
            text="Search:",
            font=FONTS['body'],
            bg=COLORS['surface']
        ).pack(side='left', padx=(10, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_students)
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=FONTS['body'],
            width=30
        )
        search_entry.pack(side='left', padx=5)

        # Filter by status
        tk.Label(
            search_frame,
            text="Status:",
            font=FONTS['body'],
            bg=COLORS['surface']
        ).pack(side='left', padx=(20, 5))

        self.status_filter = ttk.Combobox(
            search_frame,
            values=['All'] + STUDENT_STATUS_OPTIONS,
            state='readonly',
            width=15
        )
        self.status_filter.set('All')
        self.status_filter.bind('<<ComboboxSelected>>',
                                lambda e: self.filter_students())
        self.status_filter.pack(side='left', padx=5)

        # Student list treeview
        list_container = tk.Frame(self.list_frame, bg=COLORS['background'])
        list_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Treeview with scrollbars
        self.tree_frame = tk.Frame(list_container)
        self.tree_frame.pack(fill='both', expand=True)

        columns = ('Roll Number', 'Name', 'Course',
                   'Semester', 'Phone', 'Status')
        self.student_tree = ttk.Treeview(
            self.tree_frame, columns=columns, show='headings', height=15)

        # Configure columns
        column_widths = {'Roll Number': 100, 'Name': 200,
                         'Course': 150, 'Semester': 80, 'Phone': 120, 'Status': 80}
        for col in columns:
            self.student_tree.heading(col, text=col)
            self.student_tree.column(col, width=column_widths[col])

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(
            self.tree_frame, orient='vertical', command=self.student_tree.yview)
        h_scrollbar = ttk.Scrollbar(
            self.tree_frame, orient='horizontal', command=self.student_tree.xview)
        self.student_tree.configure(
            yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Pack treeview and scrollbars
        self.student_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')

        # Bind events
        self.student_tree.bind('<Double-1>', self.on_student_select)
        self.student_tree.bind('<Button-3>', self.show_context_menu)

        # Action buttons
        btn_frame = tk.Frame(self.list_frame, bg=COLORS['background'])
        btn_frame.pack(fill='x', padx=10, pady=5)

        buttons = [
            ("View Details", self.view_student_details, COLORS['primary']),
            ("Edit Student", self.edit_student, COLORS['accent']),
            ("Delete Student", self.delete_student, COLORS['danger'])
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                command=command,
                font=FONTS['button'],
                bg=color,
                fg=COLORS['on_primary'],
                relief='flat',
                bd=0,
                padx=15,
                pady=8,
                cursor='hand2'
            )
            btn.pack(side='left', padx=5)

    def create_student_form(self):
        """Create student form for add/edit operations"""
        # Form container
        form_container = tk.Frame(self.form_frame, bg=COLORS['surface'])
        form_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Form title
        self.form_title = tk.Label(
            form_container,
            text="Add New Student",
            font=FONTS['heading'],
            bg=COLORS['surface'],
            fg=COLORS['on_surface']
        )
        self.form_title.pack(pady=(0, 20))

        # Form fields frame
        fields_frame = tk.Frame(form_container, bg=COLORS['surface'])
        fields_frame.pack(fill='x', padx=20)

        # Initialize form variables
        self.form_vars = {}

        # Form fields configuration
        form_fields = [
            ('Roll Number', 'roll_number', 'entry', None),
            ('First Name', 'first_name', 'entry', None),
            ('Last Name', 'last_name', 'entry', None),
            ('Father Name', 'father_name', 'entry', None),
            ('Mother Name', 'mother_name', 'entry', None),
            ('Date of Birth', 'date_of_birth', 'entry', None),
            ('Gender', 'gender', 'combobox', GENDER_OPTIONS),
            ('Address', 'address', 'text', None),
            ('Phone Number', 'phone_number', 'entry', None),
            ('Email', 'email', 'entry', None),
            ('Course', 'course', 'combobox', COURSE_OPTIONS),
            ('Semester', 'semester', 'combobox',
             [str(i) for i in range(1, 9)]),
            ('Status', 'status', 'combobox', STUDENT_STATUS_OPTIONS)
        ]

        # Create form fields
        row = 0
        for label_text, var_name, field_type, options in form_fields:
            # Label
            label = tk.Label(
                fields_frame,
                text=f"{label_text}:",
                font=FONTS['body'],
                bg=COLORS['surface'],
                fg=COLORS['on_surface']
            )
            label.grid(row=row, column=0, sticky='w', padx=(0, 10), pady=5)

            # Field
            if field_type == 'entry':
                var = tk.StringVar()
                entry = tk.Entry(
                    fields_frame,
                    textvariable=var,
                    font=FONTS['body'],
                    width=30
                )
                entry.grid(row=row, column=1, sticky='w', pady=5)
                self.form_vars[var_name] = var

            elif field_type == 'combobox':
                var = tk.StringVar()
                combo = ttk.Combobox(
                    fields_frame,
                    textvariable=var,
                    values=options,
                    state='readonly',
                    width=27
                )
                combo.grid(row=row, column=1, sticky='w', pady=5)
                self.form_vars[var_name] = var

            elif field_type == 'text':
                var = tk.StringVar()
                text_widget = tk.Text(
                    fields_frame,
                    font=FONTS['body'],
                    width=30,
                    height=3
                )
                text_widget.grid(row=row, column=1, sticky='w', pady=5)
                # Special handling for text widget
                self.form_vars[var_name] = text_widget

            row += 1

        # Form buttons
        btn_frame = tk.Frame(form_container, bg=COLORS['surface'])
        btn_frame.pack(pady=30)

        self.save_btn = tk.Button(
            btn_frame,
            text="Save Student",
            command=self.save_student,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.save_btn.pack(side='left', padx=10)

        clear_btn = tk.Button(
            btn_frame,
            text="Clear Form",
            command=self.clear_form,
            font=FONTS['button'],
            bg=COLORS['secondary'],
            fg=COLORS['on_secondary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        clear_btn.pack(side='left', padx=10)

        # Initially hide the form (will be shown when needed)
        self.is_edit_mode = False
        self.current_student_id = None

    def load_students(self):
        """Load students from database"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT student_id, roll_number, first_name, last_name, 
                       course, semester, phone_number, status
                FROM students
                ORDER BY roll_number
            """)

            # Clear existing items
            for item in self.student_tree.get_children():
                self.student_tree.delete(item)

            # Insert new items
            self.all_students = cursor.fetchall()
            for student in self.all_students:
                name = f"{student['first_name']} {student['last_name']}"
                self.student_tree.insert('', 'end', values=(
                    student['roll_number'],
                    name,
                    student['course'] or '',
                    student['semester'] or '',
                    student['phone_number'] or '',
                    student['status']
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load students: {str(e)}")

    def filter_students(self, *args):
        """Filter students based on search criteria"""
        search_term = self.search_var.get().lower()
        status_filter = self.status_filter.get()

        # Clear existing items
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        # Filter and insert matching items
        for student in self.all_students:
            name = f"{student['first_name']} {student['last_name']}".lower()
            roll_number = student['roll_number'].lower()

            # Check search term
            if search_term and search_term not in name and search_term not in roll_number:
                continue

            # Check status filter
            if status_filter != 'All' and student['status'] != status_filter:
                continue

            # Insert matching student
            display_name = f"{student['first_name']} {student['last_name']}"
            self.student_tree.insert('', 'end', values=(
                student['roll_number'],
                display_name,
                student['course'] or '',
                student['semester'] or '',
                student['phone_number'] or '',
                student['status']
            ))

    def show_add_form(self):
        """Show form for adding new student"""
        self.clear_form()
        self.form_title.config(text="Add New Student")
        self.save_btn.config(text="Save Student")
        self.is_edit_mode = False
        self.current_student_id = None
        self.notebook.select(1)  # Switch to form tab

    def save_student(self):
        """Save student data"""
        try:
            # Collect form data
            data = {}
            for field_name, widget in self.form_vars.items():
                if isinstance(widget, tk.Text):
                    data[field_name] = widget.get('1.0', 'end-1c')
                else:
                    data[field_name] = widget.get()

            # Validate required fields
            required_fields = ['roll_number', 'first_name', 'last_name']
            for field in required_fields:
                if not data[field].strip():
                    messagebox.showerror(
                        "Validation Error", f"{field.replace('_', ' ').title()} is required")
                    return

            # Validate email format
            if data['email'] and not self.validate_email(data['email']):
                messagebox.showerror("Validation Error",
                                     "Invalid email format")
                return

            # Save to database
            if self.is_edit_mode:
                self.update_student(data)
            else:
                self.add_student(data)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save student: {str(e)}")

    def add_student(self, data):
        """Add new student to database"""
        # Check if roll number exists
        cursor = self.db_manager.execute_query(
            "SELECT COUNT(*) FROM students WHERE roll_number = ?",
            (data['roll_number'],)
        )
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Error", "Roll number already exists")
            return

        # Insert student
        self.db_manager.execute_and_commit("""
            INSERT INTO students (
                roll_number, first_name, last_name, father_name, mother_name,
                date_of_birth, gender, address, phone_number, email,
                course, semester, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['roll_number'], data['first_name'], data['last_name'],
            data['father_name'], data['mother_name'], data['date_of_birth'],
            data['gender'], data['address'], data['phone_number'],
            data['email'], data['course'], data['semester'], data['status']
        ))

        messagebox.showinfo("Success", "Student added successfully")
        self.clear_form()
        self.load_students()
        self.notebook.select(0)  # Switch to list tab

    def update_student(self, data):
        """Update existing student in database"""
        self.db_manager.execute_and_commit("""
            UPDATE students SET
                roll_number = ?, first_name = ?, last_name = ?, father_name = ?,
                mother_name = ?, date_of_birth = ?, gender = ?, address = ?,
                phone_number = ?, email = ?, course = ?, semester = ?, status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE student_id = ?
        """, (
            data['roll_number'], data['first_name'], data['last_name'],
            data['father_name'], data['mother_name'], data['date_of_birth'],
            data['gender'], data['address'], data['phone_number'],
            data['email'], data['course'], data['semester'], data['status'],
            self.current_student_id
        ))

        messagebox.showinfo("Success", "Student updated successfully")
        self.load_students()
        self.notebook.select(0)  # Switch to list tab

    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def clear_form(self):
        """Clear all form fields"""
        for field_name, widget in self.form_vars.items():
            if isinstance(widget, tk.Text):
                widget.delete('1.0', 'end')
            else:
                widget.set('')

    def on_student_select(self, event):
        """Handle student selection from list"""
        selection = self.student_tree.selection()
        if selection:
            self.view_student_details()

    def view_student_details(self):
        """View selected student details"""
        selection = self.student_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a student")
            return

        # Get selected student data
        item = self.student_tree.item(selection[0])
        roll_number = item['values'][0]

        try:
            cursor = self.db_manager.execute_query(
                "SELECT * FROM students WHERE roll_number = ?",
                (roll_number,)
            )
            student = cursor.fetchone()

            if student:
                self.show_student_details_window(student)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to load student details: {str(e)}")

    def show_student_details_window(self, student):
        """Show student details in popup window"""
        details_window = tk.Toplevel(self.parent)
        details_window.title(
            f"Student Details - {student['first_name']} {student['last_name']}")
        details_window.geometry("500x600")
        details_window.configure(bg=COLORS['background'])

        # Title
        title_label = tk.Label(
            details_window,
            text="Student Details",
            font=FONTS['heading'],
            bg=COLORS['background'],
            fg=COLORS['on_background']
        )
        title_label.pack(pady=20)

        # Details frame
        details_frame = tk.Frame(
            details_window, bg=COLORS['surface'], relief='solid', bd=1)
        details_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Student information
        info_fields = [
            ('Roll Number', student['roll_number']),
            ('Name', f"{student['first_name']} {student['last_name']}"),
            ('Father Name', student['father_name']),
            ('Mother Name', student['mother_name']),
            ('Date of Birth', student['date_of_birth']),
            ('Gender', student['gender']),
            ('Address', student['address']),
            ('Phone', student['phone_number']),
            ('Email', student['email']),
            ('Course', student['course']),
            ('Semester', student['semester']),
            ('Status', student['status']),
            ('Admission Date', student['admission_date'])
        ]

        for i, (label, value) in enumerate(info_fields):
            tk.Label(
                details_frame,
                text=f"{label}:",
                font=FONTS['subheading'],
                bg=COLORS['surface'],
                fg=COLORS['on_surface']
            ).grid(row=i, column=0, sticky='w', padx=20, pady=5)

            tk.Label(
                details_frame,
                text=str(value) if value else 'N/A',
                font=FONTS['body'],
                bg=COLORS['surface'],
                fg=COLORS['on_surface']
            ).grid(row=i, column=1, sticky='w', padx=20, pady=5)

        # Close button
        close_btn = tk.Button(
            details_window,
            text="Close",
            command=details_window.destroy,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        close_btn.pack(pady=20)

    def edit_student(self):
        """Edit selected student"""
        selection = self.student_tree.selection()
        if not selection:
            messagebox.showwarning(
                "Warning", "Please select a student to edit")
            return

        # Get selected student data
        item = self.student_tree.item(selection[0])
        roll_number = item['values'][0]

        try:
            cursor = self.db_manager.execute_query(
                "SELECT * FROM students WHERE roll_number = ?",
                (roll_number,)
            )
            student = cursor.fetchone()

            if student:
                # Populate form with student data
                self.populate_form_with_student(student)
                self.form_title.config(text="Edit Student")
                self.save_btn.config(text="Update Student")
                self.is_edit_mode = True
                self.current_student_id = student['student_id']
                self.notebook.select(1)  # Switch to form tab

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to load student for editing: {str(e)}")

    def populate_form_with_student(self, student):
        """Populate form with student data"""
        field_mapping = {
            'roll_number': student['roll_number'],
            'first_name': student['first_name'],
            'last_name': student['last_name'],
            'father_name': student['father_name'],
            'mother_name': student['mother_name'],
            'date_of_birth': student['date_of_birth'],
            'gender': student['gender'],
            'phone_number': student['phone_number'],
            'email': student['email'],
            'course': student['course'],
            'semester': str(student['semester']) if student['semester'] else '',
            'status': student['status']
        }

        # Populate regular fields
        for field_name, value in field_mapping.items():
            if field_name in self.form_vars:
                widget = self.form_vars[field_name]
                if isinstance(widget, tk.Text):
                    widget.delete('1.0', 'end')
                    widget.insert('1.0', value or '')
                else:
                    widget.set(value or '')

        # Populate address (text widget)
        if 'address' in self.form_vars:
            self.form_vars['address'].delete('1.0', 'end')
            self.form_vars['address'].insert('1.0', student['address'] or '')

    def delete_student(self):
        """Delete selected student"""
        selection = self.student_tree.selection()
        if not selection:
            messagebox.showwarning(
                "Warning", "Please select a student to delete")
            return

        # Get selected student data
        item = self.student_tree.item(selection[0])
        roll_number = item['values'][0]
        student_name = item['values'][1]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student {student_name}?"):
            try:
                self.db_manager.execute_and_commit(
                    "DELETE FROM students WHERE roll_number = ?",
                    (roll_number,)
                )
                messagebox.showinfo("Success", "Student deleted successfully")
                self.load_students()

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to delete student: {str(e)}")

    def show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select item under cursor
        item = self.student_tree.identify_row(event.y)
        if item:
            self.student_tree.selection_set(item)

            # Create context menu
            context_menu = tk.Menu(self.parent, tearoff=0)
            context_menu.add_command(
                label="View Details", command=self.view_student_details)
            context_menu.add_command(
                label="Edit Student", command=self.edit_student)
            context_menu.add_separator()
            context_menu.add_command(
                label="Delete Student", command=self.delete_student)

            # Show menu
            context_menu.post(event.x_root, event.y_root)
