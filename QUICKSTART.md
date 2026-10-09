# College Management System - Quick Start Guide

## Quick Setup (Windows)

### Step 1: Verify Python Installation
Open Command Prompt (cmd) and check Python version:
```cmd
python --version
```
*Ensure you have Python 3.7 or higher*

### Step 2: Navigate to Project Directory
```cmd
cd "d:\Projects\ProjectHUB_Sources\College-Management-System-python"
```

### Step 3: Initialize Database
```cmd
python database_setup.py
```

### Step 4: Run the Application
```cmd
python main.py
```

## Default Login Credentials
- **Username:** admin
- **Password:** admin

*Change these credentials after first login for security*

## Features Overview

### Dashboard
- System overview with statistics
- Quick action buttons for common tasks
- Navigation to all modules

### Student Management
- Add, edit, and delete student records
- Search and filter students
- View detailed student information
- Manage student status and academic details

### Database Features
- SQLite database for reliable data storage
- Automatic table creation and initialization
- Data validation and error handling
- Backup and restore capabilities

## Troubleshooting

### Common Issues

1. **"Module not found" Error**
   - Ensure you're in the correct directory
   - Check Python installation

2. **Database Error**
   - Run `python database_setup.py` again
   - Check file permissions

3. **GUI Not Displaying**
   - Ensure tkinter is installed (comes with Python)
   - Check display settings

### Reset Database (if needed)
```cmd
python database_setup.py reset
```
*Warning: This deletes all data*

## Project Structure

```
College-Management-System-python/
├── main.py                 # Main application entry point
├── database_setup.py       # Database initialization script
├── config/                 # Configuration files
├── modules/                # Application modules
├── utils/                  # Utility functions
├── database/              # SQLite database files
└── README.md              # Detailed documentation
```

## Next Steps

1. **Change Default Password**: Update admin credentials in settings
2. **Add Students**: Use Student Management to add student records
3. **Explore Modules**: Navigate through different system modules
4. **Backup Data**: Regularly backup your database

## Support

For detailed documentation, see the main README.md file.
For issues or questions, refer to the troubleshooting section.
