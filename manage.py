#!/usr/bin/env python3
"""
Trading Dashboard Management CLI
Complete website management tool for adding, removing, and updating features
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
import subprocess

class TradingDashboardManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.frontend_dir = self.project_root / 'frontend'
        self.backend_dir = self.project_root / 'backend'
        self.components_dir = self.frontend_dir / 'js' / 'components'
        
    def run_command(self, command, cwd=None):
        """Execute shell command"""
        try:
            result = subprocess.run(
                command, shell=True, cwd=cwd or self.project_root,
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"❌ Error: {e.stderr}")
            return None

    def create_component(self, name, component_type='widget'):
        """Create a new frontend component"""
        print(f"🎨 Creating {component_type}: {name}")
        
        # Create component file
        component_file = self.components_dir / f"{name}.js"
        
        if component_file.exists():
            print(f"❌ Component {name} already exists")
            return False
        
        # Component template
        template = f'''/**
 * {name.title()} Component
 * Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 */

export function render{name.title()}(data) {{
    const container = document.getElementById('{name.lower()}-container');
    if (!container) {{
        console.error('{name} container not found');
        return;
    }}

    container.innerHTML = `
        <div class="{name.lower()}-{component_type}">
            <div class="{component_type}-header">
                <h3>{name.title()}</h3>
                <div class="{component_type}-controls">
                    <!-- Add controls here -->
                </div>
            </div>
            <div class="{component_type}-content">
                <!-- Add content here -->
                <p>Welcome to {name.title()}!</p>
            </div>
        </div>
    `;
}}

export function update{name.title()}(data) {{
    // Update component with new data
    console.log('Updating {name}:', data);
}}

// Initialize component
document.addEventListener('DOMContentLoaded', () => {{
    // Auto-initialize if container exists
    const container = document.getElementById('{name.lower()}-container');
    if (container) {{
        render{name.title()}({{}});
    }}
}});'''

        # Write component file
        component_file.write_text(template)
        print(f"✅ Created component: {component_file}")
        
        # Add CSS template
        self.add_component_styles(name, component_type)
        
        # Update main app.js
        self.update_main_app(name, 'add')
        
        return True

    def add_component_styles(self, name, component_type):
        """Add CSS styles for new component"""
        css_file = self.frontend_dir / 'css' / 'styles.css'
        
        styles = f'''
/* {name.title()} {component_type.title()} Styles */
.{name.lower()}-{component_type} {{
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 25px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}}

.{name.lower()}-{component_type}:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 212, 255, 0.2);
}}

.{component_type}-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}}

.{component_type}-header h3 {{
    color: #ffffff;
    font-size: 1.3rem;
    font-weight: 600;
    margin: 0;
}}

.{component_type}-controls {{
    display: flex;
    gap: 10px;
}}

.{component_type}-content {{
    color: #a0aec0;
    line-height: 1.6;
}}

@media (max-width: 768px) {{
    .{name.lower()}-{component_type} {{
        padding: 20px;
    }}
    
    .{component_type}-header {{
        flex-direction: column;
        align-items: flex-start;
        gap: 15px;
    }}
}}
'''
        
        # Append styles to CSS file
        with open(css_file, 'a') as f:
            f.write(styles)
        
        print(f"✅ Added CSS styles for {name}")

    def remove_component(self, name):
        """Remove a frontend component"""
        print(f"🗑️ Removing component: {name}")
        
        component_file = self.components_dir / f"{name}.js"
        
        if not component_file.exists():
            print(f"❌ Component {name} not found")
            return False
        
        # Remove component file
        component_file.unlink()
        print(f"✅ Removed component file: {component_file}")
        
        # Update main app.js
        self.update_main_app(name, 'remove')
        
        # Note: CSS removal would require more complex parsing
        print("ℹ️ Note: CSS styles need to be manually removed from styles.css")
        
        return True

    def update_main_app(self, component_name, action):
        """Update main app.js to include/exclude component"""
        app_file = self.frontend_dir / 'js' / 'app.js'
        
        if not app_file.exists():
            print("❌ app.js not found")
            return
        
        content = app_file.read_text()
        
        if action == 'add':
            # Add import statement
            import_line = f"import {{ render{component_name.title()} }} from './components/{component_name}.js';"
            
            if import_line not in content:
                # Find a good place to add the import
                lines = content.split('\n')
                import_index = 0
                for i, line in enumerate(lines):
                    if line.startswith('import'):
                        import_index = i + 1
                
                lines.insert(import_index, import_line)
                content = '\n'.join(lines)
                
                app_file.write_text(content)
                print(f"✅ Added {component_name} import to app.js")
        
        elif action == 'remove':
            # Remove import statement
            import_line = f"import {{ render{component_name.title()} }} from './components/{component_name}.js';"
            content = content.replace(import_line + '\n', '')
            content = content.replace(import_line, '')
            
            app_file.write_text(content)
            print(f"✅ Removed {component_name} import from app.js")

    def add_api_endpoint(self, endpoint_name, method='GET'):
        """Add new API endpoint"""
        print(f"🔌 Adding API endpoint: {method} /api/{endpoint_name}")
        
        api_routes_file = self.backend_dir / 'api_routes.py'
        
        if not api_routes_file.exists():
            print("❌ api_routes.py not found")
            return False
        
        # Endpoint template
        endpoint_code = f'''
    @app.route('/api/{endpoint_name}', methods=['{method}'])
    def {endpoint_name.replace('-', '_')}():
        """Handle {endpoint_name} requests"""
        db = next(get_db())
        
        try:
            # Add your logic here
            data = {{"message": "Hello from {endpoint_name}!"}}
            return jsonify(data)
            
        except Exception as e:
            return jsonify({{"error": str(e)}}), 500
'''
        
        # Read current content
        content = api_routes_file.read_text()
        
        # Find the return statement at the end
        if 'return app' in content:
            content = content.replace('return app', endpoint_code + '\n    return app')
        else:
            content += endpoint_code
        
        # Write back
        api_routes_file.write_text(content)
        print(f"✅ Added API endpoint: {endpoint_name}")
        
        return True

    def create_database_model(self, model_name, fields):
        """Create new database model"""
        print(f"🗄️ Creating database model: {model_name}")
        
        models_file = self.backend_dir / 'models.py'
        
        if not models_file.exists():
            print("❌ models.py not found")
            return False
        
        # Model template
        model_code = f'''
class {model_name}(Base):
    """Generated model for {model_name}"""
    __tablename__ = '{model_name.lower()}s'
    
    id = Column(Integer, primary_key=True)
'''
        
        # Add fields
        for field_name, field_type in fields.items():
            if field_type == 'string':
                model_code += f"    {field_name} = Column(String(255), nullable=True)\n"
            elif field_type == 'integer':
                model_code += f"    {field_name} = Column(Integer, nullable=True)\n"
            elif field_type == 'float':
                model_code += f"    {field_name} = Column(Float, nullable=True)\n"
            elif field_type == 'boolean':
                model_code += f"    {field_name} = Column(Boolean, default=False)\n"
            elif field_type == 'datetime':
                model_code += f"    {field_name} = Column(DateTime, default=datetime.utcnow)\n"
        
        # Add to_dict method
        model_code += f'''    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {{
            'id': self.id,
'''
        
        for field_name in fields.keys():
            model_code += f"            '{field_name}': self.{field_name},\n"
        
        model_code += '''            'created_at': self.created_at.isoformat() if self.created_at else None
        }
'''
        
        # Append to models file
        with open(models_file, 'a') as f:
            f.write(model_code)
        
        print(f"✅ Created model: {model_name}")
        print("ℹ️ Run 'python manage.py migrate' to apply database changes")
        
        return True

    def run_migrations(self):
        """Create and run database migrations"""
        print("🔄 Running database migrations...")
        
        # Create migration
        result = self.run_command("alembic revision --autogenerate -m 'Auto migration'", cwd=self.backend_dir)
        if result is None:
            print("❌ Failed to create migration")
            return False
        
        # Apply migration
        result = self.run_command("alembic upgrade head", cwd=self.backend_dir)
        if result is None:
            print("❌ Failed to apply migration")
            return False
        
        print("✅ Migrations completed successfully")
        return True

    def backup_project(self):
        """Create full project backup"""
        print("💾 Creating project backup...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = self.project_root.parent / f"trading_dashboard_backup_{timestamp}"
        
        # Copy entire project
        shutil.copytree(self.project_root, backup_dir, ignore=shutil.ignore_patterns(
            '__pycache__', '*.pyc', 'node_modules', '.git', 'venv', 'env'
        ))
        
        print(f"✅ Project backed up to: {backup_dir}")
        return str(backup_dir)

    def show_help(self):
        """Show help information"""
        print("""
