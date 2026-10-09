"""
Utility Helper Functions
College Management System - ProjectsHUB

Common utility functions used throughout the application.
"""

import re
from datetime import datetime, date
import tkinter as tk
from tkinter import messagebox


def validate_email(email):
    """
    Validate email format using regex

    Args:
        email (str): Email address to validate

    Returns:
        bool: True if email is valid, False otherwise
    """
    if not email:
        return True  # Allow empty emails

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """
    Validate phone number format

    Args:
        phone (str): Phone number to validate

    Returns:
        bool: True if phone is valid, False otherwise
    """
    if not phone:
        return True  # Allow empty phone numbers

    # Remove spaces, dashes, and parentheses
    cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)

    # Check if it contains only digits and optional + at start
    pattern = r'^\+?\d{10,15}$'
    return re.match(pattern, cleaned_phone) is not None


def validate_roll_number(roll_number):
    """
    Validate student roll number format

    Args:
        roll_number (str): Roll number to validate

    Returns:
        bool: True if roll number is valid, False otherwise
    """
    if not roll_number:
        return False

    # Roll number should be 4-10 characters, alphanumeric
    pattern = r'^[A-Z0-9]{4,10}$'
    return re.match(pattern, roll_number.upper()) is not None


def validate_date(date_string, date_format="%Y-%m-%d"):
    """
    Validate date string format

    Args:
        date_string (str): Date string to validate
        date_format (str): Expected date format

    Returns:
        bool: True if date is valid, False otherwise
    """
    if not date_string:
        return True  # Allow empty dates

    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False


def format_date(date_obj, format_string="%Y-%m-%d"):
    """
    Format date object to string

    Args:
        date_obj: Date object to format
        format_string (str): Output format

    Returns:
        str: Formatted date string
    """
    if isinstance(date_obj, str):
        return date_obj
    elif isinstance(date_obj, (date, datetime)):
        return date_obj.strftime(format_string)
    else:
        return ""


def calculate_age(birth_date):
    """
    Calculate age from birth date

    Args:
        birth_date: Birth date (string or date object)

    Returns:
        int: Age in years
    """
    if isinstance(birth_date, str):
        try:
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        except ValueError:
            return None

    if isinstance(birth_date, date):
        today = date.today()
        age = today.year - birth_date.year

        # Adjust if birthday hasn't occurred this year
        if today.month < birth_date.month or \
           (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1

        return age

    return None


def calculate_grade(marks, max_marks=100):
    """
    Calculate grade based on percentage

    Args:
        marks (int): Obtained marks
        max_marks (int): Maximum marks

    Returns:
        str: Grade (A+, A, B+, B, C+, C, D, F)
    """
    if marks is None or max_marks is None or max_marks == 0:
        return 'N/A'

    percentage = (marks / max_marks) * 100

    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B+'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C+'
    elif percentage >= 40:
        return 'C'
    elif percentage >= 30:
        return 'D'
    else:
        return 'F'


def calculate_gpa(grades):
    """
    Calculate GPA from list of grades

    Args:
        grades (list): List of grade strings

    Returns:
        float: GPA value
    """
    grade_points = {
        'A+': 4.0, 'A': 3.7, 'B+': 3.3, 'B': 3.0,
        'C+': 2.7, 'C': 2.3, 'D': 2.0, 'F': 0.0
    }

    valid_grades = [grade for grade in grades if grade in grade_points]

    if not valid_grades:
        return 0.0

    total_points = sum(grade_points[grade] for grade in valid_grades)
    return round(total_points / len(valid_grades), 2)


def format_currency(amount):
    """
    Format amount as currency

    Args:
        amount (float): Amount to format

    Returns:
        str: Formatted currency string
    """
    if amount is None:
        return "$0.00"

    return f"${amount:,.2f}"


def sanitize_filename(filename):
    """
    Sanitize filename by removing invalid characters

    Args:
        filename (str): Original filename

    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)

    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')

    return sanitized


def show_error_dialog(title, message):
    """
    Show error dialog with consistent styling

    Args:
        title (str): Dialog title
        message (str): Error message
    """
    messagebox.showerror(title, message)


def show_success_dialog(title, message):
    """
    Show success dialog with consistent styling

    Args:
        title (str): Dialog title
        message (str): Success message
    """
    messagebox.showinfo(title, message)


def show_warning_dialog(title, message):
    """
    Show warning dialog with consistent styling

    Args:
        title (str): Dialog title
        message (str): Warning message
    """
    messagebox.showwarning(title, message)


def confirm_action(title, message):
    """
    Show confirmation dialog

    Args:
        title (str): Dialog title
        message (str): Confirmation message

    Returns:
        bool: True if user confirmed, False otherwise
    """
    return messagebox.askyesno(title, message)


def center_window(window, width=None, height=None):
    """
    Center window on screen

    Args:
        window: Tkinter window object
        width (int): Window width (optional)
        height (int): Window height (optional)
    """
    window.update_idletasks()

    if width is None:
        width = window.winfo_width()
    if height is None:
        height = window.winfo_height()

    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


def bind_mousewheel(widget, frame):
    """
    Bind mousewheel scrolling to a widget

    Args:
        widget: Widget to bind scrolling to
        frame: Frame containing the scrollable content
    """
    def on_mousewheel(event):
        widget.yview_scroll(int(-1 * (event.delta / 120)), "units")

    frame.bind("<MouseWheel>", on_mousewheel)


def create_tooltip(widget, text):
    """
    Create a tooltip for a widget

    Args:
        widget: Widget to add tooltip to
        text (str): Tooltip text
    """
    def show_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

        label = tk.Label(
            tooltip,
            text=text,
            background="lightyellow",
            relief="solid",
            borderwidth=1,
            font=("Arial", 10)
        )
        label.pack()

        # Store tooltip reference
        widget.tooltip = tooltip

    def hide_tooltip(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            del widget.tooltip

    widget.bind("<Enter>", show_tooltip)
    widget.bind("<Leave>", hide_tooltip)


def get_current_academic_year():
    """
    Get current academic year string

    Returns:
        str: Academic year (e.g., "2023-2024")
    """
    current_date = date.today()

    # Academic year typically starts in July/August
    if current_date.month >= 7:
        start_year = current_date.year
        end_year = current_date.year + 1
    else:
        start_year = current_date.year - 1
        end_year = current_date.year

    return f"{start_year}-{end_year}"


def export_to_csv(data, filename, headers=None):
    """
    Export data to CSV file

    Args:
        data (list): List of data rows
        filename (str): Output filename
        headers (list): Column headers (optional)

    Returns:
        bool: True if export successful, False otherwise
    """
    try:
        import csv

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            if headers:
                writer.writerow(headers)

            for row in data:
                writer.writerow(row)

        return True

    except Exception as e:
        show_error_dialog("Export Error", f"Failed to export data: {str(e)}")
        return False


def generate_receipt_number():
    """
    Generate unique receipt number

    Returns:
        str: Receipt number in format REC-YYYYMMDD-HHMMSS
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"REC-{timestamp}"


def get_semester_name(semester_number):
    """
    Get semester name from number

    Args:
        semester_number (int): Semester number (1-8)

    Returns:
        str: Semester name
    """
    semester_names = {
        1: "First Semester",
        2: "Second Semester",
        3: "Third Semester",
        4: "Fourth Semester",
        5: "Fifth Semester",
        6: "Sixth Semester",
        7: "Seventh Semester",
        8: "Eighth Semester"
    }

    return semester_names.get(semester_number, f"Semester {semester_number}")
