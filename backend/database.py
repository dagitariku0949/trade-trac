"""
Enhanced Database Configuration with Multiple Database Support
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class DatabaseConfig:
    """Database configuration class supporting multiple database types"""
    
    def __init__(self):
        self.database_url = self._get_database_url()
        self.engine = create_engine(
            self.database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=os.getenv('SQL_DEBUG', 'False').lower() == 'true'
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def _get_database_url(self):
        """Get database URL based on environment"""
        # Check for specific database URLs first
        if os.getenv('DATABASE_URL'):
            return os.getenv('DATABASE_URL')
        
        # PostgreSQL (Production recommended)
        if os.getenv('POSTGRES_URL'):
            return os.getenv('POSTGRES_URL')
        
        # MySQL
        if os.getenv('MYSQL_URL'):
            return os.getenv('MYSQL_URL')
        
        # Build from individual components
        db_type = os.getenv('DB_TYPE', 'sqlite')
        
        if db_type == 'postgresql':
            user = os.getenv('DB_USER', 'postgres')
            password = os.getenv('DB_PASSWORD', '')
            host = os.getenv('DB_HOST', 'localhost')
            port = os.getenv('DB_PORT', '5432')
            name = os.getenv('DB_NAME', 'trading_dashboard')
            return f"postgresql://{user}:{password}@{host}:{port}/{name}"
        
        elif db_type == 'mysql':
            user = os.getenv('DB_USER', 'root')
            password = os.getenv('DB_PASSWORD', '')
            host = os.getenv('DB_HOST', 'localhost')
            port = os.getenv('DB_PORT', '3306')
            name = os.getenv('DB_NAME', 'trading_dashboard')
            return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"
        
        else:  # SQLite (default for development)
            db_path = os.getenv('DB_PATH', 'database.db')
            return f"sqlite:///{db_path}"
    
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_db(self):
        """Get database session"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Global database instance
db_config = DatabaseConfig()

def get_db():
    """Get database session - for backward compatibility"""
    return db_config.get_db()

def create_tables():
    """Create tables - for backward compatibility"""
    return db_config.create_tables()