🎛️ Trading Dashboard Management CLI

COMPONENT MANAGEMENT:
  add-component <name> [type]     - Create new frontend component
  remove-component <name>         - Remove frontend component
  list-components                 - List all components

API MANAGEMENT:
  add-endpoint <name> [method]    - Add new API endpoint
  list-endpoints                  - List all API endpoints

DATABASE MANAGEMENT:
  add-model <name> <fields>       - Create new database model
  migrate                         - Run database migrations
  backup-db                       - Backup database

PROJECT MANAGEMENT:
  backup                          - Create full project backup
  deploy <target>                 - Deploy to target (frontend/render/heroku)
  status                          - Show project status
  
EXAMPLES:
  python manage.py add-component portfolio widget
  python manage.py add-endpoint user-stats GET
  python manage.py add-model UserProfile name:string,age:integer
  python manage.py deploy frontend
        """)

def main():
    """Main CLI function"""
    manager = TradingDashboardManager()
    
    if len(sys.argv) < 2:
        manager.show_help()
        return
    
    command = sys.argv[1].lower()
    
    try:
        if command == 'add-component':
            name = sys.argv[2]
            comp_type = sys.argv[3] if len(sys.argv) > 3 else 'widget'
            manager.create_component(name, comp_type)
            
        elif command == 'remove-component':
            name = sys.argv[2]
            manager.remove_component(name)
            
        elif command == 'add-endpoint':
            name = sys.argv[2]
            method = sys.argv[3] if len(sys.argv) > 3 else 'GET'
            manager.add_api_endpoint(name, method)
            
        elif command == 'add-model':
            name = sys.argv[2]
            fields_str = sys.argv[3] if len(sys.argv) > 3 else 'name:string'
            fields = {}
            for field in fields_str.split(','):
                field_name, field_type = field.split(':')
                fields[field_name.strip()] = field_type.strip()
            manager.create_database_model(name, fields)
            
        elif command == 'migrate':
            manager.run_migrations()
            
        elif command == 'backup':
            manager.backup_project()
            
        elif command == 'deploy':
            target = sys.argv[2] if len(sys.argv) > 2 else 'frontend'
            from deploy import DeploymentManager
            deploy_manager = DeploymentManager()
            
            if target == 'frontend':
                deploy_manager.deploy_frontend()
            elif target == 'render':
                deploy_manager.deploy_to_render()
            elif target == 'heroku':
                deploy_manager.deploy_to_heroku()
            else:
                print(f"❌ Unknown deployment target: {target}")
                
        elif command == 'status':
            from deploy import DeploymentManager
            DeploymentManager().show_status()
            
        else:
            print(f"❌ Unknown command: {command}")
            manager.show_help()
            
    except IndexError:
        print("❌ Missing required arguments")
        manager.show_help()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()