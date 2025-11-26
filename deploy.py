#!/usr/bin/env python3
"""
Deployment Automation Script for Trading Dashboard
Handles frontend and full-stack deployments
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json
from datetime import datetime

class DeploymentManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.frontend_dir = self.project_root / 'frontend'
        self.docs_dir = self.project_root / 'docs'
        self.backend_dir = self.project_root / 'backend'

    def run_command(self, command, cwd=None):
        """Run shell command and return result"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd or self.project_root,
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {command}")
            print(f"Error: {e.stderr}")
            return None

    def sync_frontend_to_docs(self):
        """Sync frontend files to docs folder for GitHub Pages"""
        print("📁 Syncing frontend to docs folder...")
        
        # Create docs directory if it doesn't exist
        self.docs_dir.mkdir(exist_ok=True)
        
        # Copy frontend files to docs
        for item in self.frontend_dir.iterdir():
            if item.name in ['.env', '.env.example']:
                continue
                
            dest = self.docs_dir / item.name
            
            if item.is_file():
                shutil.copy2(item, dest)
                print(f"  ✅ Copied {item.name}")
            elif item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
                print(f"  ✅ Copied directory {item.name}")
        
        # Create .nojekyll file for GitHub Pages
        (self.docs_dir / '.nojekyll').touch()
        print("  ✅ Created .nojekyll file")

    def deploy_frontend(self):
        """Deploy frontend to GitHub Pages"""
        print("🚀 Deploying frontend to GitHub Pages...")
        
        # Sync files
        self.sync_frontend_to_docs()
        
        # Git operations
        commands = [
            "git add docs/",
            f"git commit -m '🚀 Frontend deployment - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'",
            "git push origin main"
        ]
        
        for cmd in commands:
            result = self.run_command(cmd)
            if result is None:
                print(f"❌ Failed to execute: {cmd}")
                return False
        
        print("✅ Frontend deployed successfully!")
        return True

    def check_backend_health(self):
        """Check if backend is running and healthy"""
        try:
            import requests
            response = requests.get('http://localhost:5000/', timeout=5)
            return response.status_code == 200
        except:
            return False

    def run_database_migrations(self):
        """Run database migrations"""
        print("🗄️ Running database migrations...")
        
        # Check if alembic is configured
        alembic_ini = self.project_root / 'alembic.ini'
        if not alembic_ini.exists():
            print("❌ Alembic not configured. Run setup first.")
            return False
        
        # Run migrations
        result = self.run_command("alembic upgrade head", cwd=self.backend_dir)
        if result is None:
            print("❌ Migration failed")
            return False
        
        print("✅ Database migrations completed")
        return True

    def backup_database(self):
        """Create database backup"""
        print("💾 Creating database backup...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = self.project_root / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        # For SQLite
        db_file = self.project_root / 'database.db'
        if db_file.exists():
            backup_file = backup_dir / f'database_backup_{timestamp}.db'
            shutil.copy2(db_file, backup_file)
            print(f"✅ SQLite backup created: {backup_file}")
            return str(backup_file)
        
        print("ℹ️ No SQLite database found")
        return None

    def deploy_to_render(self):
        """Deploy to Render.com"""
        print("🚀 Deploying to Render.com...")
        
        # Check if render.yaml exists
        render_config = self.project_root / 'render.yaml'
        if not render_config.exists():
            print("❌ render.yaml not found")
            return False
        
        # Push to main branch (triggers Render deployment)
        commands = [
            "git add .",
            f"git commit -m '🚀 Render deployment - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'",
            "git push origin main"
        ]
        
        for cmd in commands:
            result = self.run_command(cmd)
            if result is None:
                print(f"❌ Failed: {cmd}")
                return False
        
        print("✅ Pushed to main branch. Render will auto-deploy.")
        return True

    def deploy_to_heroku(self):
        """Deploy to Heroku"""
        print("🚀 Deploying to Heroku...")
        
        # Check if Heroku CLI is installed
        if not self.run_command("heroku --version"):
            print("❌ Heroku CLI not installed")
            return False
        
        # Deploy commands
        commands = [
            "git add .",
            f"git commit -m '🚀 Heroku deployment - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'",
            "git push heroku main",
            "heroku run alembic upgrade head"
        ]
        
        for cmd in commands:
            result = self.run_command(cmd)
            if result is None and "heroku run" not in cmd:
                print(f"❌ Failed: {cmd}")
                return False
        
        print("✅ Deployed to Heroku successfully!")
        return True

    def setup_environment(self):
        """Setup development environment"""
        print("🔧 Setting up development environment...")
        
        # Create .env file if it doesn't exist
        env_file = self.backend_dir / '.env'
        env_example = self.project_root / '.env.example'
        
        if not env_file.exists() and env_example.exists():
            shutil.copy2(env_example, env_file)
            print("✅ Created .env file from example")
        
        # Install Python dependencies
        requirements_file = self.backend_dir / 'requirements.txt'
        if requirements_file.exists():
            result = self.run_command("pip install -r requirements.txt", cwd=self.backend_dir)
            if result is not None:
                print("✅ Python dependencies installed")
        
        # Initialize database
        setup_script = self.project_root / 'setup_database.py'
        if setup_script.exists():
            result = self.run_command("python setup_database.py")
            if result is not None:
                print("✅ Database initialized")
        
        print("✅ Development environment ready!")

    def show_status(self):
        """Show deployment status"""
        print("\n📊 Deployment Status")
        print("=" * 40)
        
        # Check Git status
        git_status = self.run_command("git status --porcelain")
        if git_status:
            print("📝 Uncommitted changes:")
            print(git_status)
        else:
            print("✅ Git: Clean working directory")
        
        # Check backend health
        if self.check_backend_health():
            print("✅ Backend: Running on localhost:5000")
        else:
            print("❌ Backend: Not running")
        
        # Check database
        db_file = self.project_root / 'database.db'
        if db_file.exists():
            print(f"✅ Database: {db_file} ({db_file.stat().st_size} bytes)")
        else:
            print("❌ Database: Not found")
        
        # Check docs sync
        if self.docs_dir.exists():
            print("✅ GitHub Pages: docs/ folder ready")
        else:
            print("❌ GitHub Pages: docs/ folder missing")

def main():
    """Main deployment function"""
    manager = DeploymentManager()
    
    if len(sys.argv) < 2:
        print("🚀 Trading Dashboard Deployment Manager")
        print("\nUsage:")
        print("  python deploy.py <command>")
        print("\nCommands:")
        print("  setup          - Setup development environment")
        print("  frontend       - Deploy frontend to GitHub Pages")
        print("  render         - Deploy to Render.com")
        print("  heroku         - Deploy to Heroku")
        print("  backup         - Create database backup")
        print("  migrate        - Run database migrations")
        print("  status         - Show deployment status")
        print("  sync           - Sync frontend to docs folder")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'setup':
        manager.setup_environment()
    elif command == 'frontend':
        manager.deploy_frontend()
    elif command == 'render':
        manager.deploy_to_render()
    elif command == 'heroku':
        manager.deploy_to_heroku()
    elif command == 'backup':
        manager.backup_database()
    elif command == 'migrate':
        manager.run_database_migrations()
    elif command == 'status':
        manager.show_status()
    elif command == 'sync':
        manager.sync_frontend_to_docs()
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python deploy.py' for help")

if __name__ == "__main__":
    main()