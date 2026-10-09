"""
System Test - College Management System
Tests all modules to ensure they load without errors
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))


def test_imports():
    """Test all module imports"""
    print("Testing College Management System Modules...")
    print("=" * 50)

    try:
        # Test config imports
        from config.settings import COLORS, FONTS
        print("✅ Config settings imported successfully")

        from config.database import DatabaseManager
        print("✅ Database manager imported successfully")

        # Test utils imports
        from utils.validators import validate_email, validate_phone
        print("✅ Validators imported successfully")

        from utils.helpers import format_currency, format_date
        print("✅ Helpers imported successfully")

        # Test module imports
        from modules.authentication.login import LoginSystem
        print("✅ Authentication module imported successfully")

        from modules.dashboard.main_dashboard import MainDashboard
        print("✅ Dashboard module imported successfully")

        from modules.student_management.student_system import StudentManagement
        print("✅ Student management module imported successfully")

        from modules.library_system.library_management import LibrarySystem
        print("✅ Library system module imported successfully")

        from modules.fee_management.fee_system import FeeSystem
        print("✅ Fee management module imported successfully")

        from modules.academic_records.marksheet_system import MarksheetSystem
        print("✅ Academic records module imported successfully")

        from modules.reports.reports_system import ReportsSystem
        print("✅ Reports system module imported successfully")

        from modules.settings.settings_system import SettingsSystem
        print("✅ Settings system module imported successfully")

        print("\n" + "=" * 50)
        print("🎉 ALL MODULES IMPORTED SUCCESSFULLY!")
        print("The College Management System is ready to use.")
        print("Default login: admin / admin123")
        print("=" * 50)

        return True

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False


def test_database_connection():
    """Test database connection"""
    try:
        from config.database import DatabaseManager
        db = DatabaseManager()

        # Test a simple query
        cursor = db.execute_query(
            "SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print(f"\n📊 Database Status:")
        print(f"Connected to database successfully")
        print(f"Found {len(tables)} tables in database")

        # Check for required tables
        table_names = [table[0] for table in tables]
        required_tables = ['users', 'students',
                           'library_books', 'fee_structure', 'marksheets']

        for table in required_tables:
            if table in table_names:
                print(f"✅ Table '{table}' exists")
            else:
                print(f"⚠️  Table '{table}' missing")

        return True

    except Exception as e:
        print(f"❌ Database Error: {e}")
        return False


if __name__ == "__main__":
    print("College Management System - ProjectsHUB")
    print("System Verification Test")
    print("=" * 50)

    # Test imports
    imports_ok = test_imports()

    # Test database if imports successful
    if imports_ok:
        db_ok = test_database_connection()

        if imports_ok and db_ok:
            print("\n🚀 System is ready! Run 'python main.py' to start the application.")
        else:
            print("\n⚠️  Some issues detected. Check the troubleshooting guide.")

    input("\nPress Enter to exit...")
