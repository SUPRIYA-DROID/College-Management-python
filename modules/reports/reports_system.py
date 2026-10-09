"""
Reports System
College Management System - ProjectsHUB

Simple but comprehensive reporting system for various college data.
"""

from config.settings import COLORS, FONTS
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import csv
import sys
from pathlib import Path

# Add config to path
sys.path.append(str(Path(__file__).parent.parent.parent))


class ReportsSystem:
    """Simple Reports Generation System"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager

        self.setup_ui()

    def setup_ui(self):
        """Create reports interface"""
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
            text="Reports & Analytics",
            font=FONTS['title'],
            bg=COLORS['surface'],
            fg=COLORS['on_surface']
        )
        title_label.pack(side='left', pady=15)

    def create_tabs(self):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)

        # Student reports tab
        self.student_reports_frame = tk.Frame(
            self.notebook, bg=COLORS['background'])
        self.notebook.add(self.student_reports_frame, text="Student Reports")
        self.create_student_reports_tab()

        # Financial reports tab
        self.financial_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.financial_frame, text="Financial Reports")
        self.create_financial_reports_tab()

        # Academic reports tab
        self.academic_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.academic_frame, text="Academic Reports")
        self.create_academic_reports_tab()

        # Library reports tab
        self.library_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.library_frame, text="Library Reports")
        self.create_library_reports_tab()

    def create_student_reports_tab(self):
        """Create student reports tab"""
        # Report options
        options_frame = tk.LabelFrame(
            self.student_reports_frame, text="Student Report Options", font=FONTS['subheading'])
        options_frame.pack(fill='x', padx=10, pady=10)

        btn_frame = tk.Frame(options_frame)
        btn_frame.pack(padx=20, pady=20)

        # All students report
        all_students_btn = tk.Button(
            btn_frame,
            text="All Students Report",
            command=self.generate_all_students_report,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        all_students_btn.grid(row=0, column=0, padx=10, pady=5)

        # Students by course
        course_students_btn = tk.Button(
            btn_frame,
            text="Students by Course",
            command=self.generate_course_wise_report,
            font=FONTS['button'],
            bg=COLORS['accent'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        course_students_btn.grid(row=0, column=1, padx=10, pady=5)

        # Student statistics
        stats_btn = tk.Button(
            btn_frame,
            text="Student Statistics",
            command=self.generate_student_statistics,
            font=FONTS['button'],
            bg=COLORS['secondary'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        stats_btn.grid(row=1, column=0, padx=10, pady=5)

        # Inactive students
        inactive_btn = tk.Button(
            btn_frame,
            text="Inactive Students",
            command=self.generate_inactive_students_report,
            font=FONTS['button'],
            bg=COLORS['warning'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        inactive_btn.grid(row=1, column=1, padx=10, pady=5)

        # Results display
        self.student_results_frame = tk.LabelFrame(
            self.student_reports_frame, text="Report Results", font=FONTS['subheading'])
        self.student_results_frame.pack(
            fill='both', expand=True, padx=10, pady=10)

        self.student_text = tk.Text(
            self.student_results_frame,
            font=FONTS['body'],
            wrap='word',
            state='disabled'
        )

        student_scrollbar = ttk.Scrollbar(
            self.student_results_frame, orient='vertical', command=self.student_text.yview)
        self.student_text.configure(yscrollcommand=student_scrollbar.set)

        self.student_text.pack(side='left', fill='both',
                               expand=True, padx=10, pady=10)
        student_scrollbar.pack(side='right', fill='y', pady=10)

        # Export button
        export_student_btn = tk.Button(
            self.student_results_frame,
            text="Export to CSV",
            command=lambda: self.export_report(
                self.current_student_data, "student_report"),
            font=FONTS['button'],
            bg=COLORS['success'],
            fg=COLORS['on_primary'],
            padx=15, pady=5
        )
        export_student_btn.pack(side='bottom', pady=10)

        self.current_student_data = []

    def create_financial_reports_tab(self):
        """Create financial reports tab"""
        # Date selection
        date_frame = tk.LabelFrame(
            self.financial_frame, text="Date Range Selection", font=FONTS['subheading'])
        date_frame.pack(fill='x', padx=10, pady=10)

        date_fields = tk.Frame(date_frame)
        date_fields.pack(padx=20, pady=10)

        tk.Label(date_fields, text="From Date:", font=FONTS['body']).grid(
            row=0, column=0, sticky='w', pady=5)
        self.from_date_var = tk.StringVar(
            value=(datetime.now().replace(day=1)).strftime('%Y-%m-%d'))
        tk.Entry(date_fields, textvariable=self.from_date_var,
                 font=FONTS['body'], width=15).grid(row=0, column=1, padx=5)

        tk.Label(date_fields, text="To Date:", font=FONTS['body']).grid(
            row=0, column=2, sticky='w', padx=(20, 0), pady=5)
        self.to_date_var = tk.StringVar(
            value=date.today().strftime('%Y-%m-%d'))
        tk.Entry(date_fields, textvariable=self.to_date_var,
                 font=FONTS['body'], width=15).grid(row=0, column=3, padx=5)

        # Report options
        options_frame = tk.LabelFrame(
            self.financial_frame, text="Financial Report Options", font=FONTS['subheading'])
        options_frame.pack(fill='x', padx=10, pady=10)

        btn_frame = tk.Frame(options_frame)
        btn_frame.pack(padx=20, pady=20)

        # Fee collection report
        collection_btn = tk.Button(
            btn_frame,
            text="Fee Collection Report",
            command=self.generate_fee_collection_report,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        collection_btn.grid(row=0, column=0, padx=10, pady=5)

        # Payment method analysis
        payment_method_btn = tk.Button(
            btn_frame,
            text="Payment Methods",
            command=self.generate_payment_method_report,
            font=FONTS['button'],
            bg=COLORS['accent'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        payment_method_btn.grid(row=0, column=1, padx=10, pady=5)

        # Outstanding fees
        outstanding_btn = tk.Button(
            btn_frame,
            text="Outstanding Fees",
            command=self.generate_outstanding_fees_report,
            font=FONTS['button'],
            bg=COLORS['danger'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        outstanding_btn.grid(row=1, column=0, padx=10, pady=5)

        # Monthly summary
        monthly_btn = tk.Button(
            btn_frame,
            text="Monthly Summary",
            command=self.generate_monthly_summary,
            font=FONTS['button'],
            bg=COLORS['secondary'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        monthly_btn.grid(row=1, column=1, padx=10, pady=5)

        # Results display
        self.financial_results_frame = tk.LabelFrame(
            self.financial_frame, text="Report Results", font=FONTS['subheading'])
        self.financial_results_frame.pack(
            fill='both', expand=True, padx=10, pady=10)

        self.financial_text = tk.Text(
            self.financial_results_frame,
            font=FONTS['body'],
            wrap='word',
            state='disabled'
        )

        financial_scrollbar = ttk.Scrollbar(
            self.financial_results_frame, orient='vertical', command=self.financial_text.yview)
        self.financial_text.configure(yscrollcommand=financial_scrollbar.set)

        self.financial_text.pack(
            side='left', fill='both', expand=True, padx=10, pady=10)
        financial_scrollbar.pack(side='right', fill='y', pady=10)

        # Export button
        export_financial_btn = tk.Button(
            self.financial_results_frame,
            text="Export to CSV",
            command=lambda: self.export_report(
                self.current_financial_data, "financial_report"),
            font=FONTS['button'],
            bg=COLORS['success'],
            fg=COLORS['on_primary'],
            padx=15, pady=5
        )
        export_financial_btn.pack(side='bottom', pady=10)

        self.current_financial_data = []

    def create_academic_reports_tab(self):
        """Create academic reports tab"""
        # Report options
        options_frame = tk.LabelFrame(
            self.academic_frame, text="Academic Report Options", font=FONTS['subheading'])
        options_frame.pack(fill='x', padx=10, pady=10)

        btn_frame = tk.Frame(options_frame)
        btn_frame.pack(padx=20, pady=20)

        # Class performance
        performance_btn = tk.Button(
            btn_frame,
            text="Class Performance",
            command=self.generate_class_performance_report,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        performance_btn.grid(row=0, column=0, padx=10, pady=5)

        # Subject analysis
        subject_btn = tk.Button(
            btn_frame,
            text="Subject Analysis",
            command=self.generate_subject_analysis_report,
            font=FONTS['button'],
            bg=COLORS['accent'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        subject_btn.grid(row=0, column=1, padx=10, pady=5)

        # Grade distribution
        grade_btn = tk.Button(
            btn_frame,
            text="Grade Distribution",
            command=self.generate_grade_distribution_report,
            font=FONTS['button'],
            bg=COLORS['secondary'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        grade_btn.grid(row=1, column=0, padx=10, pady=5)

        # Top performers
        top_performers_btn = tk.Button(
            btn_frame,
            text="Top Performers",
            command=self.generate_top_performers_report,
            font=FONTS['button'],
            bg=COLORS['warning'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        top_performers_btn.grid(row=1, column=1, padx=10, pady=5)

        # Results display
        self.academic_results_frame = tk.LabelFrame(
            self.academic_frame, text="Report Results", font=FONTS['subheading'])
        self.academic_results_frame.pack(
            fill='both', expand=True, padx=10, pady=10)

        self.academic_text = tk.Text(
            self.academic_results_frame,
            font=FONTS['body'],
            wrap='word',
            state='disabled'
        )

        academic_scrollbar = ttk.Scrollbar(
            self.academic_results_frame, orient='vertical', command=self.academic_text.yview)
        self.academic_text.configure(yscrollcommand=academic_scrollbar.set)

        self.academic_text.pack(side='left', fill='both',
                                expand=True, padx=10, pady=10)
        academic_scrollbar.pack(side='right', fill='y', pady=10)

        # Export button
        export_academic_btn = tk.Button(
            self.academic_results_frame,
            text="Export to CSV",
            command=lambda: self.export_report(
                self.current_academic_data, "academic_report"),
            font=FONTS['button'],
            bg=COLORS['success'],
            fg=COLORS['on_primary'],
            padx=15, pady=5
        )
        export_academic_btn.pack(side='bottom', pady=10)

        self.current_academic_data = []

    def create_library_reports_tab(self):
        """Create library reports tab"""
        # Report options
        options_frame = tk.LabelFrame(
            self.library_frame, text="Library Report Options", font=FONTS['subheading'])
        options_frame.pack(fill='x', padx=10, pady=10)

        btn_frame = tk.Frame(options_frame)
        btn_frame.pack(padx=20, pady=20)

        # Books inventory
        inventory_btn = tk.Button(
            btn_frame,
            text="Books Inventory",
            command=self.generate_books_inventory_report,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        inventory_btn.grid(row=0, column=0, padx=10, pady=5)

        # Issued books
        issued_btn = tk.Button(
            btn_frame,
            text="Currently Issued",
            command=self.generate_issued_books_report,
            font=FONTS['button'],
            bg=COLORS['accent'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        issued_btn.grid(row=0, column=1, padx=10, pady=5)

        # Overdue books
        overdue_btn = tk.Button(
            btn_frame,
            text="Overdue Books",
            command=self.generate_overdue_books_report,
            font=FONTS['button'],
            bg=COLORS['danger'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        overdue_btn.grid(row=1, column=0, padx=10, pady=5)

        # Popular books
        popular_btn = tk.Button(
            btn_frame,
            text="Popular Books",
            command=self.generate_popular_books_report,
            font=FONTS['button'],
            bg=COLORS['secondary'],
            fg=COLORS['on_primary'],
            width=20, padx=10, pady=8
        )
        popular_btn.grid(row=1, column=1, padx=10, pady=5)

        # Results display
        self.library_results_frame = tk.LabelFrame(
            self.library_frame, text="Report Results", font=FONTS['subheading'])
        self.library_results_frame.pack(
            fill='both', expand=True, padx=10, pady=10)

        self.library_text = tk.Text(
            self.library_results_frame,
            font=FONTS['body'],
            wrap='word',
            state='disabled'
        )

        library_scrollbar = ttk.Scrollbar(
            self.library_results_frame, orient='vertical', command=self.library_text.yview)
        self.library_text.configure(yscrollcommand=library_scrollbar.set)

        self.library_text.pack(side='left', fill='both',
                               expand=True, padx=10, pady=10)
        library_scrollbar.pack(side='right', fill='y', pady=10)

        # Export button
        export_library_btn = tk.Button(
            self.library_results_frame,
            text="Export to CSV",
            command=lambda: self.export_report(
                self.current_library_data, "library_report"),
            font=FONTS['button'],
            bg=COLORS['success'],
            fg=COLORS['on_primary'],
            padx=15, pady=5
        )
        export_library_btn.pack(side='bottom', pady=10)

        self.current_library_data = []

    # Student Reports Methods
    def generate_all_students_report(self):
        """Generate report of all students"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT roll_number, first_name, last_name, course, semester, 
                       phone_number, email, status, admission_date
                FROM students ORDER BY course, semester, roll_number
            """)

            students = cursor.fetchall()

            report = []
            report.append("ALL STUDENTS REPORT")
            report.append("=" * 60)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"Total Students: {len(students)}")
            report.append("")

            current_course = ""
            for student in students:
                if student['course'] != current_course:
                    current_course = student['course']
                    report.append(f"\n{current_course.upper()}:")
                    report.append("-" * 40)

                name = f"{student['first_name']} {student['last_name']}"
                report.append(
                    f"{student['roll_number']:<12} {name:<25} Sem {student['semester']:<2} {student['status']}")

            self.display_student_report("\n".join(report))

            # Prepare data for export
            self.current_student_data = [
                ['Roll Number', 'Name', 'Course', 'Semester',
                    'Phone', 'Email', 'Status', 'Admission Date']
            ]
            for student in students:
                self.current_student_data.append([
                    student['roll_number'],
                    f"{student['first_name']} {student['last_name']}",
                    student['course'],
                    student['semester'],
                    student['phone_number'] or 'N/A',
                    student['email'] or 'N/A',
                    student['status'],
                    student['admission_date']
                ])

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    def generate_course_wise_report(self):
        """Generate course-wise student distribution report"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT course, semester, COUNT(*) as count, 
                       SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_count
                FROM students 
                GROUP BY course, semester
                ORDER BY course, semester
            """)

            course_data = cursor.fetchall()

            report = []
            report.append("COURSE-WISE STUDENT DISTRIBUTION")
            report.append("=" * 60)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("")

            current_course = ""
            course_total = 0
            course_active = 0

            for data in course_data:
                if data['course'] != current_course:
                    if current_course:
                        report.append(
                            f"Course Total: {course_total} (Active: {course_active})")
                        report.append("")

                    current_course = data['course']
                    report.append(f"{current_course.upper()}:")
                    report.append("-" * 30)
                    course_total = 0
                    course_active = 0

                report.append(
                    f"  Semester {data['semester']}: {data['count']} students (Active: {data['active_count']})")
                course_total += data['count']
                course_active += data['active_count']

            if current_course:
                report.append(
                    f"Course Total: {course_total} (Active: {course_active})")

            self.display_student_report("\n".join(report))

            # Prepare data for export
            self.current_student_data = [
                ['Course', 'Semester', 'Total Students', 'Active Students']
            ]
            for data in course_data:
                self.current_student_data.append([
                    data['course'], data['semester'], data['count'], data['active_count']
                ])

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    def generate_student_statistics(self):
        """Generate student statistics report"""
        try:
            # Get overall statistics
            cursor = self.db_manager.execute_query(
                "SELECT COUNT(*) as total FROM students")
            total_students = cursor.fetchone()['total']

            cursor = self.db_manager.execute_query(
                "SELECT status, COUNT(*) as count FROM students GROUP BY status")
            status_stats = cursor.fetchall()

            cursor = self.db_manager.execute_query(
                "SELECT course, COUNT(*) as count FROM students GROUP BY course ORDER BY count DESC")
            course_stats = cursor.fetchall()

            cursor = self.db_manager.execute_query(
                "SELECT gender, COUNT(*) as count FROM students WHERE gender IS NOT NULL GROUP BY gender")
            gender_stats = cursor.fetchall()

            report = []
            report.append("STUDENT STATISTICS REPORT")
            report.append("=" * 60)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("")

            report.append(f"TOTAL STUDENTS: {total_students}")
            report.append("")

            report.append("BY STATUS:")
            for stat in status_stats:
                percentage = (stat['count'] / total_students) * 100
                report.append(
                    f"  {stat['status'].title()}: {stat['count']} ({percentage:.1f}%)")
            report.append("")

            report.append("BY COURSE:")
            for stat in course_stats:
                percentage = (stat['count'] / total_students) * 100
                report.append(
                    f"  {stat['course']}: {stat['count']} ({percentage:.1f}%)")
            report.append("")

            if gender_stats:
                report.append("BY GENDER:")
                for stat in gender_stats:
                    percentage = (stat['count'] / total_students) * 100
                    report.append(
                        f"  {stat['gender']}: {stat['count']} ({percentage:.1f}%)")

            self.display_student_report("\n".join(report))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate statistics: {str(e)}")

    def generate_inactive_students_report(self):
        """Generate inactive students report"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT roll_number, first_name, last_name, course, semester, status, admission_date
                FROM students WHERE status != 'active'
                ORDER BY status, course, roll_number
            """)

            inactive_students = cursor.fetchall()

            report = []
            report.append("INACTIVE STUDENTS REPORT")
            report.append("=" * 60)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"Total Inactive Students: {len(inactive_students)}")
            report.append("")

            current_status = ""
            for student in inactive_students:
                if student['status'] != current_status:
                    current_status = student['status']
                    report.append(f"\n{current_status.upper()} STUDENTS:")
                    report.append("-" * 30)

                name = f"{student['first_name']} {student['last_name']}"
                report.append(
                    f"{student['roll_number']:<12} {name:<25} {student['course']}")

            self.display_student_report("\n".join(report))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    # Financial Reports Methods
    def generate_fee_collection_report(self):
        """Generate fee collection report"""
        try:
            from_date = self.from_date_var.get()
            to_date = self.to_date_var.get()

            cursor = self.db_manager.execute_query("""
                SELECT p.payment_date, s.roll_number, s.first_name, s.last_name,
                       p.amount_paid, p.payment_method, p.receipt_number
                FROM fee_payments p
                JOIN students s ON p.student_id = s.student_id
                WHERE p.payment_date BETWEEN ? AND ?
                ORDER BY p.payment_date DESC
            """, (from_date, to_date))

            payments = cursor.fetchall()
            total_collected = sum(p['amount_paid'] for p in payments)

            report = []
            report.append("FEE COLLECTION REPORT")
            report.append("=" * 60)
            report.append(f"Period: {from_date} to {to_date}")
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"Total Payments: {len(payments)}")
            report.append(f"Total Amount: ${total_collected:.2f}")
            report.append("")

            if payments:
                report.append("PAYMENT DETAILS:")
                report.append("-" * 80)
                report.append(
                    f"{'Date':<12} {'Receipt':<15} {'Student':<20} {'Amount':<10} {'Method'}")
                report.append("-" * 80)

                for payment in payments:
                    student_name = f"{payment['first_name']} {payment['last_name']}"
                    report.append(f"{payment['payment_date']:<12} {payment['receipt_number']:<15} "
                                  f"{student_name:<20} ${payment['amount_paid']:<9.2f} {payment['payment_method']}")
            else:
                report.append("No payments found in the selected period.")

            self.display_financial_report("\n".join(report))

            # Prepare data for export
            self.current_financial_data = [
                ['Date', 'Receipt Number', 'Student Name',
                    'Roll Number', 'Amount', 'Payment Method']
            ]
            for payment in payments:
                self.current_financial_data.append([
                    payment['payment_date'],
                    payment['receipt_number'],
                    f"{payment['first_name']} {payment['last_name']}",
                    payment['roll_number'],
                    payment['amount_paid'],
                    payment['payment_method']
                ])

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    def generate_payment_method_report(self):
        """Generate payment method analysis report"""
        try:
            from_date = self.from_date_var.get()
            to_date = self.to_date_var.get()

            cursor = self.db_manager.execute_query("""
                SELECT payment_method, COUNT(*) as count, SUM(amount_paid) as total
                FROM fee_payments
                WHERE payment_date BETWEEN ? AND ?
                GROUP BY payment_method
                ORDER BY total DESC
            """, (from_date, to_date))

            method_stats = cursor.fetchall()
            total_amount = sum(stat['total'] for stat in method_stats)

            report = []
            report.append("PAYMENT METHOD ANALYSIS")
            report.append("=" * 60)
            report.append(f"Period: {from_date} to {to_date}")
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"Total Amount: ${total_amount:.2f}")
            report.append("")

            if method_stats:
                report.append("BY PAYMENT METHOD:")
                report.append("-" * 50)

                for stat in method_stats:
                    percentage = (stat['total'] / total_amount) * \
                        100 if total_amount > 0 else 0
                    report.append(f"{stat['payment_method']:<15} {stat['count']:>3} payments  "
                                  f"${stat['total']:>8.2f} ({percentage:>5.1f}%)")
            else:
                report.append("No payments found in the selected period.")

            self.display_financial_report("\n".join(report))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    def generate_outstanding_fees_report(self):
        """Generate outstanding fees report"""
        try:
            # This is a simplified version - in a real system, you'd track expected vs paid amounts
            cursor = self.db_manager.execute_query("""
                SELECT s.roll_number, s.first_name, s.last_name, s.course, s.semester,
                       COALESCE(SUM(p.amount_paid), 0) as paid_amount,
                       COALESCE(fs.total_fee, 0) as expected_amount
                FROM students s
                LEFT JOIN fee_payments p ON s.student_id = p.student_id
                LEFT JOIN fee_structure fs ON s.course = fs.course AND s.semester = fs.semester
                WHERE s.status = 'active'
                GROUP BY s.student_id, s.roll_number, s.first_name, s.last_name, 
                         s.course, s.semester, fs.total_fee
                HAVING COALESCE(fs.total_fee, 0) > COALESCE(SUM(p.amount_paid), 0)
                ORDER BY s.course, s.roll_number
            """)

            outstanding = cursor.fetchall()

            report = []
            report.append("OUTSTANDING FEES REPORT")
            report.append("=" * 60)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(
                f"Students with Outstanding Fees: {len(outstanding)}")
            report.append("")

            if outstanding:
                total_outstanding = 0
                report.append("OUTSTANDING FEE DETAILS:")
                report.append("-" * 70)
                report.append(
                    f"{'Roll No':<10} {'Student Name':<20} {'Expected':<10} {'Paid':<10} {'Outstanding'}")
                report.append("-" * 70)

                for student in outstanding:
                    expected = student['expected_amount'] or 0
                    paid = student['paid_amount'] or 0
                    outstanding_amount = expected - paid
                    total_outstanding += outstanding_amount

                    name = f"{student['first_name']} {student['last_name']}"
                    report.append(f"{student['roll_number']:<10} {name:<20} "
                                  f"${expected:<9.2f} ${paid:<9.2f} ${outstanding_amount:.2f}")

                report.append("-" * 70)
                report.append(
                    f"{'TOTAL OUTSTANDING:':<50} ${total_outstanding:.2f}")
            else:
                report.append("No outstanding fees found.")

            self.display_financial_report("\n".join(report))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    def generate_monthly_summary(self):
        """Generate monthly financial summary"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT strftime('%Y-%m', payment_date) as month,
                       COUNT(*) as payment_count,
                       SUM(amount_paid) as total_amount
                FROM fee_payments
                GROUP BY strftime('%Y-%m', payment_date)
                ORDER BY month DESC
                LIMIT 12
            """)

            monthly_data = cursor.fetchall()

            report = []
            report.append("MONTHLY FINANCIAL SUMMARY")
            report.append("=" * 60)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("Last 12 Months Collection Summary")
            report.append("")

            if monthly_data:
                total_yearly = sum(data['total_amount']
                                   for data in monthly_data)
                report.append(
                    f"{'Month':<10} {'Payments':<10} {'Amount':<12} {'% of Total'}")
                report.append("-" * 45)

                for data in monthly_data:
                    percentage = (
                        data['total_amount'] / total_yearly) * 100 if total_yearly > 0 else 0
                    report.append(f"{data['month']:<10} {data['payment_count']:<10} "
                                  f"${data['total_amount']:<11.2f} {percentage:>6.1f}%")

                report.append("-" * 45)
                report.append(f"{'TOTAL:':<10} {sum(d['payment_count'] for d in monthly_data):<10} "
                              f"${total_yearly:<11.2f}")
            else:
                report.append("No payment data found.")

            self.display_financial_report("\n".join(report))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    # Academic Reports Methods (simplified implementations)
    def generate_class_performance_report(self):
        """Generate class performance report"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT s.course, s.semester, 
                       AVG(CAST(m.obtained_marks AS FLOAT) / m.max_marks * 100) as avg_percentage,
                       COUNT(DISTINCT s.student_id) as student_count,
                       COUNT(m.marksheet_id) as total_subjects
                FROM students s
                JOIN marksheets m ON s.student_id = m.student_id
                GROUP BY s.course, s.semester
                ORDER BY s.course, s.semester
            """)

            performance_data = cursor.fetchall()

            report = []
            report.append("CLASS PERFORMANCE REPORT")
            report.append("=" * 60)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("")

            if performance_data:
                report.append(
                    f"{'Course':<20} {'Sem':<4} {'Students':<8} {'Subjects':<8} {'Avg %'}")
                report.append("-" * 55)

                for data in performance_data:
                    report.append(f"{data['course']:<20} {data['semester']:<4} "
                                  f"{data['student_count']:<8} {data['total_subjects']:<8} "
                                  f"{data['avg_percentage']:.1f}%")
            else:
                report.append("No academic data found.")

            self.display_academic_report("\n".join(report))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    def generate_subject_analysis_report(self):
        """Generate subject-wise analysis report"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT subject_name,
                       COUNT(*) as student_count,
                       AVG(CAST(obtained_marks AS FLOAT) / max_marks * 100) as avg_percentage,
                       MAX(CAST(obtained_marks AS FLOAT) / max_marks * 100) as max_percentage,
                       MIN(CAST(obtained_marks AS FLOAT) / max_marks * 100) as min_percentage
                FROM marksheets
                GROUP BY subject_name
                ORDER BY avg_percentage DESC
            """)

            subject_data = cursor.fetchall()

            report = []
            report.append("SUBJECT-WISE ANALYSIS REPORT")
            report.append("=" * 70)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("")

            if subject_data:
                report.append(
                    f"{'Subject':<25} {'Students':<8} {'Avg %':<7} {'Max %':<7} {'Min %'}")
                report.append("-" * 70)

                for data in subject_data:
                    report.append(f"{data['subject_name']:<25} {data['student_count']:<8} "
                                  f"{data['avg_percentage']:<6.1f}% {data['max_percentage']:<6.1f}% "
                                  f"{data['min_percentage']:.1f}%")
            else:
                report.append("No academic data found.")

            self.display_academic_report("\n".join(report))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    def generate_grade_distribution_report(self):
        """Generate grade distribution report"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT grade, COUNT(*) as count
                FROM marksheets
                GROUP BY grade
                ORDER BY 
                    CASE grade 
                        WHEN 'A+' THEN 1 
                        WHEN 'A' THEN 2 
                        WHEN 'B+' THEN 3 
                        WHEN 'B' THEN 4 
                        WHEN 'C+' THEN 5 
                        WHEN 'C' THEN 6 
                        WHEN 'D' THEN 7 
                        WHEN 'F' THEN 8 
                    END
            """)

            grade_data = cursor.fetchall()
            total_grades = sum(data['count'] for data in grade_data)

            report = []
            report.append("GRADE DISTRIBUTION REPORT")
            report.append("=" * 60)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"Total Assessments: {total_grades}")
            report.append("")

            if grade_data:
                report.append(f"{'Grade':<6} {'Count':<8} {'Percentage'}")
                report.append("-" * 25)

                for data in grade_data:
                    percentage = (data['count'] / total_grades) * 100
                    bar = '█' * int(percentage / 2)  # Simple bar chart
                    report.append(
                        f"{data['grade']:<6} {data['count']:<8} {percentage:>6.1f}% {bar}")
            else:
                report.append("No grade data found.")

            self.display_academic_report("\n".join(report))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    def generate_top_performers_report(self):
        """Generate top performers report"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT s.roll_number, s.first_name, s.last_name, s.course, s.semester,
                       AVG(CAST(m.obtained_marks AS FLOAT) / m.max_marks * 100) as avg_percentage,
                       COUNT(m.marksheet_id) as subject_count
                FROM students s
                JOIN marksheets m ON s.student_id = m.student_id
                GROUP BY s.student_id
                HAVING COUNT(m.marksheet_id) >= 3  -- At least 3 subjects
                ORDER BY avg_percentage DESC
                LIMIT 20
            """)

            top_performers = cursor.fetchall()

            report = []
            report.append("TOP PERFORMERS REPORT")
            report.append("=" * 70)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("Top 20 Students by Average Performance")
            report.append("")

            if top_performers:
                report.append(
                    f"{'Rank':<4} {'Roll No':<10} {'Name':<20} {'Course':<15} {'Avg %'}")
                report.append("-" * 70)

                for i, student in enumerate(top_performers, 1):
                    name = f"{student['first_name']} {student['last_name']}"
                    report.append(f"{i:<4} {student['roll_number']:<10} {name:<20} "
                                  f"{student['course']:<15} {student['avg_percentage']:.1f}%")
            else:
                report.append("No performance data found.")

            self.display_academic_report("\n".join(report))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    # Library Reports Methods (simplified implementations)
    def generate_books_inventory_report(self):
        """Generate books inventory report"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT title, author, category, total_copies, available_copies,
                       (total_copies - available_copies) as issued_copies
                FROM library_books
                ORDER BY category, title
            """)

            books = cursor.fetchall()

            report = []
            report.append("BOOKS INVENTORY REPORT")
            report.append("=" * 80)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"Total Books: {len(books)}")
            report.append("")

            if books:
                current_category = ""
                for book in books:
                    if book['category'] != current_category:
                        current_category = book['category'] or "General"
                        report.append(f"\n{current_category.upper()}:")
                        report.append("-" * 50)

                    issued = book['issued_copies']
                    status = f"Available: {book['available_copies']}, Issued: {issued}"
                    report.append(
                        f"{book['title']:<30} by {book['author']:<20} ({status})")
            else:
                report.append("No books found in inventory.")

            self.display_library_report("\n".join(report))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    def generate_issued_books_report(self):
        """Generate currently issued books report"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT b.title, b.author, s.roll_number, s.first_name, s.last_name,
                       t.issue_date, t.due_date,
                       CASE 
                           WHEN DATE(t.due_date) < DATE('now') THEN 'Overdue'
                           ELSE 'On Time'
                       END as status
                FROM library_transactions t
                JOIN library_books b ON t.book_id = b.book_id
                JOIN students s ON t.student_id = s.student_id
                WHERE t.status = 'issued'
                ORDER BY t.due_date
            """)

            issued_books = cursor.fetchall()

            report = []
            report.append("CURRENTLY ISSUED BOOKS REPORT")
            report.append("=" * 80)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"Total Issued Books: {len(issued_books)}")
            report.append("")

            if issued_books:
                overdue_count = sum(
                    1 for book in issued_books if book['status'] == 'Overdue')
                report.append(f"Overdue Books: {overdue_count}")
                report.append("")

                report.append(
                    f"{'Book Title':<25} {'Student':<15} {'Issue Date':<12} {'Due Date':<12} {'Status'}")
                report.append("-" * 80)

                for book in issued_books:
                    student_name = f"{book['first_name']} {book['last_name']}"
                    report.append(f"{book['title'][:24]:<25} {student_name[:14]:<15} "
                                  f"{book['issue_date']:<12} {book['due_date']:<12} {book['status']}")
            else:
                report.append("No books currently issued.")

            self.display_library_report("\n".join(report))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    def generate_overdue_books_report(self):
        """Generate overdue books report"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT b.title, b.author, s.roll_number, s.first_name, s.last_name,
                       t.issue_date, t.due_date,
                       (julianday('now') - julianday(t.due_date)) as days_overdue
                FROM library_transactions t
                JOIN library_books b ON t.book_id = b.book_id
                JOIN students s ON t.student_id = s.student_id
                WHERE t.status = 'issued' AND DATE(t.due_date) < DATE('now')
                ORDER BY days_overdue DESC
            """)

            overdue_books = cursor.fetchall()

            report = []
            report.append("OVERDUE BOOKS REPORT")
            report.append("=" * 80)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"Total Overdue Books: {len(overdue_books)}")
            report.append("")

            if overdue_books:
                total_fine = sum(
                    # $2 per day
                    int(book['days_overdue']) * 2 for book in overdue_books)
                report.append(f"Total Potential Fine: ${total_fine:.2f}")
                report.append("")

                report.append(
                    f"{'Book Title':<25} {'Student':<15} {'Due Date':<12} {'Days Over':<10} {'Fine'}")
                report.append("-" * 80)

                for book in overdue_books:
                    student_name = f"{book['first_name']} {book['last_name']}"
                    days_over = int(book['days_overdue'])
                    fine = days_over * 2
                    report.append(f"{book['title'][:24]:<25} {student_name[:14]:<15} "
                                  f"{book['due_date']:<12} {days_over:<10} ${fine:.2f}")
            else:
                report.append("No overdue books found.")

            self.display_library_report("\n".join(report))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    def generate_popular_books_report(self):
        """Generate popular books report"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT b.title, b.author, b.category,
                       COUNT(t.transaction_id) as issue_count
                FROM library_books b
                LEFT JOIN library_transactions t ON b.book_id = t.book_id
                GROUP BY b.book_id
                ORDER BY issue_count DESC, b.title
                LIMIT 20
            """)

            popular_books = cursor.fetchall()

            report = []
            report.append("POPULAR BOOKS REPORT")
            report.append("=" * 80)
            report.append(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("Top 20 Most Issued Books")
            report.append("")

            if popular_books:
                report.append(
                    f"{'Rank':<4} {'Title':<30} {'Author':<20} {'Issues'}")
                report.append("-" * 70)

                for i, book in enumerate(popular_books, 1):
                    report.append(f"{i:<4} {book['title'][:29]:<30} "
                                  f"{book['author'][:19]:<20} {book['issue_count']}")
            else:
                report.append("No book data found.")

            self.display_library_report("\n".join(report))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to generate report: {str(e)}")

    # Display Methods
    def display_student_report(self, report_text):
        """Display student report in text widget"""
        self.student_text.config(state='normal')
        self.student_text.delete(1.0, tk.END)
        self.student_text.insert(tk.END, report_text)
        self.student_text.config(state='disabled')

    def display_financial_report(self, report_text):
        """Display financial report in text widget"""
        self.financial_text.config(state='normal')
        self.financial_text.delete(1.0, tk.END)
        self.financial_text.insert(tk.END, report_text)
        self.financial_text.config(state='disabled')

    def display_academic_report(self, report_text):
        """Display academic report in text widget"""
        self.academic_text.config(state='normal')
        self.academic_text.delete(1.0, tk.END)
        self.academic_text.insert(tk.END, report_text)
        self.academic_text.config(state='disabled')

    def display_library_report(self, report_text):
        """Display library report in text widget"""
        self.library_text.config(state='normal')
        self.library_text.delete(1.0, tk.END)
        self.library_text.insert(tk.END, report_text)
        self.library_text.config(state='disabled')

    def export_report(self, data, report_type):
        """Export report data to CSV"""
        if not data:
            messagebox.showwarning("Warning", "No data to export")
            return

        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialname=f"{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )

            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for row in data:
                        writer.writerow(row)

                messagebox.showinfo(
                    "Success", f"Report exported to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
