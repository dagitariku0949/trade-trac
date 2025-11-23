from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Video(Base):
    __tablename__ = 'videos'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    video_url = Column(String(500), nullable=False)  # YouTube/Vimeo URL
    thumbnail_url = Column(String(500), nullable=True)
    category = Column(String(50), nullable=True)  # e.g., "Tutorial", "Analysis", "Strategy"
    duration = Column(String(20), nullable=True)  # e.g., "15:30"
    is_featured = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'video_url': self.video_url,
            'thumbnail_url': self.thumbnail_url,
            'category': self.category,
            'duration': self.duration,
            'is_featured': self.is_featured,
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), nullable=False)
    direction = Column(String(10), nullable=False)  # LONG or SHORT
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    lot_size = Column(Float, nullable=False)
    status = Column(String(10), default='OPEN')  # OPEN or CLOSED
    
    # Confluence scores (0-100)
    weekly_tf = Column(Integer, default=0)
    daily_tf = Column(Integer, default=0)
    h4_tf = Column(Integer, default=0)
    h1_tf = Column(Integer, default=0)
    lower_tf = Column(Integer, default=0)
    total_confluence = Column(Float, default=0)
    
    # Optional fields
    risk_reward = Column(Float, nullable=True)
    notes = Column(String(500), nullable=True)
    
    # Calculated fields
    pnl = Column(Float, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'direction': self.direction,
            'entry_price': self.entry_price,
            'exit_price': self.exit_price,
            'lot_size': self.lot_size,
            'status': self.status,
            'weekly_tf': self.weekly_tf,
            'daily_tf': self.daily_tf,
            'h4_tf': self.h4_tf,
            'h1_tf': self.h1_tf,
            'lower_tf': self.lower_tf,
            'total_confluence': self.total_confluence,
            'risk_reward': self.risk_reward,
            'notes': self.notes,
            'pnl': self.pnl,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None
        }

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()