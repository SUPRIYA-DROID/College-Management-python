"""
Fee Management System
College Management System - ProjectsHUB

Simple but fully functional fee management with payments and receipts.
"""

from config.settings import COLORS, FONTS, PAYMENT_METHODS
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import sys
from pathlib import Path

# Add config to path
sys.path.append(str(Path(__file__).parent.parent.parent))


class FeeSystem:
    """Simple Fee Management System"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager

        self.setup_ui()
        self.load_fee_records()

    def setup_ui(self):
        """Create fee management interface"""
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
            text="Fee Management",
            font=FONTS['title'],
            bg=COLORS['surface'],
            fg=COLORS['on_surface']
        )
        title_label.pack(side='left', pady=15)

    def create_tabs(self):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)

        # Fee structure tab
        self.structure_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.structure_frame, text="Fee Structure")
        self.create_structure_tab()

        # Payment tab
        self.payment_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.payment_frame, text="Record Payment")
        self.create_payment_tab()

        # Records tab
        self.records_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.records_frame, text="Payment Records")
        self.create_records_tab()

    def create_structure_tab(self):
        """Create fee structure management tab"""
        # Add fee structure form
        form_frame = tk.LabelFrame(
            self.structure_frame, text="Add Fee Structure", font=FONTS['subheading'])
        form_frame.pack(fill='x', padx=10, pady=10)

        fields_frame = tk.Frame(form_frame)
        fields_frame.pack(fill='x', padx=20, pady=10)

        # Course and Semester
        tk.Label(fields_frame, text="Course:", font=FONTS['body']).grid(
            row=0, column=0, sticky='w', pady=5)
        self.course_var = tk.StringVar()
        course_combo = ttk.Combobox(
            fields_frame, textvariable=self.course_var, width=20)
        course_combo['values'] = ['Computer Science',
                                  'Business Administration', 'Engineering', 'Arts', 'Science']
        course_combo.grid(row=0, column=1, padx=5)

        tk.Label(fields_frame, text="Semester:", font=FONTS['body']).grid(
            row=0, column=2, sticky='w', padx=(20, 0), pady=5)
        self.semester_var = tk.StringVar()
        semester_combo = ttk.Combobox(fields_frame, textvariable=self.semester_var, values=[
                                      str(i) for i in range(1, 9)], width=10)
        semester_combo.grid(row=0, column=3, padx=5)

        # Fee amounts
        tk.Label(fields_frame, text="Tuition Fee:", font=FONTS['body']).grid(
            row=1, column=0, sticky='w', pady=5)
        self.tuition_fee_var = tk.StringVar(value="0")
        tk.Entry(fields_frame, textvariable=self.tuition_fee_var,
                 font=FONTS['body'], width=15).grid(row=1, column=1, padx=5)

        tk.Label(fields_frame, text="Library Fee:", font=FONTS['body']).grid(
            row=1, column=2, sticky='w', padx=(20, 0), pady=5)
        self.library_fee_var = tk.StringVar(value="0")
        tk.Entry(fields_frame, textvariable=self.library_fee_var,
                 font=FONTS['body'], width=15).grid(row=1, column=3, padx=5)

        tk.Label(fields_frame, text="Lab Fee:", font=FONTS['body']).grid(
            row=2, column=0, sticky='w', pady=5)
        self.lab_fee_var = tk.StringVar(value="0")
        tk.Entry(fields_frame, textvariable=self.lab_fee_var,
                 font=FONTS['body'], width=15).grid(row=2, column=1, padx=5)

        tk.Label(fields_frame, text="Other Fee:", font=FONTS['body']).grid(
            row=2, column=2, sticky='w', padx=(20, 0), pady=5)
        self.other_fee_var = tk.StringVar(value="0")
        tk.Entry(fields_frame, textvariable=self.other_fee_var,
                 font=FONTS['body'], width=15).grid(row=2, column=3, padx=5)

        # Academic Year
        tk.Label(fields_frame, text="Academic Year:", font=FONTS['body']).grid(
            row=3, column=0, sticky='w', pady=5)
        self.academic_year_var = tk.StringVar(
            value=self.get_current_academic_year())
        tk.Entry(fields_frame, textvariable=self.academic_year_var,
                 font=FONTS['body'], width=15).grid(row=3, column=1, padx=5)

        # Add structure button
        add_structure_btn = tk.Button(
            form_frame,
            text="Add Fee Structure",
            command=self.add_fee_structure,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            padx=20, pady=5
        )
        add_structure_btn.pack(pady=10)

        # Fee structures list
        list_frame = tk.LabelFrame(
            self.structure_frame, text="Fee Structures", font=FONTS['subheading'])
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)

        columns = ('Course', 'Semester', 'Tuition',
                   'Library', 'Lab', 'Other', 'Total', 'Year')
        self.structure_tree = ttk.Treeview(
            list_frame, columns=columns, show='headings', height=10)

        for col in columns:
            self.structure_tree.heading(col, text=col)
            self.structure_tree.column(col, width=80)

        scrollbar_structure = ttk.Scrollbar(
            list_frame, orient='vertical', command=self.structure_tree.yview)
        self.structure_tree.configure(yscrollcommand=scrollbar_structure.set)

        self.structure_tree.pack(
            side='left', fill='both', expand=True, padx=10, pady=5)
        scrollbar_structure.pack(side='right', fill='y', pady=5)

        self.load_fee_structures()

    def create_payment_tab(self):
        """Create payment recording tab"""
        # Payment form
        form_frame = tk.LabelFrame(
            self.payment_frame, text="Record Fee Payment", font=FONTS['subheading'])
        form_frame.pack(fill='x', padx=10, pady=10)

        fields_frame = tk.Frame(form_frame)
        fields_frame.pack(fill='x', padx=20, pady=10)

        # Student selection
        tk.Label(fields_frame, text="Student Roll No:", font=FONTS['body']).grid(
            row=0, column=0, sticky='w', pady=5)
        self.payment_student_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.payment_student_var,
                 font=FONTS['body'], width=20).grid(row=0, column=1, padx=5)

        # Get student info button
        get_student_btn = tk.Button(
            fields_frame,
            text="Get Student Info",
            command=self.get_student_fee_info,
            font=FONTS['body'],
            bg=COLORS['accent'],
            fg=COLORS['on_primary'],
            padx=10, pady=3
        )
        get_student_btn.grid(row=0, column=2, padx=10)

        # Student info display
        self.student_info_label = tk.Label(
            fields_frame, text="", font=FONTS['body'], fg=COLORS['primary'])
        self.student_info_label.grid(
            row=1, column=0, columnspan=3, sticky='w', pady=5)

        # Payment details
        tk.Label(fields_frame, text="Amount Paid:", font=FONTS['body']).grid(
            row=2, column=0, sticky='w', pady=5)
        self.amount_paid_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.amount_paid_var,
                 font=FONTS['body'], width=15).grid(row=2, column=1, padx=5)

        tk.Label(fields_frame, text="Payment Method:", font=FONTS['body']).grid(
            row=3, column=0, sticky='w', pady=5)
        self.payment_method_var = tk.StringVar()
        method_combo = ttk.Combobox(
            fields_frame, textvariable=self.payment_method_var, values=PAYMENT_METHODS, width=17)
        method_combo.grid(row=3, column=1, padx=5)

        tk.Label(fields_frame, text="Receipt Number:", font=FONTS['body']).grid(
            row=4, column=0, sticky='w', pady=5)
        self.receipt_number_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.receipt_number_var,
                 font=FONTS['body'], width=20).grid(row=4, column=1, padx=5)

        # Generate receipt number button
        gen_receipt_btn = tk.Button(
            fields_frame,
            text="Generate",
            command=self.generate_receipt_number,
            font=FONTS['body'],
            bg=COLORS['secondary'],
            fg=COLORS['on_primary'],
            padx=5, pady=3
        )
        gen_receipt_btn.grid(row=4, column=2, padx=5)

        # Remarks
        tk.Label(fields_frame, text="Remarks:", font=FONTS['body']).grid(
            row=5, column=0, sticky='w', pady=5)
        self.remarks_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.remarks_var, font=FONTS['body'], width=40).grid(
            row=5, column=1, columnspan=2, padx=5)

        # Record payment button
        record_payment_btn = tk.Button(
            form_frame,
            text="Record Payment",
            command=self.record_payment,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            padx=20, pady=5
        )
        record_payment_btn.pack(pady=10)

        # Hidden fee_id variable
        self.selected_fee_id = None

    def create_records_tab(self):
        """Create payment records tab"""
        # Search frame
        search_frame = tk.Frame(self.records_frame)
        search_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(search_frame, text="Search by Student Roll No:",
                 font=FONTS['body']).pack(side='left')
        self.search_payment_var = tk.StringVar()
        self.search_payment_var.trace('w', self.filter_payments)
        tk.Entry(search_frame, textvariable=self.search_payment_var,
                 font=FONTS['body'], width=20).pack(side='left', padx=5)

        # Payment records list
        list_frame = tk.LabelFrame(
            self.records_frame, text="Payment Records", font=FONTS['subheading'])
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)

        columns = ('Receipt No', 'Student', 'Amount',
                   'Date', 'Method', 'Remarks')
        self.payments_tree = ttk.Treeview(
            list_frame, columns=columns, show='headings', height=15)

        column_widths = {'Receipt No': 120, 'Student': 100,
                         'Amount': 80, 'Date': 100, 'Method': 100, 'Remarks': 150}
        for col in columns:
            self.payments_tree.heading(col, text=col)
            self.payments_tree.column(col, width=column_widths[col])

        scrollbar_payments = ttk.Scrollbar(
            list_frame, orient='vertical', command=self.payments_tree.yview)
        self.payments_tree.configure(yscrollcommand=scrollbar_payments.set)

        self.payments_tree.pack(side='left', fill='both',
                                expand=True, padx=10, pady=5)
        scrollbar_payments.pack(side='right', fill='y', pady=5)

        # Summary frame
        summary_frame = tk.Frame(self.records_frame, bg=COLORS['surface'])
        summary_frame.pack(fill='x', padx=10, pady=5)

        self.total_collected_label = tk.Label(
            summary_frame, text="Total Collected: $0.00", font=FONTS['subheading'], bg=COLORS['surface'])
        self.total_collected_label.pack(side='right', padx=10, pady=5)

    def get_current_academic_year(self):
        """Get current academic year"""
        current_year = datetime.now().year
        if datetime.now().month >= 7:
            return f"{current_year}-{current_year + 1}"
        else:
            return f"{current_year - 1}-{current_year}"

    def add_fee_structure(self):
        """Add fee structure"""
        try:
            course = self.course_var.get().strip()
            semester = self.semester_var.get().strip()
            tuition_fee = float(self.tuition_fee_var.get() or 0)
            library_fee = float(self.library_fee_var.get() or 0)
            lab_fee = float(self.lab_fee_var.get() or 0)
            other_fee = float(self.other_fee_var.get() or 0)
            academic_year = self.academic_year_var.get().strip()

            if not course or not semester or not academic_year:
                messagebox.showerror(
                    "Error", "Course, Semester, and Academic Year are required")
                return

            total_fee = tuition_fee + library_fee + lab_fee + other_fee

            # Check if structure already exists
            cursor = self.db_manager.execute_query(
                "SELECT COUNT(*) FROM fee_structure WHERE course = ? AND semester = ? AND academic_year = ?",
                (course, semester, academic_year)
            )
            if cursor.fetchone()[0] > 0:
                messagebox.showerror(
                    "Error", "Fee structure already exists for this course/semester/year")
                return

            # Insert fee structure
            self.db_manager.execute_and_commit("""
                INSERT INTO fee_structure (course, semester, tuition_fee, library_fee, lab_fee, other_fee, total_fee, academic_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (course, semester, tuition_fee, library_fee, lab_fee, other_fee, total_fee, academic_year))

            messagebox.showinfo("Success", "Fee structure added successfully")
            self.clear_structure_form()
            self.load_fee_structures()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid fee amounts")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to add fee structure: {str(e)}")

    def clear_structure_form(self):
        """Clear fee structure form"""
        self.course_var.set("")
        self.semester_var.set("")
        self.tuition_fee_var.set("0")
        self.library_fee_var.set("0")
        self.lab_fee_var.set("0")
        self.other_fee_var.set("0")

    def load_fee_structures(self):
        """Load fee structures"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT course, semester, tuition_fee, library_fee, lab_fee, other_fee, total_fee, academic_year
                FROM fee_structure ORDER BY course, semester
            """)

            # Clear existing items
            for item in self.structure_tree.get_children():
                self.structure_tree.delete(item)

            # Insert structures
            for structure in cursor.fetchall():
                self.structure_tree.insert('', 'end', values=(
                    structure['course'],
                    structure['semester'],
                    f"${structure['tuition_fee']:.2f}",
                    f"${structure['library_fee']:.2f}",
                    f"${structure['lab_fee']:.2f}",
                    f"${structure['other_fee']:.2f}",
                    f"${structure['total_fee']:.2f}",
                    structure['academic_year']
                ))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to load fee structures: {str(e)}")

    def get_student_fee_info(self):
        """Get student and fee information"""
        try:
            roll_number = self.payment_student_var.get().strip()
            if not roll_number:
                messagebox.showerror(
                    "Error", "Please enter student roll number")
                return

            # Get student info
            cursor = self.db_manager.execute_query(
                "SELECT student_id, first_name, last_name, course, semester FROM students WHERE roll_number = ?",
                (roll_number,)
            )
            student = cursor.fetchone()
            if not student:
                messagebox.showerror("Error", "Student not found")
                return

            # Get fee structure for student's course and semester
            cursor = self.db_manager.execute_query("""
                SELECT fee_id, total_fee, academic_year FROM fee_structure 
                WHERE course = ? AND semester = ? AND academic_year = ?
            """, (student['course'], student['semester'], self.get_current_academic_year()))

            fee_structure = cursor.fetchone()
            if fee_structure:
                self.selected_fee_id = fee_structure['fee_id']
                info_text = f"Student: {student['first_name']} {student['last_name']}, Course: {student['course']}, Semester: {student['semester']}, Total Fee: ${fee_structure['total_fee']:.2f}"
            else:
                self.selected_fee_id = None
                info_text = f"Student: {student['first_name']} {student['last_name']}, Course: {student['course']}, Semester: {student['semester']}, Fee structure not found"

            self.student_info_label.config(text=info_text)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to get student info: {str(e)}")

    def generate_receipt_number(self):
        """Generate receipt number"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        receipt_number = f"REC{timestamp}"
        self.receipt_number_var.set(receipt_number)

    def record_payment(self):
        """Record fee payment"""
        try:
            roll_number = self.payment_student_var.get().strip()
            amount_paid = self.amount_paid_var.get().strip()
            payment_method = self.payment_method_var.get().strip()
            receipt_number = self.receipt_number_var.get().strip()
            remarks = self.remarks_var.get().strip()

            if not all([roll_number, amount_paid, payment_method, receipt_number]):
                messagebox.showerror(
                    "Error", "All fields except remarks are required")
                return

            amount = float(amount_paid)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return

            # Get student ID
            cursor = self.db_manager.execute_query(
                "SELECT student_id FROM students WHERE roll_number = ?", (roll_number,))
            student = cursor.fetchone()
            if not student:
                messagebox.showerror("Error", "Student not found")
                return

            if not self.selected_fee_id:
                messagebox.showerror(
                    "Error", "Please get student fee information first")
                return

            # Check if receipt number already exists
            cursor = self.db_manager.execute_query(
                "SELECT COUNT(*) FROM fee_payments WHERE receipt_number = ?", (receipt_number,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "Receipt number already exists")
                return

            # Record payment
            self.db_manager.execute_and_commit("""
                INSERT INTO fee_payments (student_id, fee_id, amount_paid, payment_method, receipt_number, remarks)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (student['student_id'], self.selected_fee_id, amount, payment_method, receipt_number, remarks))

            messagebox.showinfo(
                "Success", f"Payment recorded successfully. Receipt: {receipt_number}")
            self.clear_payment_form()
            self.load_fee_records()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to record payment: {str(e)}")

    def clear_payment_form(self):
        """Clear payment form"""
        self.payment_student_var.set("")
        self.amount_paid_var.set("")
        self.payment_method_var.set("")
        self.receipt_number_var.set("")
        self.remarks_var.set("")
        self.student_info_label.config(text="")
        self.selected_fee_id = None

    def load_fee_records(self):
        """Load payment records"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT p.receipt_number, s.roll_number, p.amount_paid, p.payment_date, p.payment_method, p.remarks
                FROM fee_payments p
                JOIN students s ON p.student_id = s.student_id
                ORDER BY p.payment_date DESC
            """)

            # Clear existing items
            for item in self.payments_tree.get_children():
                self.payments_tree.delete(item)

            # Insert payments and calculate total
            self.all_payments = cursor.fetchall()
            total_collected = 0.0

            for payment in self.all_payments:
                self.payments_tree.insert('', 'end', values=(
                    payment['receipt_number'],
                    payment['roll_number'],
                    f"${payment['amount_paid']:.2f}",
                    payment['payment_date'],
                    payment['payment_method'],
                    payment['remarks'] or 'N/A'
                ))
                total_collected += payment['amount_paid']

            self.total_collected_label.config(
                text=f"Total Collected: ${total_collected:.2f}")

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to load payment records: {str(e)}")

    def filter_payments(self, *args):
        """Filter payments by student roll number"""
        search_term = self.search_payment_var.get().lower()

        # Clear existing items
        for item in self.payments_tree.get_children():
            self.payments_tree.delete(item)

        # Filter and insert matching payments
        total_filtered = 0.0
        for payment in self.all_payments:
            if search_term in payment['roll_number'].lower():
                self.payments_tree.insert('', 'end', values=(
                    payment['receipt_number'],
                    payment['roll_number'],
                    f"${payment['amount_paid']:.2f}",
                    payment['payment_date'],
                    payment['payment_method'],
                    payment['remarks'] or 'N/A'
                ))
                total_filtered += payment['amount_paid']

        self.total_collected_label.config(
            text=f"Filtered Total: ${total_filtered:.2f}")
