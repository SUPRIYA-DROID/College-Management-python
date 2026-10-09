"""
Input Validation Module
College Management System - ProjectsHUB

Provides comprehensive input validation functions for form data.
"""

import re
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Tuple


class ValidationResult:
    """Represents the result of a validation operation"""

    def __init__(self, is_valid: bool = True, error_message: str = ""):
        self.is_valid = is_valid
        self.error_message = error_message

    def __bool__(self):
        return self.is_valid


class FormValidator:
    """Comprehensive form validation class"""

    # Validation patterns
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    PHONE_PATTERN = r'^[\d\s\-\+\(\)]{10,15}$'
    ROLL_NUMBER_PATTERN = r'^[A-Z0-9]{4,10}$'
    ISBN_PATTERN = r'^(?:\d{10}|\d{13})$'
    NAME_PATTERN = r'^[a-zA-Z\s]{2,50}$'

    @staticmethod
    def validate_required(value: Any, field_name: str) -> ValidationResult:
        """Validate required field"""
        if not value or (isinstance(value, str) and not value.strip()):
            return ValidationResult(False, f"{field_name} is required")
        return ValidationResult()

    @staticmethod
    def validate_string_length(value: str, field_name: str, min_length: int = 0, max_length: int = 255) -> ValidationResult:
        """Validate string length"""
        if not isinstance(value, str):
            return ValidationResult(False, f"{field_name} must be a string")

        length = len(value.strip())
        if length < min_length:
            return ValidationResult(False, f"{field_name} must be at least {min_length} characters long")
        if length > max_length:
            return ValidationResult(False, f"{field_name} must be at most {max_length} characters long")

        return ValidationResult()

    @staticmethod
    def validate_email(email: str) -> ValidationResult:
        """Validate email format"""
        if not email:
            return ValidationResult()  # Empty email is allowed

        if not re.match(FormValidator.EMAIL_PATTERN, email):
            return ValidationResult(False, "Invalid email format")
        return ValidationResult()

    @staticmethod
    def validate_phone(phone: str) -> ValidationResult:
        """Validate phone number"""
        if not phone:
            return ValidationResult()  # Empty phone is allowed

        # Remove spaces and formatting
        cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)

        if not re.match(r'^\+?\d{10,15}$', cleaned_phone):
            return ValidationResult(False, "Invalid phone number format")
        return ValidationResult()

    @staticmethod
    def validate_roll_number(roll_number: str) -> ValidationResult:
        """Validate student roll number"""
        if not roll_number:
            return ValidationResult(False, "Roll number is required")

        if not re.match(FormValidator.ROLL_NUMBER_PATTERN, roll_number.upper()):
            return ValidationResult(False, "Roll number must be 4-10 alphanumeric characters")
        return ValidationResult()

    @staticmethod
    def validate_name(name: str, field_name: str) -> ValidationResult:
        """Validate person name"""
        if not name:
            return ValidationResult(False, f"{field_name} is required")

        if not re.match(FormValidator.NAME_PATTERN, name):
            return ValidationResult(False, f"{field_name} must contain only letters and spaces (2-50 characters)")
        return ValidationResult()

    @staticmethod
    def validate_date(date_string: str, field_name: str, date_format: str = "%Y-%m-%d") -> ValidationResult:
        """Validate date format"""
        if not date_string:
            return ValidationResult()  # Empty date is allowed

        try:
            parsed_date = datetime.strptime(date_string, date_format).date()

            # Check if date is not in the future (for birth dates)
            if field_name.lower().find('birth') != -1 and parsed_date > date.today():
                return ValidationResult(False, f"{field_name} cannot be in the future")

            return ValidationResult()
        except ValueError:
            return ValidationResult(False, f"Invalid {field_name.lower()} format (YYYY-MM-DD)")

    @staticmethod
    def validate_numeric(value: str, field_name: str, min_value: Optional[float] = None, max_value: Optional[float] = None) -> ValidationResult:
        """Validate numeric value"""
        if not value:
            return ValidationResult(False, f"{field_name} is required")

        try:
            numeric_value = float(value)

            if min_value is not None and numeric_value < min_value:
                return ValidationResult(False, f"{field_name} must be at least {min_value}")
            if max_value is not None and numeric_value > max_value:
                return ValidationResult(False, f"{field_name} must be at most {max_value}")

            return ValidationResult()
        except ValueError:
            return ValidationResult(False, f"{field_name} must be a valid number")

    @staticmethod
    def validate_integer(value: str, field_name: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> ValidationResult:
        """Validate integer value"""
        if not value:
            return ValidationResult(False, f"{field_name} is required")

        try:
            int_value = int(value)

            if min_value is not None and int_value < min_value:
                return ValidationResult(False, f"{field_name} must be at least {min_value}")
            if max_value is not None and int_value > max_value:
                return ValidationResult(False, f"{field_name} must be at most {max_value}")

            return ValidationResult()
        except ValueError:
            return ValidationResult(False, f"{field_name} must be a valid integer")

    @staticmethod
    def validate_choice(value: str, field_name: str, choices: List[str]) -> ValidationResult:
        """Validate choice from predefined options"""
        if not value:
            return ValidationResult(False, f"{field_name} is required")

        if value not in choices:
            return ValidationResult(False, f"{field_name} must be one of: {', '.join(choices)}")
        return ValidationResult()

    @staticmethod
    def validate_isbn(isbn: str) -> ValidationResult:
        """Validate ISBN format"""
        if not isbn:
            return ValidationResult()  # Empty ISBN is allowed

        # Remove hyphens and spaces
        cleaned_isbn = re.sub(r'[\s\-]', '', isbn)

        if not re.match(FormValidator.ISBN_PATTERN, cleaned_isbn):
            return ValidationResult(False, "ISBN must be 10 or 13 digits")
        return ValidationResult()

    @staticmethod
    def validate_password(password: str, min_length: int = 6) -> ValidationResult:
        """Validate password strength"""
        if not password:
            return ValidationResult(False, "Password is required")

        if len(password) < min_length:
            return ValidationResult(False, f"Password must be at least {min_length} characters long")

        # Additional password strength checks can be added here
        return ValidationResult()


class StudentValidator:
    """Specialized validator for student data"""

    @staticmethod
    def validate_student_data(data: Dict[str, Any]) -> Dict[str, str]:
        """
        Validate complete student data

        Returns:
            Dict with field names as keys and error messages as values
        """
        errors = {}

        # Required fields validation
        required_fields = ['roll_number', 'first_name', 'last_name']
        for field in required_fields:
            result = FormValidator.validate_required(
                data.get(field), field.replace('_', ' ').title())
            if not result:
                errors[field] = result.error_message

        # Roll number validation
        if 'roll_number' in data and data['roll_number']:
            result = FormValidator.validate_roll_number(data['roll_number'])
            if not result:
                errors['roll_number'] = result.error_message

        # Name validations
        name_fields = ['first_name', 'last_name', 'father_name', 'mother_name']
        for field in name_fields:
            if field in data and data[field]:
                result = FormValidator.validate_name(
                    data[field], field.replace('_', ' ').title())
                if not result:
                    errors[field] = result.error_message

        # Email validation
        if 'email' in data and data['email']:
            result = FormValidator.validate_email(data['email'])
            if not result:
                errors['email'] = result.error_message

        # Phone validation
        if 'phone_number' in data and data['phone_number']:
            result = FormValidator.validate_phone(data['phone_number'])
            if not result:
                errors['phone_number'] = result.error_message

        # Date of birth validation
        if 'date_of_birth' in data and data['date_of_birth']:
            result = FormValidator.validate_date(
                data['date_of_birth'], 'Date of Birth')
            if not result:
                errors['date_of_birth'] = result.error_message

        # Gender validation
        if 'gender' in data and data['gender']:
            result = FormValidator.validate_choice(
                data['gender'], 'Gender', ['Male', 'Female', 'Other'])
            if not result:
                errors['gender'] = result.error_message

        # Semester validation
        if 'semester' in data and data['semester']:
            result = FormValidator.validate_integer(
                str(data['semester']), 'Semester', 1, 8)
            if not result:
                errors['semester'] = result.error_message

        return errors


class LibraryValidator:
    """Specialized validator for library data"""

    @staticmethod
    def validate_book_data(data: Dict[str, Any]) -> Dict[str, str]:
        """Validate book data"""
        errors = {}

        # Required fields
        required_fields = ['title', 'author']
        for field in required_fields:
            result = FormValidator.validate_required(
                data.get(field), field.replace('_', ' ').title())
            if not result:
                errors[field] = result.error_message

        # ISBN validation
        if 'isbn' in data and data['isbn']:
            result = FormValidator.validate_isbn(data['isbn'])
            if not result:
                errors['isbn'] = result.error_message

        # Publication year validation
        if 'publication_year' in data and data['publication_year']:
            current_year = datetime.now().year
            result = FormValidator.validate_integer(
                str(data['publication_year']), 'Publication Year', 1000, current_year)
            if not result:
                errors['publication_year'] = result.error_message

        # Copies validation
        for field in ['total_copies', 'available_copies']:
            if field in data and data[field]:
                result = FormValidator.validate_integer(
                    str(data[field]), field.replace('_', ' ').title(), 0)
                if not result:
                    errors[field] = result.error_message

        return errors


class FeeValidator:
    """Specialized validator for fee data"""

    @staticmethod
    def validate_fee_data(data: Dict[str, Any]) -> Dict[str, str]:
        """Validate fee data"""
        errors = {}

        # Amount validation
        fee_fields = ['tuition_fee', 'library_fee',
                      'lab_fee', 'other_fee', 'amount_paid']
        for field in fee_fields:
            if field in data and data[field]:
                result = FormValidator.validate_numeric(
                    str(data[field]), field.replace('_', ' ').title(), 0.0)
                if not result:
                    errors[field] = result.error_message

        # Payment method validation
        if 'payment_method' in data and data['payment_method']:
            valid_methods = ['Cash', 'Credit Card',
                             'Debit Card', 'Bank Transfer', 'Cheque']
            result = FormValidator.validate_choice(
                data['payment_method'], 'Payment Method', valid_methods)
            if not result:
                errors['payment_method'] = result.error_message

        return errors


class AcademicValidator:
    """Specialized validator for academic data"""

    @staticmethod
    def validate_marksheet_data(data: Dict[str, Any]) -> Dict[str, str]:
        """Validate marksheet data"""
        errors = {}

        # Required fields
        required_fields = ['subject_name', 'obtained_marks', 'max_marks']
        for field in required_fields:
            result = FormValidator.validate_required(
                data.get(field), field.replace('_', ' ').title())
            if not result:
                errors[field] = result.error_message

        # Marks validation
        if 'max_marks' in data and data['max_marks']:
            result = FormValidator.validate_integer(
                str(data['max_marks']), 'Maximum Marks', 1, 1000)
            if not result:
                errors['max_marks'] = result.error_message

        if 'obtained_marks' in data and data['obtained_marks']:
            max_marks = int(data.get('max_marks', 100))
            result = FormValidator.validate_integer(
                str(data['obtained_marks']), 'Obtained Marks', 0, max_marks)
            if not result:
                errors['obtained_marks'] = result.error_message

        # Semester validation
        if 'semester' in data and data['semester']:
            result = FormValidator.validate_integer(
                str(data['semester']), 'Semester', 1, 8)
            if not result:
                errors['semester'] = result.error_message

        return errors


def validate_form_data(data: Dict[str, Any], validator_class: str) -> Tuple[bool, Dict[str, str]]:
    """
    Validate form data using specified validator

    Args:
        data: Form data dictionary
        validator_class: Validator class name ('student', 'library', 'fee', 'academic')

    Returns:
        Tuple of (is_valid, errors_dict)
    """
    validators = {
        'student': StudentValidator.validate_student_data,
        'library': LibraryValidator.validate_book_data,
        'fee': FeeValidator.validate_fee_data,
        'academic': AcademicValidator.validate_marksheet_data
    }

    validator = validators.get(validator_class.lower())
    if not validator:
        return False, {'general': f"Unknown validator: {validator_class}"}

    errors = validator(data)
    is_valid = len(errors) == 0

    return is_valid, errors


# Standalone validation functions for backwards compatibility
def validate_email(email: str) -> bool:
    """Validate email address format"""
    if not email:
        return False
    result = FormValidator.validate_email(email)
    return result.is_valid


def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    if not phone:
        return False
    result = FormValidator.validate_phone(phone)
    return result.is_valid
