#!/usr/bin/env python3
"""
Setup script for Trading Dashboard Management Tools
Makes management scripts executable and sets up shortcuts
"""

import os
import sys
import stat
from pathlib import Path

def make_executable(file_path):
    """Make a file executable"""
    current_permissions = file_path.stat().st_mode
    file_path.chmod(current_permissions | stat.S_IEXEC)

def setup_management_tools():
    """Setup management tools"""
    project_root = Path(__file__).parent
    
    print("🔧 Setting up Trading Dashboard Management Tools")
    print("=" * 50)
    
    # Make scripts executable
    scripts = [
        'manage.py',
        'deploy.py', 
        'setup_database.py'
    ]
    
    for script in scripts:
        script_path = project_root / script
        if script_path.exists():
            make_executable(script_path)
            print(f"✅ Made {script} executable")
        else:
            print(f"❌ {script} not found")
    
    # Create shortcuts/aliases file
    shortcuts_content = '''#!/bin/bash
# Trading Dashboard Management Shortcuts

# Component Management
alias td-add-component="python manage.py add-component"
alias td-remove-component="python manage.py remove-component"

# API Management  
alias td-add-endpoint="python manage.py add-endpoint"

# Database Management
alias td-add-model="python manage.py add-model"
alias td-migrate="python manage.py migrate"
alias td-backup-db="python manage.py backup-db"

# Deployment
alias td-deploy="python deploy.py"
alias td-status="python deploy.py status"
alias td-backup="python manage.py backup"

# Development
alias td-setup="python setup_database.py"
alias td-admin="echo 'Open http://localhost:5000/admin.html in your browser'"

echo "🎛️ Trading Dashboard shortcuts loaded!"
echo "Usage examples:"
echo "  td-add-component portfolio widget"
echo "  td-add-endpoint user-stats GET"
echo "  td-deploy frontend"
echo "  td-status"
'''
    
    shortcuts_file = project_root / 'td_shortcuts.sh'
    shortcuts_file.write_text(shortcuts_content)
    make_executable(shortcuts_file)
    print(f"✅ Created shortcuts file: {shortcuts_file}")
    
    # Create Windows batch file
    batch_content = '''@echo off
REM Trading Dashboard Management Shortcuts for Windows

if "%1"=="add-component" (
    python manage.py add-component %2 %3
) else if "%1"=="remove-component" (
    python manage.py remove-component %2
) else if "%1"=="add-endpoint" (
    python manage.py add-endpoint %2 %3
) else if "%1"=="deploy" (
    python deploy.py %2
) else if "%1"=="status" (
    python deploy.py status
) else if "%1"=="setup" (
    python setup_database.py
) else if "%1"=="admin" (
    echo Open http://localhost:5000/admin.html in your browser
    start http://localhost:5000/admin.html
) else (
    echo Trading Dashboard Management Tool
    echo.
    echo Usage: td [command] [args]
    echo.
    echo Commands:
    echo   add-component [name] [type]  - Create new component
    echo   remove-component [name]      - Remove component
    echo   add-endpoint [name] [method] - Add API endpoint
    echo   deploy [target]              - Deploy application
    echo   status                       - Show status
    echo   setup                        - Setup database
    echo   admin                        - Open admin panel
)
'''
    
    batch_file = project_root / 'td.bat'
    batch_file.write_text(batch_content)
    print(f"✅ Created Windows batch file: {batch_file}")
    
    # Create package.json for npm scripts
    package_json = {
        "name": "trading-dashboard",
        "version": "1.0.0",
        "description": "Professional Trading Dashboard",
        "scripts": {
            "setup": "python setup_database.py",
            "dev": "cd backend && python app.py",
            "deploy": "python deploy.py frontend",
            "deploy:render": "python deploy.py render",
            "deploy:heroku": "python deploy.py heroku",
            "backup": "python manage.py backup",
            "migrate": "python manage.py migrate",
            "add:component": "python manage.py add-component",
            "add:endpoint": "python manage.py add-endpoint",
            "add:model": "python manage.py add-model",
            "status": "python deploy.py status"
        },
        "keywords": ["trading", "dashboard", "finance", "analytics"],
        "author": "Trading Dashboard",
        "license": "MIT"
    }
    
    package_file = project_root / 'package.json'
    import json
    package_file.write_text(json.dumps(package_json, indent=2))
    print(f"✅ Created package.json with npm scripts")
    
    print("\n🎉 Management tools setup complete!")
    print("\n📋 Quick Start Commands:")
    print("  python manage.py add-component portfolio widget")
    print("  python manage.py add-endpoint user-stats GET") 
    print("  python deploy.py frontend")
    print("  python deploy.py status")
    print("\n📋 NPM Scripts (if you have Node.js):")
    print("  npm run setup")
    print("  npm run dev")
    print("  npm run deploy")
    print("  npm run status")
    
    print("\n🌟 Admin Panel:")
    print("  Start backend: python backend/app.py")
    print("  Open: http://localhost:5000/admin.html")

if __name__ == "__main__":
    setup_management_tools()