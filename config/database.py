"""
Database Configuration and Management
College Management System - ProjectsHUB

Handles all database operations and configurations.
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime
import hashlib


class DatabaseManager:
    """Manages database operations for the College Management System"""

    def __init__(self, db_path=None):
        if db_path is None:
            # Create database directory if it doesn't exist
            db_dir = Path(__file__).parent.parent / "database"
            db_dir.mkdir(exist_ok=True)
            self.db_path = db_dir / "college_management.db"
        else:
            self.db_path = Path(db_path)

        self.connection = None

    def get_connection(self):
        """Get database connection"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
        return self.connection

    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        conn = self.get_connection()
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        return cursor

    def execute_and_commit(self, query, params=None):
        """Execute query and commit changes"""
        cursor = self.execute_query(query, params)
        self.connection.commit()
        return cursor

    def initialize_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()

        # Create users table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT,
                role TEXT DEFAULT 'admin',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')

        # Create students table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_number TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                father_name TEXT,
                mother_name TEXT,
                date_of_birth DATE,
                gender TEXT,
                address TEXT,
                phone_number TEXT,
                email TEXT,
                admission_date DATE DEFAULT CURRENT_DATE,
                course TEXT,
                semester INTEGER,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create library_books table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS library_books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT UNIQUE,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publisher TEXT,
                publication_year INTEGER,
                category TEXT,
                total_copies INTEGER DEFAULT 1,
                available_copies INTEGER DEFAULT 1,
                location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create library_transactions table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS library_transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                issue_date DATE DEFAULT CURRENT_DATE,
                due_date DATE,
                return_date DATE,
                fine_amount DECIMAL(10,2) DEFAULT 0.00,
                status TEXT DEFAULT 'issued',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (student_id),
                FOREIGN KEY (book_id) REFERENCES library_books (book_id)
            )
        ''')

        # Create fee_structure table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS fee_structure (
                fee_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course TEXT NOT NULL,
                semester INTEGER NOT NULL,
                tuition_fee DECIMAL(10,2) DEFAULT 0.00,
                library_fee DECIMAL(10,2) DEFAULT 0.00,
                lab_fee DECIMAL(10,2) DEFAULT 0.00,
                other_fee DECIMAL(10,2) DEFAULT 0.00,
                total_fee DECIMAL(10,2) DEFAULT 0.00,
                academic_year TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create fee_payments table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS fee_payments (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                fee_id INTEGER NOT NULL,
                amount_paid DECIMAL(10,2) NOT NULL,
                payment_date DATE DEFAULT CURRENT_DATE,
                payment_method TEXT DEFAULT 'cash',
                receipt_number TEXT UNIQUE,
                remarks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (student_id),
                FOREIGN KEY (fee_id) REFERENCES fee_structure (fee_id)
            )
        ''')

        # Create marksheets table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS marksheets (
                marksheet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course TEXT NOT NULL,
                semester INTEGER NOT NULL,
                subject_name TEXT NOT NULL,
                max_marks INTEGER DEFAULT 100,
                obtained_marks INTEGER NOT NULL,
                grade TEXT,
                exam_type TEXT DEFAULT 'semester',
                exam_date DATE,
                academic_year TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students (student_id)
            )
        ''')

        conn.commit()

        # Create default admin user if not exists
        self._create_default_admin()

    def _create_default_admin(self):
        """Create default admin user"""
        conn = self.get_connection()

        # Check if admin user exists
        cursor = conn.execute(
            "SELECT COUNT(*) FROM users WHERE username = ?", ("admin",))
        if cursor.fetchone()[0] == 0:
            # Create default admin user
            password_hash = self._hash_password("admin")
            conn.execute('''
                INSERT INTO users (username, password_hash, full_name, email, role)
                VALUES (?, ?, ?, ?, ?)
            ''', ("admin", password_hash, "System Administrator", "admin@college.edu", "admin"))
            conn.commit()

    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password, password_hash):
        """Verify password against hash"""
        return self._hash_password(password) == password_hash

    def backup_database(self, backup_path=None):
        """Create database backup"""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"college_management_backup_{timestamp}.db"

        # Copy database file
        import shutil
        shutil.copy2(self.db_path, backup_path)
        return backup_path

    def restore_database(self, backup_path):
        """Restore database from backup"""
        import shutil
        self.close_connection()
        shutil.copy2(backup_path, self.db_path)
        self.get_connection()

    def get_table_info(self, table_name):
        """Get table structure information"""
        cursor = self.execute_query(f"PRAGMA table_info({table_name})")
        return cursor.fetchall()

    def get_all_tables(self):
        """Get list of all tables in database"""
        cursor = self.execute_query(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        return [row[0] for row in cursor.fetchall()]
