from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

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
    """Enhanced Trade model with new features"""
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    
    # Foreign Keys
    account_id = Column(Integer, ForeignKey('trading_accounts.id'), nullable=True)
    strategy_id = Column(Integer, ForeignKey('trading_strategies.id'), nullable=True)
    
    # Basic Trade Info
    symbol = Column(String(20), nullable=False)
    direction = Column(String(10), nullable=False)  # LONG or SHORT
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    lot_size = Column(Float, nullable=False)
    status = Column(String(10), default='OPEN')  # OPEN, CLOSED, CANCELLED
    
    # Enhanced Trade Details
    trade_type = Column(String(20), default='MARKET')  # MARKET, LIMIT, STOP
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    commission = Column(Float, default=0)
    swap = Column(Float, default=0)
    
    # Confluence scores (0-100)
    weekly_tf = Column(Integer, default=0)
    daily_tf = Column(Integer, default=0)
    h4_tf = Column(Integer, default=0)
    h1_tf = Column(Integer, default=0)
    lower_tf = Column(Integer, default=0)
    total_confluence = Column(Float, default=0)
    
    # Risk Management
    risk_reward = Column(Float, nullable=True)
    risk_percentage = Column(Float, nullable=True)  # % of account risked
    position_size_usd = Column(Float, nullable=True)
    
    # Trade Analysis
    setup_quality = Column(Integer, nullable=True)  # 1-10 rating
    execution_quality = Column(Integer, nullable=True)  # 1-10 rating
    market_condition = Column(String(20), nullable=True)  # TRENDING, RANGING, VOLATILE
    session = Column(String(20), nullable=True)  # LONDON, NEW_YORK, ASIAN, OVERLAP
    
    # Notes and Tags
    notes = Column(Text, nullable=True)
    tags = Column(String(200), nullable=True)  # Comma-separated tag names
    
    # Calculated fields
    pnl = Column(Float, default=0)
    pnl_percentage = Column(Float, default=0)
    duration_minutes = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    entry_time = Column(DateTime, nullable=True)
    exit_time = Column(DateTime, nullable=True)
    
    # Relationships
    account = relationship("TradingAccount", back_populates="trades")
    strategy = relationship("TradingStrategy", back_populates="trades")
    images = relationship("TradeImage", back_populates="trade", cascade="all, delete-orphan")
    
    # Indexes for better performance
    __table_args__ = (
        Index('idx_trade_symbol_date', 'symbol', 'created_at'),
        Index('idx_trade_status', 'status'),
        Index('idx_trade_account', 'account_id'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'strategy_id': self.strategy_id,
            'symbol': self.symbol,
            'direction': self.direction,
            'entry_price': self.entry_price,
            'exit_price': self.exit_price,
            'lot_size': self.lot_size,
            'status': self.status,
            'trade_type': self.trade_type,
            'stop_loss': self.stop_loss,
            'take_profit': self.take_profit,
            'commission': self.commission,
            'swap': self.swap,
            'weekly_tf': self.weekly_tf,
            'daily_tf': self.daily_tf,
            'h4_tf': self.h4_tf,
            'h1_tf': self.h1_tf,
            'lower_tf': self.lower_tf,
            'total_confluence': self.total_confluence,
            'risk_reward': self.risk_reward,
            'risk_percentage': self.risk_percentage,
            'position_size_usd': self.position_size_usd,
            'setup_quality': self.setup_quality,
            'execution_quality': self.execution_quality,
            'market_condition': self.market_condition,
            'session': self.session,
            'notes': self.notes,
            'tags': self.tags,
            'pnl': self.pnl,
            'pnl_percentage': self.pnl_percentage,
            'duration_minutes': self.duration_minutes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None,
            'entry_time': self.entry_time.isoformat() if self.entry_time else None,
            'exit_time': self.exit_time.isoformat() if self.exit_time else None,
            'images': [img.to_dict() for img in self.images] if self.images else []
        }

# New Models for Enhanced Features

class TradingAccount(Base):
    """Trading account model for multi-account support"""
    __tablename__ = 'trading_accounts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    account_type = Column(String(20), default='DEMO')  # DEMO, LIVE
    broker = Column(String(50), nullable=True)
    starting_balance = Column(Float, default=100000)
    current_balance = Column(Float, default=100000)
    currency = Column(String(3), default='USD')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    trades = relationship("Trade", back_populates="account")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'account_type': self.account_type,
            'broker': self.broker,
            'starting_balance': self.starting_balance,
            'current_balance': self.current_balance,
            'currency': self.currency,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class TradingStrategy(Base):
    """Trading strategy model"""
    __tablename__ = 'trading_strategies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    rules = Column(Text, nullable=True)  # JSON string of strategy rules
    win_rate_target = Column(Float, nullable=True)
    risk_reward_target = Column(Float, nullable=True)
    max_daily_trades = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    trades = relationship("Trade", back_populates="strategy")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'rules': self.rules,
            'win_rate_target': self.win_rate_target,
            'risk_reward_target': self.risk_reward_target,
            'max_daily_trades': self.max_daily_trades,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class TradeTag(Base):
    """Trade tags for categorization"""
    __tablename__ = 'trade_tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    color = Column(String(7), default='#00d4ff')  # Hex color
    description = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class TradeImage(Base):
    """Trade screenshots/charts"""
    __tablename__ = 'trade_images'
    
    id = Column(Integer, primary_key=True)
    trade_id = Column(Integer, ForeignKey('trades.id'), nullable=False)
    image_url = Column(String(500), nullable=False)
    image_type = Column(String(20), default='CHART')  # CHART, ENTRY, EXIT, ANALYSIS
    description = Column(String(200), nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    trade = relationship("Trade", back_populates="images")
    
    def to_dict(self):
        return {
            'id': self.id,
            'trade_id': self.trade_id,
            'image_url': self.image_url,
            'image_type': self.image_type,
            'description': self.description,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }