"""
Library Management System
College Management System - ProjectsHUB

Simple but fully functional library management with book operations.
"""

from config.settings import COLORS, FONTS, BOOK_CATEGORIES
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
import sys
from pathlib import Path

# Add config to path
sys.path.append(str(Path(__file__).parent.parent.parent))


class LibrarySystem:
    """Simple Library Management System"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager

        self.setup_ui()
        self.load_books()

    def setup_ui(self):
        """Create library interface"""
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
            text="Library Management",
            font=FONTS['title'],
            bg=COLORS['surface'],
            fg=COLORS['on_surface']
        )
        title_label.pack(side='left', pady=15)

    def create_tabs(self):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)

        # Books tab
        self.books_frame = tk.Frame(self.notebook, bg=COLORS['background'])
        self.notebook.add(self.books_frame, text="Books")
        self.create_books_tab()

        # Transactions tab
        self.transactions_frame = tk.Frame(
            self.notebook, bg=COLORS['background'])
        self.notebook.add(self.transactions_frame, text="Issue/Return")
        self.create_transactions_tab()

    def create_books_tab(self):
        """Create books management tab"""
        # Add book form
        form_frame = tk.LabelFrame(
            self.books_frame, text="Add New Book", font=FONTS['subheading'])
        form_frame.pack(fill='x', padx=10, pady=10)

        # Form fields
        fields_frame = tk.Frame(form_frame)
        fields_frame.pack(fill='x', padx=20, pady=10)

        # Title
        tk.Label(fields_frame, text="Title:", font=FONTS['body']).grid(
            row=0, column=0, sticky='w', pady=5)
        self.title_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.title_var,
                 font=FONTS['body'], width=25).grid(row=0, column=1, padx=5)

        # Author
        tk.Label(fields_frame, text="Author:", font=FONTS['body']).grid(
            row=0, column=2, sticky='w', padx=(20, 0), pady=5)
        self.author_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.author_var,
                 font=FONTS['body'], width=25).grid(row=0, column=3, padx=5)

        # ISBN
        tk.Label(fields_frame, text="ISBN:", font=FONTS['body']).grid(
            row=1, column=0, sticky='w', pady=5)
        self.isbn_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.isbn_var,
                 font=FONTS['body'], width=25).grid(row=1, column=1, padx=5)

        # Category
        tk.Label(fields_frame, text="Category:", font=FONTS['body']).grid(
            row=1, column=2, sticky='w', padx=(20, 0), pady=5)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(
            fields_frame, textvariable=self.category_var, values=BOOK_CATEGORIES, width=22)
        category_combo.grid(row=1, column=3, padx=5)

        # Copies
        tk.Label(fields_frame, text="Total Copies:", font=FONTS['body']).grid(
            row=2, column=0, sticky='w', pady=5)
        self.copies_var = tk.StringVar(value="1")
        tk.Entry(fields_frame, textvariable=self.copies_var,
                 font=FONTS['body'], width=10).grid(row=2, column=1, sticky='w', padx=5)

        # Add button
        add_btn = tk.Button(
            form_frame,
            text="Add Book",
            command=self.add_book,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            padx=20, pady=5
        )
        add_btn.pack(pady=10)

        # Books list
        list_frame = tk.LabelFrame(
            self.books_frame, text="Books List", font=FONTS['subheading'])
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Search
        search_frame = tk.Frame(list_frame)
        search_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(search_frame, text="Search:",
                 font=FONTS['body']).pack(side='left')
        self.book_search_var = tk.StringVar()
        self.book_search_var.trace('w', self.filter_books)
        tk.Entry(search_frame, textvariable=self.book_search_var,
                 font=FONTS['body'], width=30).pack(side='left', padx=5)

        # Books treeview
        columns = ('Title', 'Author', 'ISBN', 'Category', 'Available', 'Total')
        self.books_tree = ttk.Treeview(
            list_frame, columns=columns, show='headings', height=12)

        for col in columns:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=120)

        scrollbar_books = ttk.Scrollbar(
            list_frame, orient='vertical', command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=scrollbar_books.set)

        self.books_tree.pack(side='left', fill='both',
                             expand=True, padx=10, pady=5)
        scrollbar_books.pack(side='right', fill='y', pady=5)

        # Delete button
        delete_btn = tk.Button(
            list_frame,
            text="Delete Selected Book",
            command=self.delete_book,
            font=FONTS['button'],
            bg=COLORS['danger'],
            fg=COLORS['on_primary'],
            padx=15, pady=5
        )
        delete_btn.pack(pady=5)

    def create_transactions_tab(self):
        """Create issue/return transactions tab"""
        # Issue book section
        issue_frame = tk.LabelFrame(
            self.transactions_frame, text="Issue Book", font=FONTS['subheading'])
        issue_frame.pack(fill='x', padx=10, pady=10)

        issue_fields = tk.Frame(issue_frame)
        issue_fields.pack(fill='x', padx=20, pady=10)

        # Student roll number
        tk.Label(issue_fields, text="Student Roll No:", font=FONTS['body']).grid(
            row=0, column=0, sticky='w', pady=5)
        self.student_roll_var = tk.StringVar()
        tk.Entry(issue_fields, textvariable=self.student_roll_var,
                 font=FONTS['body'], width=20).grid(row=0, column=1, padx=5)

        # Book ID
        tk.Label(issue_fields, text="Book ID:", font=FONTS['body']).grid(
            row=0, column=2, sticky='w', padx=(20, 0), pady=5)
        self.book_id_var = tk.StringVar()
        tk.Entry(issue_fields, textvariable=self.book_id_var,
                 font=FONTS['body'], width=15).grid(row=0, column=3, padx=5)

        # Issue button
        issue_btn = tk.Button(
            issue_frame,
            text="Issue Book",
            command=self.issue_book,
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['on_primary'],
            padx=20, pady=5
        )
        issue_btn.pack(pady=10)

        # Return book section
        return_frame = tk.LabelFrame(
            self.transactions_frame, text="Return Book", font=FONTS['subheading'])
        return_frame.pack(fill='x', padx=10, pady=10)

        return_fields = tk.Frame(return_frame)
        return_fields.pack(fill='x', padx=20, pady=10)

        # Transaction ID for return
        tk.Label(return_fields, text="Transaction ID:", font=FONTS['body']).grid(
            row=0, column=0, sticky='w', pady=5)
        self.transaction_id_var = tk.StringVar()
        tk.Entry(return_fields, textvariable=self.transaction_id_var,
                 font=FONTS['body'], width=15).grid(row=0, column=1, padx=5)

        # Return button
        return_btn = tk.Button(
            return_frame,
            text="Return Book",
            command=self.return_book,
            font=FONTS['button'],
            bg=COLORS['accent'],
            fg=COLORS['on_primary'],
            padx=20, pady=5
        )
        return_btn.pack(pady=10)

        # Active transactions list
        trans_list_frame = tk.LabelFrame(
            self.transactions_frame, text="Active Transactions", font=FONTS['subheading'])
        trans_list_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Transactions treeview
        trans_columns = ('ID', 'Student', 'Book Title',
                         'Issue Date', 'Due Date', 'Status')
        self.trans_tree = ttk.Treeview(
            trans_list_frame, columns=trans_columns, show='headings', height=8)

        for col in trans_columns:
            self.trans_tree.heading(col, text=col)
            self.trans_tree.column(col, width=100)

        scrollbar_trans = ttk.Scrollbar(
            trans_list_frame, orient='vertical', command=self.trans_tree.yview)
        self.trans_tree.configure(yscrollcommand=scrollbar_trans.set)

        self.trans_tree.pack(side='left', fill='both',
                             expand=True, padx=10, pady=5)
        scrollbar_trans.pack(side='right', fill='y', pady=5)

        # Load transactions
        self.load_transactions()

    def add_book(self):
        """Add new book to library"""
        try:
            title = self.title_var.get().strip()
            author = self.author_var.get().strip()
            isbn = self.isbn_var.get().strip()
            category = self.category_var.get().strip()
            copies = self.copies_var.get().strip()

            if not title or not author:
                messagebox.showerror("Error", "Title and Author are required")
                return

            if copies and not copies.isdigit():
                messagebox.showerror("Error", "Copies must be a number")
                return

            total_copies = int(copies) if copies else 1

            # Check if ISBN already exists
            if isbn:
                cursor = self.db_manager.execute_query(
                    "SELECT COUNT(*) FROM library_books WHERE isbn = ?", (isbn,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Error", "ISBN already exists")
                    return

            # Insert book
            self.db_manager.execute_and_commit("""
                INSERT INTO library_books (title, author, isbn, category, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, author, isbn, category, total_copies, total_copies))

            messagebox.showinfo("Success", "Book added successfully")
            self.clear_book_form()
            self.load_books()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {str(e)}")

    def clear_book_form(self):
        """Clear book form fields"""
        self.title_var.set("")
        self.author_var.set("")
        self.isbn_var.set("")
        self.category_var.set("")
        self.copies_var.set("1")

    def load_books(self):
        """Load books from database"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT book_id, title, author, isbn, category, available_copies, total_copies
                FROM library_books ORDER BY title
            """)

            # Clear existing items
            for item in self.books_tree.get_children():
                self.books_tree.delete(item)

            # Insert books
            self.all_books = cursor.fetchall()
            for book in self.all_books:
                self.books_tree.insert('', 'end', values=(
                    book['title'],
                    book['author'],
                    book['isbn'] or 'N/A',
                    book['category'] or 'General',
                    book['available_copies'],
                    book['total_copies']
                ), tags=(book['book_id'],))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {str(e)}")

    def filter_books(self, *args):
        """Filter books based on search"""
        search_term = self.book_search_var.get().lower()

        # Clear existing items
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

        # Filter and insert matching books
        for book in self.all_books:
            if (search_term in book['title'].lower() or
                search_term in book['author'].lower() or
                    (book['isbn'] and search_term in book['isbn'].lower())):

                self.books_tree.insert('', 'end', values=(
                    book['title'],
                    book['author'],
                    book['isbn'] or 'N/A',
                    book['category'] or 'General',
                    book['available_copies'],
                    book['total_copies']
                ), tags=(book['book_id'],))

    def delete_book(self):
        """Delete selected book"""
        selection = self.books_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return

        # Get book ID from tags
        book_id = self.books_tree.item(selection[0])['tags'][0]
        book_title = self.books_tree.item(selection[0])['values'][0]

        if messagebox.askyesno("Confirm", f"Delete book '{book_title}'?"):
            try:
                # Check if book is currently issued
                cursor = self.db_manager.execute_query(
                    "SELECT COUNT(*) FROM library_transactions WHERE book_id = ? AND status = 'issued'",
                    (book_id,)
                )
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror(
                        "Error", "Cannot delete book that is currently issued")
                    return

                self.db_manager.execute_and_commit(
                    "DELETE FROM library_books WHERE book_id = ?", (book_id,))
                messagebox.showinfo("Success", "Book deleted successfully")
                self.load_books()

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to delete book: {str(e)}")

    def issue_book(self):
        """Issue book to student"""
        try:
            roll_number = self.student_roll_var.get().strip()
            book_id = self.book_id_var.get().strip()

            if not roll_number or not book_id:
                messagebox.showerror(
                    "Error", "Student Roll Number and Book ID are required")
                return

            # Check if student exists
            cursor = self.db_manager.execute_query(
                "SELECT student_id FROM students WHERE roll_number = ?", (roll_number,))
            student = cursor.fetchone()
            if not student:
                messagebox.showerror("Error", "Student not found")
                return

            student_id = student['student_id']

            # Check if book exists and is available
            cursor = self.db_manager.execute_query(
                "SELECT book_id, title, available_copies FROM library_books WHERE book_id = ?",
                (book_id,)
            )
            book = cursor.fetchone()
            if not book:
                messagebox.showerror("Error", "Book not found")
                return

            if book['available_copies'] <= 0:
                messagebox.showerror("Error", "Book not available")
                return

            # Calculate due date (14 days from today)
            issue_date = date.today()
            due_date = issue_date + timedelta(days=14)

            # Create transaction
            self.db_manager.execute_and_commit("""
                INSERT INTO library_transactions (student_id, book_id, issue_date, due_date, status)
                VALUES (?, ?, ?, ?, 'issued')
            """, (student_id, book_id, issue_date, due_date))

            # Update available copies
            self.db_manager.execute_and_commit(
                "UPDATE library_books SET available_copies = available_copies - 1 WHERE book_id = ?",
                (book_id,)
            )

            messagebox.showinfo(
                "Success", f"Book '{book['title']}' issued to student {roll_number}")
            self.student_roll_var.set("")
            self.book_id_var.set("")
            self.load_books()
            self.load_transactions()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to issue book: {str(e)}")

    def return_book(self):
        """Return book"""
        try:
            transaction_id = self.transaction_id_var.get().strip()

            if not transaction_id:
                messagebox.showerror("Error", "Transaction ID is required")
                return

            # Check if transaction exists and is active
            cursor = self.db_manager.execute_query("""
                SELECT t.transaction_id, t.book_id, b.title, t.due_date
                FROM library_transactions t
                JOIN library_books b ON t.book_id = b.book_id
                WHERE t.transaction_id = ? AND t.status = 'issued'
            """, (transaction_id,))

            transaction = cursor.fetchone()
            if not transaction:
                messagebox.showerror("Error", "Active transaction not found")
                return

            # Calculate fine if overdue
            return_date = date.today()
            due_date = datetime.strptime(
                transaction['due_date'], '%Y-%m-%d').date()
            fine_amount = 0.0

            if return_date > due_date:
                days_overdue = (return_date - due_date).days
                fine_amount = days_overdue * 2.0  # $2 per day

            # Update transaction
            self.db_manager.execute_and_commit("""
                UPDATE library_transactions 
                SET return_date = ?, status = 'returned', fine_amount = ?
                WHERE transaction_id = ?
            """, (return_date, fine_amount, transaction_id))

            # Update available copies
            self.db_manager.execute_and_commit(
                "UPDATE library_books SET available_copies = available_copies + 1 WHERE book_id = ?",
                (transaction['book_id'],)
            )

            message = f"Book '{transaction['title']}' returned successfully"
            if fine_amount > 0:
                message += f"\nFine amount: ${fine_amount:.2f}"

            messagebox.showinfo("Success", message)
            self.transaction_id_var.set("")
            self.load_books()
            self.load_transactions()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {str(e)}")

    def load_transactions(self):
        """Load active transactions"""
        try:
            cursor = self.db_manager.execute_query("""
                SELECT t.transaction_id, s.roll_number, b.title, t.issue_date, t.due_date, t.status
                FROM library_transactions t
                JOIN students s ON t.student_id = s.student_id
                JOIN library_books b ON t.book_id = b.book_id
                WHERE t.status = 'issued'
                ORDER BY t.issue_date DESC
            """)

            # Clear existing items
            for item in self.trans_tree.get_children():
                self.trans_tree.delete(item)

            # Insert transactions
            for trans in cursor.fetchall():
                self.trans_tree.insert('', 'end', values=(
                    trans['transaction_id'],
                    trans['roll_number'],
                    trans['title'],
                    trans['issue_date'],
                    trans['due_date'],
                    trans['status'].title()
                ))

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to load transactions: {str(e)}")
