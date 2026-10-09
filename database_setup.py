"""
Database Setup Script
College Management System - ProjectsHUB

This script initializes the database and creates the necessary tables.
Run this script before starting the application for the first time.
"""

from config.database import DatabaseManager
import sys
from pathlib import Path
import sqlite3

# Add config to path
sys.path.append(str(Path(__file__).parent))


def setup_database():
    """Initialize the database with all required tables"""
    print("College Management System - Database Setup")
    print("Powered by ProjectsHUB")
    print("=" * 50)

    try:
        # Create database manager
        db_manager = DatabaseManager()
        print(f"Database path: {db_manager.db_path}")

        # Initialize database
        print("Creating database tables...")
        db_manager.initialize_database()

        # Verify tables were created
        tables = db_manager.get_all_tables()
        print(f"Created {len(tables)} tables: {', '.join(tables)}")

        # Close connection
        db_manager.close_connection()

        print("\nDatabase setup completed successfully!")
        print("Default admin credentials:")
        print("Username: admin")
        print("Password: admin")
        print("\nYou can now run the application using: python main.py")

    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

    return True


def check_database():
    """Check if database exists and is properly set up"""
    try:
        db_manager = DatabaseManager()
        tables = db_manager.get_all_tables()

        expected_tables = [
            'users', 'students', 'library_books', 'library_transactions',
            'fee_structure', 'fee_payments', 'marksheets'
        ]

        missing_tables = [
            table for table in expected_tables if table not in tables]

        if missing_tables:
            print(f"Missing tables: {', '.join(missing_tables)}")
            return False

        print("Database is properly configured")
        return True

    except Exception as e:
        print(f"Database check failed: {e}")
        return False


def reset_database():
    """Reset database (WARNING: This will delete all data)"""
    print("WARNING: This will delete all existing data!")
    response = input(
        "Are you sure you want to reset the database? (type 'YES' to confirm): ")

    if response == 'YES':
        try:
            db_manager = DatabaseManager()

            # Drop all tables
            tables = db_manager.get_all_tables()
            for table in tables:
                db_manager.execute_and_commit(f"DROP TABLE IF EXISTS {table}")

            print("All tables dropped")

            # Recreate tables
            db_manager.initialize_database()
            print("Database reset completed")

        except Exception as e:
            print(f"Error resetting database: {e}")
    else:
        print("Database reset cancelled")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "check":
            check_database()
        elif sys.argv[1] == "reset":
            reset_database()
        else:
            print("Usage:")
            print("python database_setup.py        - Initialize database")
            print("python database_setup.py check  - Check database")
            print(
                "python database_setup.py reset  - Reset database (WARNING: Deletes all data)")
    else:
        setup_database()
