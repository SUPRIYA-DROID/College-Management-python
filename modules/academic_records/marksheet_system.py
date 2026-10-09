"""
Academic Records System
College Management System - ProjectsHUB

Simple but fully functional academic records and marksheet management.
"""

from config.settings import COLORS, FONTS, EXAM_TYPES
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import sys
from pathlib import Path

# Add config to path
sys.path.append(str(Path(__file__).parent.parent.parent))


class MarksheetSystem:
    """Simple Academic Records Management System"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager

        self.setup_ui()
        self.load_marksheets()

    def setup_ui(self):
        """Create academic records interface"""
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
            text="Academic Records",
            font=FONTS['title'],
            bg=COLORS['surface'],
            fg=COLORS['on_surface']
        )
        title_label.pack(side='left', pady=15)

    def create_tabs(self):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)

        # Add marks tab
        self.add_marks_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.add_marks_frame, text="Add Marks")
        self.create_add_marks_tab()

        # View marksheets tab
        self.view_marks_frame = tk.Frame(
            self.notebook, bg=COLORS['background'])
        self.notebook.add(self.view_marks_frame, text="View Marksheets")
        self.create_view_marks_tab()

        # Student performance tab
        self.performance_frame = tk.Frame(
            self.notebook, bg=COLORS['background'])
        self.notebook.add(self.performance_frame, text="Student Performance")
        self.create_performance_tab()

    def create_add_marks_tab(self):
        """Create add marks tab"""
        # Student selection
        student_frame = tk.LabelFrame(
            self.add_marks_frame, text="Select Student", font=FONTS['subheading'])
        student_frame.pack(fill='x', padx=10, pady=10)

        student_fields = tk.Frame(student_frame)
        student_fields.pack(fill='x', padx=20, pady=10)

        tk.Label(student_fields, text="Student Roll No:", font=FONTS['body']).grid(
            row=0, column=0, sticky='w', pady=5)
        self.student_roll_var = tk.StringVar()
        tk.Entry(student_fields, textvariable=self.student_roll_var,
                 font=FONTS['body'], width=20).grid(row=0, column=1, padx=5)

        get_student_btn = tk.Button(
            student_fields,
            text="Get Student Info",
            command=self.get_student_info,
            font=FONTS['body'],
            bg=COLORS['accent'],
            fg=COLORS['on_primary'],
            padx=10, pady=3
        )
        get_student_btn.grid(row=0, column=2, padx=10)

        self.student_info_label = tk.Label(
            student_fields, text="", font=FONTS['body'], fg=COLORS['primary'])
        self.student_info_label.grid(
            row=1, column=0, columnspan=3, sticky='w', pady=5)

        # Marks form
        marks_frame = tk.LabelFrame(
            self.add_marks_frame, text="Add Subject Marks", font=FONTS['subheading'])
        marks_frame.pack(fill='x', padx=10, pady=10)

        marks_fields = tk.Frame(marks_frame)
        marks_fields.pack(fill='x', padx=20, pady=10)

        # Subject details
        tk.Label(marks_fields, text="Subject Name:", font=FONTS['body']).grid(
            row=0, column=0, sticky='w', pady=5)
        self.subject_name_var = tk.StringVar()
        tk.Entry(marks_fields, textvariable=self.subject_name_var,
                 font=FONTS['body'], width=25).grid(row=0, column=1, padx=5)

        tk.Label(marks_fields, text="Exam Type:", font=FONTS['body']).grid(
            row=0, column=2, sticky='w', padx=(20, 0), pady=5)
        self.exam_type_var = tk.StringVar()
        exam_combo = ttk.Combobox(
            marks_fields, textvariable=self.exam_type_var, values=EXAM_TYPES, width=15)
        exam_combo.grid(row=0, column=3, padx=5)

        # Marks
        tk.Label(marks_fields, text="Maximum Marks:", font=FONTS['body']).grid(
            row=1, column=0, sticky='w', pady=5)
        self.max_marks_var = tk.StringVar(value="100")
        tk.Entry(marks_fields, textvariable=self.max_marks_var,
                 font=FONTS['body'], width=10).grid(row=1, column=1, sticky='w', padx=5)

        tk.Label(marks_fields, text="Obtained Marks:", font=FONTS['body']).grid(
            row=1, column=2, sticky='w', padx=(20, 0), pady=5)
        self.obtained_marks_var = tk.StringVar()
        tk.Entry(marks_fields, textvariable=self.obtained_marks_var,
                 font=FONTS['body'], width=10).grid(row=1, column=3, sticky='w', padx=5)

        # Grade display
        tk.Label(marks_fields, text="Grade:", font=FONTS['body']).grid(
            row=2, column=0, sticky='w', pady=5)
        self.grade_label = tk.Label(
            marks_fields, text="", font=FONTS['subheading'], fg=COLORS['primary'])
        self.grade_label.grid(row=2, column=1, sticky='w', padx=5)

        # Calculate grade when marks change
        self.obtained_marks_var.trace('w', self.calculate_grade)
        self.max_marks_var.trace('w', self.calculate_grade)

        # Exam date and academic year
        tk.Label(marks_fields, text="Exam Date:", font=FONTS['body']).grid(
            row=3, column=0, sticky='w', pady=5)
        self.exam_date_var = tk.StringVar(
            value=date.today().strftime('%Y-%m-%d'))
        tk.Entry(marks_fields, textvariable=self.exam_date_var,
                 font=FONTS['body'], width=15).grid(row=3, column=1, padx=5)

        tk.Label(marks_fields, text="Academic Year:", font=FONTS['body']).grid(
            row=3, column=2, sticky='w', padx=(20, 0), pady=5)
        self.academic_year_var = tk.StringVar(
            value=self.get_current_academic_year())
        tk.Entry(marks_fields, textvariable=self.academic_year_var,
                 font=FONTS['body'], width=15).grid(row=3, column=3, padx=5)

        # Add marks button
        add_marks_btn = tk.Button(
            marks_frame,
            text="Add Marks",
            command=self.add_marks,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            padx=20, pady=5
        )
        add_marks_btn.pack(pady=10)

        # Hidden student ID
        self.selected_student_id = None

    def create_view_marks_tab(self):
        """Create view marksheets tab"""
        # Search frame
        search_frame = tk.Frame(self.view_marks_frame)
        search_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(search_frame, text="Search by Roll No:",
                 font=FONTS['body']).pack(side='left')
        self.search_marks_var = tk.StringVar()
        self.search_marks_var.trace('w', self.filter_marksheets)
        tk.Entry(search_frame, textvariable=self.search_marks_var,
                 font=FONTS['body'], width=20).pack(side='left', padx=5)

        tk.Label(search_frame, text="Semester:", font=FONTS['body']).pack(
            side='left', padx=(20, 0))
        self.filter_semester_var = tk.StringVar()
        semester_combo = ttk.Combobox(search_frame, textvariable=self.filter_semester_var,
                                      values=['All'] + [str(i) for i in range(1, 9)], width=10)
        semester_combo.set('All')
        semester_combo.bind('<<ComboboxSelected>>',
                            lambda e: self.filter_marksheets())
        semester_combo.pack(side='left', padx=5)

        # Marksheets list
        list_frame = tk.LabelFrame(
            self.view_marks_frame, text="Student Marksheets", font=FONTS['subheading'])
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)

        columns = ('Roll No', 'Student Name', 'Subject', 'Max Marks',
                   'Obtained', 'Grade', 'Exam Type', 'Date')
        self.marksheets_tree = ttk.Treeview(
            list_frame, columns=columns, show='headings', height=15)

        column_widths = {'Roll No': 80, 'Student Name': 150, 'Subject': 120, 'Max Marks': 80,
                         'Obtained': 80, 'Grade': 60, 'Exam Type': 100, 'Date': 100}
        for col in columns:
            self.marksheets_tree.heading(col, text=col)
            self.marksheets_tree.column(col, width=column_widths[col])

        scrollbar_marks = ttk.Scrollbar(
            list_frame, orient='vertical', command=self.marksheets_tree.yview)
        self.marksheets_tree.configure(yscrollcommand=scrollbar_marks.set)

        self.marksheets_tree.pack(
            side='left', fill='both', expand=True, padx=10, pady=5)
        scrollbar_marks.pack(side='right', fill='y', pady=5)

        # Buttons frame
        btn_frame = tk.Frame(self.view_marks_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)

        generate_sheet_btn = tk.Button(
            btn_frame,
            text="Generate Marksheet",
            command=self.generate_student_marksheet,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            padx=20, pady=5
        )
        generate_sheet_btn.pack(side='left', padx=5)

        delete_marks_btn = tk.Button(
            btn_frame,
            text="Delete Selected",
            command=self.delete_marks,
            font=FONTS['button'],
            bg=COLORS['danger'],
            fg=COLORS['on_primary'],
            padx=20, pady=5
        )
        delete_marks_btn.pack(side='left', padx=5)

    def create_performance_tab(self):
        """Create student performance analysis tab"""
        # Student selection
        perf_search_frame = tk.Frame(self.performance_frame)
        perf_search_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(perf_search_frame, text="Student Roll No:",
                 font=FONTS['body']).pack(side='left')
        self.perf_student_var = tk.StringVar()
        tk.Entry(perf_search_frame, textvariable=self.perf_student_var,
                 font=FONTS['body'], width=20).pack(side='left', padx=5)

        analyze_btn = tk.Button(
            perf_search_frame,
            text="Analyze Performance",
            command=self.analyze_performance,
            font=FONTS['button'],
            bg=COLORS['accent'],
            fg=COLORS['on_primary'],
            padx=15, pady=5
        )
        analyze_btn.pack(side='left', padx=10)

        # Performance display
        self.performance_display_frame = tk.LabelFrame(
            self.performance_frame, text="Performance Analysis", font=FONTS['subheading'])
        self.performance_display_frame.pack(
            fill='both', expand=True, padx=10, pady=10)

        # Performance text widget
        self.performance_text = tk.Text(
            self.performance_display_frame,
            font=FONTS['body'],
            wrap='word',
            height=20,
            state='disabled'
        )

        perf_scrollbar = ttk.Scrollbar(
            self.performance_display_frame, orient='vertical', command=self.performance_text.yview)
        self.performance_text.configure(yscrollcommand=perf_scrollbar.set)

        self.performance_text.pack(
            side='left', fill='both', expand=True, padx=10, pady=10)
        perf_scrollbar.pack(side='right', fill='y', pady=10)

    def get_current_academic_year(self):
        """Get current academic year"""
        current_year = datetime.now().year
        if datetime.now().month >= 7:
            return f"{current_year}-{current_year + 1}"
        else:
            return f"{current_year - 1}-{current_year}"

    def get_student_info(self):
        """Get student information for marks entry"""
        try:
            roll_number = self.student_roll_var.get().strip()
            if not roll_number:
                messagebox.showerror(
                    "Error", "Please enter student roll number")
                return

            cursor = self.db_manager.execute_query(
                "SELECT student_id, first_name, last_name, course, semester FROM students WHERE roll_number = ?",
                (roll_number,)
            )
            student = cursor.fetchone()
            if not student:
                messagebox.showerror("Error", "Student not found")
                return

            self.selected_student_id = student['student_id']
            info_text = f"Student: {student['first_name']} {student['last_name']}, Course: {student['course']}, Semester: {student['semester']}"
            self.student_info_label.config(text=info_text)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to get student info: {str(e)}")

    def calculate_grade(self, *args):
        """Calculate grade based on marks"""
        try:
            max_marks = float(self.max_marks_var.get() or 100)
            obtained_marks = float(self.obtained_marks_var.get() or 0)

            if max_marks <= 0:
                self.grade_label.config(text="")
                return

            percentage = (obtained_marks / max_marks) * 100

            if percentage >= 90:
                grade = 'A+'
            elif percentage >= 80:
                grade = 'A'
            elif percentage >= 70:
                grade = 'B+'
            elif percentage >= 60:
                grade = 'B'
            elif percentage >= 50:
                grade = 'C+'
            elif percentage >= 40:
                grade = 'C'
            elif percentage >= 30:
                grade = 'D'
            else:
                grade = 'F'

            self.grade_label.config(text=f"{grade} ({percentage:.1f}%)")

        except ValueError:
            self.grade_label.config(text="")

    def add_marks(self):
        """Add subject marks for student"""
        try:
            if not self.selected_student_id:
                messagebox.showerror("Error", "Please select a student first")
                return

            subject_name = self.subject_name_var.get().strip()
            exam_type = self.exam_type_var.get().strip()
            max_marks = int(self.max_marks_var.get() or 100)
            obtained_marks = int(self.obtained_marks_var.get() or 0)
            exam_date = self.exam_date_var.get().strip()
            academic_year = self.academic_year_var.get().strip()

            if not all([subject_name, exam_type, exam_date, academic_year]):
                messagebox.showerror("Error", "All fields are required")
                return

            if obtained_marks > max_marks:
                messagebox.showerror(
                    "Error", "Obtained marks cannot be greater than maximum marks")
                return

            # Calculate grade
            percentage = (obtained_marks / max_marks) * 100
            if percentage >= 90:
                grade = 'A+'
            elif percentage >= 80:
                grade = 'A'
            elif percentage >= 70:
                grade = 'B+'
            elif percentage >= 60:
                grade = 'B'
            elif percentage >= 50:
                grade = 'C+'
            elif percentage >= 40:
                grade = 'C'
            elif percentage >= 30:
                grade = 'D'
            else:
                grade = 'F'

            # Get student semester and course for record
            cursor = self.db_manager.execute_query(
                "SELECT course, semester FROM students WHERE student_id = ?",
                (self.selected_student_id,)
            )
            student = cursor.fetchone()

            # Insert marks
            self.db_manager.execute_and_commit("""
                INSERT INTO marksheets (student_id, course, semester, subject_name, max_marks, 
                                      obtained_marks, grade, exam_type, exam_date, academic_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.selected_student_id, student['course'], student['semester'], subject_name,
                  max_marks, obtained_marks, grade, exam_type, exam_date, academic_year))

            messagebox.showinfo(
                "Success", f"Marks added successfully for {subject_name}")
            self.clear_marks_form()
            self.load_marksheets()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid marks")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add marks: {str(e)}")

    def clear_marks_form(self):
        """Clear marks form"""
        self.subject_name_var.set("")
        self.exam_type_var.set("")
        self.max_marks_var.set("100")
        self.obtained_marks_var.set("")
        self.grade_label.config(text="")

    def load_marksheets(self):
        """Load all marksheets"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT s.roll_number, s.first_name, s.last_name, m.subject_name, 
                       m.max_marks, m.obtained_marks, m.grade, m.exam_type, m.exam_date,
                       m.marksheet_id, s.semester
                FROM marksheets m
                JOIN students s ON m.student_id = s.student_id
                ORDER BY s.roll_number, m.subject_name
            """)

            # Clear existing items
            for item in self.marksheets_tree.get_children():
                self.marksheets_tree.delete(item)

            # Insert marksheets
            self.all_marksheets = cursor.fetchall()
            for mark in self.all_marksheets:
                student_name = f"{mark['first_name']} {mark['last_name']}"
                self.marksheets_tree.insert('', 'end', values=(
                    mark['roll_number'],
                    student_name,
                    mark['subject_name'],
                    mark['max_marks'],
                    mark['obtained_marks'],
                    mark['grade'],
                    mark['exam_type'],
                    mark['exam_date']
                ), tags=(mark['marksheet_id'],))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to load marksheets: {str(e)}")

    def filter_marksheets(self, *args):
        """Filter marksheets by student and semester"""
        search_term = self.search_marks_var.get().lower()
        semester_filter = self.filter_semester_var.get()

        # Clear existing items
        for item in self.marksheets_tree.get_children():
            self.marksheets_tree.delete(item)

        # Filter and insert matching marksheets
        for mark in self.all_marksheets:
            # Check search term
            if search_term and search_term not in mark['roll_number'].lower():
                continue

            # Check semester filter
            if semester_filter != 'All' and str(mark['semester']) != semester_filter:
                continue

            student_name = f"{mark['first_name']} {mark['last_name']}"
            self.marksheets_tree.insert('', 'end', values=(
                mark['roll_number'],
                student_name,
                mark['subject_name'],
                mark['max_marks'],
                mark['obtained_marks'],
                mark['grade'],
                mark['exam_type'],
                mark['exam_date']
            ), tags=(mark['marksheet_id'],))

    def generate_student_marksheet(self):
        """Generate complete marksheet for a student"""
        roll_number = self.search_marks_var.get().strip()
        if not roll_number:
            messagebox.showerror(
                "Error", "Please enter a student roll number to generate marksheet")
            return

        try:
            # Get student info
            cursor = self.db_manager.execute_query(
                "SELECT * FROM students WHERE roll_number = ?", (roll_number,)
            )
            student = cursor.fetchone()
            if not student:
                messagebox.showerror("Error", "Student not found")
                return

            # Get student marks
            cursor = self.db_manager.execute_query("""
                SELECT subject_name, max_marks, obtained_marks, grade, exam_type, exam_date
                FROM marksheets WHERE student_id = ?
                ORDER BY subject_name
            """, (student['student_id'],))

            marks = cursor.fetchall()
            if not marks:
                messagebox.showwarning(
                    "Warning", "No marks found for this student")
                return

            # Create marksheet window
            self.show_marksheet_window(student, marks)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate marksheet: {str(e)}")

    def show_marksheet_window(self, student, marks):
        """Show marksheet in a new window"""
        marksheet_window = tk.Toplevel(self.parent)
        marksheet_window.title(
            f"Marksheet - {student['first_name']} {student['last_name']}")
        marksheet_window.geometry("600x700")
        marksheet_window.configure(bg=COLORS['background'])

        # Header
        header_frame = tk.Frame(
            marksheet_window, bg=COLORS['primary'], height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="COLLEGE MARKSHEET",
            font=FONTS['title'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary']
        )
        title_label.pack(pady=20)

        # Student details
        details_frame = tk.Frame(marksheet_window, bg=COLORS['surface'])
        details_frame.pack(fill='x', padx=20, pady=20)

        details = [
            ("Name", f"{student['first_name']} {student['last_name']}"),
            ("Roll Number", student['roll_number']),
            ("Course", student['course']),
            ("Semester", str(student['semester'])),
            ("Father's Name", student['father_name'] or 'N/A'),
        ]

        for i, (label, value) in enumerate(details):
            tk.Label(details_frame, text=f"{label}:", font=FONTS['subheading'], bg=COLORS['surface']).grid(
                row=i//2, column=(i % 2)*2, sticky='w', padx=10, pady=5)
            tk.Label(details_frame, text=value, font=FONTS['body'], bg=COLORS['surface']).grid(
                row=i//2, column=(i % 2)*2+1, sticky='w', padx=10, pady=5)

        # Marks table
        marks_frame = tk.Frame(marksheet_window, bg=COLORS['background'])
        marks_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Table headers
        headers = ['Subject', 'Max Marks', 'Obtained', 'Grade', 'Exam Type']
        for i, header in enumerate(headers):
            tk.Label(marks_frame, text=header, font=FONTS['subheading'],
                     bg=COLORS['primary'], fg=COLORS['on_primary'],
                     relief='solid', bd=1).grid(row=0, column=i, sticky='ew', padx=1, pady=1)

        # Marks data
        total_max = 0
        total_obtained = 0

        for i, mark in enumerate(marks, 1):
            row_data = [
                mark['subject_name'],
                str(mark['max_marks']),
                str(mark['obtained_marks']),
                mark['grade'],
                mark['exam_type']
            ]

            for j, data in enumerate(row_data):
                tk.Label(marks_frame, text=data, font=FONTS['body'],
                         bg=COLORS['surface'], relief='solid', bd=1).grid(
                    row=i, column=j, sticky='ew', padx=1, pady=1)

            total_max += mark['max_marks']
            total_obtained += mark['obtained_marks']

        # Total row
        if marks:
            percentage = (total_obtained / total_max) * 100
            total_row = ['TOTAL', str(total_max), str(
                total_obtained), f"{percentage:.1f}%", ""]

            for j, data in enumerate(total_row):
                tk.Label(marks_frame, text=data, font=FONTS['subheading'],
                         bg=COLORS['accent'], fg=COLORS['on_primary'],
                         relief='solid', bd=1).grid(row=len(marks)+1, column=j, sticky='ew', padx=1, pady=1)

        # Configure grid weights
        for i in range(5):
            marks_frame.grid_columnconfigure(i, weight=1)

        # Footer
        footer_frame = tk.Frame(marksheet_window, bg=COLORS['surface'])
        footer_frame.pack(fill='x', pady=20)

        generated_label = tk.Label(
            footer_frame,
            text=f"Generated on: {date.today().strftime('%B %d, %Y')}",
            font=FONTS['small'],
            bg=COLORS['surface']
        )
        generated_label.pack(pady=10)

        powered_label = tk.Label(
            footer_frame,
            text="Powered by ProjectsHUB",
            font=FONTS['small'],
            bg=COLORS['surface'],
            fg=COLORS['primary']
        )
        powered_label.pack()

    def delete_marks(self):
        """Delete selected marks record"""
        selection = self.marksheets_tree.selection()
        if not selection:
            messagebox.showwarning(
                "Warning", "Please select a record to delete")
            return

        marksheet_id = self.marksheets_tree.item(selection[0])['tags'][0]
        subject = self.marksheets_tree.item(selection[0])['values'][2]

        if messagebox.askyesno("Confirm", f"Delete marks for {subject}?"):
            try:
                self.db_manager.execute_and_commit(
                    "DELETE FROM marksheets WHERE marksheet_id = ?", (
                        marksheet_id,)
                )
                messagebox.showinfo("Success", "Marks deleted successfully")
                self.load_marksheets()

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to delete marks: {str(e)}")

    def analyze_performance(self):
        """Analyze student performance"""
        try:
            roll_number = self.perf_student_var.get().strip()
            if not roll_number:
                messagebox.showerror(
                    "Error", "Please enter student roll number")
                return

            # Get student info
            cursor = self.db_manager.execute_query(
                "SELECT * FROM students WHERE roll_number = ?", (roll_number,)
            )
            student = cursor.fetchone()
            if not student:
                messagebox.showerror("Error", "Student not found")
                return

            # Get student marks
            cursor = self.db_manager.execute_query("""
                SELECT subject_name, max_marks, obtained_marks, grade, exam_type, exam_date
                FROM marksheets WHERE student_id = ?
                ORDER BY exam_date DESC
            """, (student['student_id'],))

            marks = cursor.fetchall()

            # Generate performance analysis
            analysis = self.generate_performance_analysis(student, marks)

            # Display analysis
            self.performance_text.config(state='normal')
            self.performance_text.delete(1.0, tk.END)
            self.performance_text.insert(tk.END, analysis)
            self.performance_text.config(state='disabled')

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to analyze performance: {str(e)}")

    def generate_performance_analysis(self, student, marks):
        """Generate detailed performance analysis"""
        if not marks:
            return "No academic records found for this student."

        analysis = []
        analysis.append("=" * 60)
        analysis.append("STUDENT PERFORMANCE ANALYSIS")
        analysis.append("=" * 60)
        analysis.append("")

        # Student details
        analysis.append(
            f"Student Name: {student['first_name']} {student['last_name']}")
        analysis.append(f"Roll Number: {student['roll_number']}")
        analysis.append(f"Course: {student['course']}")
        analysis.append(f"Semester: {student['semester']}")
        analysis.append("")

        # Overall performance
        total_max = sum(mark['max_marks'] for mark in marks)
        total_obtained = sum(mark['obtained_marks'] for mark in marks)
        overall_percentage = (total_obtained / total_max) * \
            100 if total_max > 0 else 0

        analysis.append("OVERALL PERFORMANCE:")
        analysis.append(f"Total Subjects: {len(marks)}")
        analysis.append(f"Total Marks: {total_obtained}/{total_max}")
        analysis.append(f"Overall Percentage: {overall_percentage:.2f}%")
        analysis.append("")

        # Grade distribution
        grade_count = {}
        for mark in marks:
            grade = mark['grade']
            grade_count[grade] = grade_count.get(grade, 0) + 1

        analysis.append("GRADE DISTRIBUTION:")
        for grade, count in sorted(grade_count.items()):
            analysis.append(f"{grade}: {count} subjects")
        analysis.append("")

        # Subject-wise performance
        analysis.append("SUBJECT-WISE PERFORMANCE:")
        analysis.append("-" * 50)

        for mark in marks:
            percentage = (mark['obtained_marks'] / mark['max_marks']) * 100
            analysis.append(f"{mark['subject_name']:<20} {mark['obtained_marks']:>3}/{mark['max_marks']:<3} "
                            f"{percentage:>6.1f}% ({mark['grade']})")

        analysis.append("")

        # Performance insights
        analysis.append("PERFORMANCE INSIGHTS:")

        # Best performing subjects
        sorted_marks = sorted(marks, key=lambda x: (
            x['obtained_marks'] / x['max_marks']), reverse=True)
        analysis.append(
            f"Best Subject: {sorted_marks[0]['subject_name']} ({sorted_marks[0]['grade']})")

        if len(sorted_marks) > 1:
            analysis.append(
                f"Needs Improvement: {sorted_marks[-1]['subject_name']} ({sorted_marks[-1]['grade']})")

        # Grade analysis
        excellent_subjects = [m for m in marks if m['grade'] in ['A+', 'A']]
        failing_subjects = [m for m in marks if m['grade'] == 'F']

        analysis.append(
            f"Excellent Performance: {len(excellent_subjects)} subjects")
        if failing_subjects:
            analysis.append(
                f"Failed Subjects: {len(failing_subjects)} subjects")

        analysis.append("")
        analysis.append("=" * 60)
        analysis.append("Report generated by College Management System")
        analysis.append("Powered by ProjectsHUB")

        return "\n".join(analysis)
