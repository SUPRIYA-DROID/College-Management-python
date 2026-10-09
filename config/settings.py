"""
Application Settings and Constants
College Management System - ProjectsHUB

Contains all application-wide settings and configuration constants.
"""

import os
from pathlib import Path

# Application Information
APP_NAME = "College Management System"
APP_VERSION = "2.0.0"
POWERED_BY = "ProjectsHUB"

# Database Configuration
DATABASE_NAME = "college_management.db"
DATABASE_PATH = Path(__file__).parent.parent / "database" / DATABASE_NAME

# UI Configuration
DEFAULT_WINDOW_SIZE = "1200x700"
MIN_WINDOW_SIZE = (800, 600)

# Color Scheme
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#C73E1D',
    'warning': '#F4B942',
    'danger': '#D32F2F',
    'light': '#F8F9FA',
    'dark': '#343A40',
    'background': '#F0F0F0',
    'surface': '#FFFFFF',
    'on_primary': '#FFFFFF',
    'on_secondary': '#FFFFFF',
    'on_background': '#000000',
    'on_surface': '#000000'
}

# Font Configuration
FONTS = {
    'title': ('Arial', 24, 'bold'),
    'heading': ('Arial', 18, 'bold'),
    'subheading': ('Arial', 14, 'bold'),
    'body': ('Arial', 12, 'normal'),
    'small': ('Arial', 10, 'normal'),
    'button': ('Arial', 12, 'bold'),
    'menu': ('Arial', 14, 'normal')
}

# Widget Styles
BUTTON_STYLE = {
    'font': FONTS['button'],
    'relief': 'flat',
    'bd': 0,
    'padx': 20,
    'pady': 8,
    'cursor': 'hand2'
}

ENTRY_STYLE = {
    'font': FONTS['body'],
    'relief': 'solid',
    'bd': 1,
    'highlightthickness': 2
}

LABEL_STYLE = {
    'font': FONTS['body'],
    'bg': COLORS['background'],
    'fg': COLORS['on_background']
}

# Application Constants
MAX_LOGIN_ATTEMPTS = 3
SESSION_TIMEOUT = 3600  # seconds
BACKUP_INTERVAL = 86400  # 24 hours in seconds

# File Paths
ASSETS_PATH = Path(__file__).parent.parent / "assets"
ICONS_PATH = ASSETS_PATH / "icons"
LOGS_PATH = Path(__file__).parent.parent / "logs"

# Ensure directories exist
ASSETS_PATH.mkdir(exist_ok=True)
ICONS_PATH.mkdir(exist_ok=True)
LOGS_PATH.mkdir(exist_ok=True)

# Student Configuration
STUDENT_STATUS_OPTIONS = ['active', 'inactive', 'graduated', 'dropped']
GENDER_OPTIONS = ['Male', 'Female', 'Other']
COURSE_OPTIONS = [
    'Computer Science', 'Information Technology', 'Electronics',
    'Mechanical Engineering', 'Civil Engineering', 'Business Administration',
    'Commerce', 'Arts', 'Science'
]

# Library Configuration
BOOK_CATEGORIES = [
    'Computer Science', 'Mathematics', 'Physics', 'Chemistry',
    'Literature', 'History', 'Geography', 'Economics',
    'Business', 'Engineering', 'Medical', 'Reference'
]
LOAN_DURATION_DAYS = 14
MAX_BOOKS_PER_STUDENT = 3
FINE_PER_DAY = 2.00

# Fee Configuration
PAYMENT_METHODS = ['Cash', 'Credit Card',
                   'Debit Card', 'Bank Transfer', 'Cheque']
FEE_TYPES = ['Tuition Fee', 'Library Fee',
             'Laboratory Fee', 'Examination Fee', 'Other']

# Academic Configuration
SEMESTERS = list(range(1, 9))  # 1 to 8 semesters
EXAM_TYPES = ['Mid-term', 'Final', 'Internal Assessment', 'Practical']
GRADE_SCALE = {
    'A+': (90, 100),
    'A': (80, 89),
    'B+': (70, 79),
    'B': (60, 69),
    'C+': (50, 59),
    'C': (40, 49),
    'D': (30, 39),
    'F': (0, 29)
}

# Logging Configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': LOGS_PATH / 'college_management.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

# Validation Patterns
VALIDATION_PATTERNS = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone': r'^[\d\s\-\+\(\)]{10,15}$',
    'roll_number': r'^[A-Z0-9]{4,10}$',
    'isbn': r'^(?:\d{10}|\d{13})$'
}

# Export Configuration
EXPORT_FORMATS = ['PDF', 'Excel', 'CSV']
REPORT_TEMPLATES_PATH = Path(__file__).parent.parent / "templates" / "reports"

# Security Configuration
PASSWORD_MIN_LENGTH = 6
PASSWORD_REQUIREMENTS = {
    'min_length': 6,
    'require_uppercase': False,
    'require_lowercase': False,
    'require_digits': False,
    'require_special': False
}
