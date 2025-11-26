from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Trade, Video, TradingAccount, TradingStrategy, TradeTag, TradeImage
from database import db_config, get_db
from api_routes import register_enhanced_routes
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Create database tables
db_config.create_tables()

# Register enhanced API routes
register_enhanced_routes(app)

def calculate_pnl(trade):
    """Calculate P&L for a trade"""
    if not trade.exit_price:
        return 0
    
    if trade.direction == 'LONG':
        pnl = (trade.exit_price - trade.entry_price) * trade.lot_size * 100000
    else:  # SHORT
        pnl = (trade.entry_price - trade.exit_price) * trade.lot_size * 100000
    
    return round(pnl, 2)

def calculate_confluence(weekly, daily, h4, h1, lower):
    """Calculate total confluence from individual timeframes"""
    return round((weekly + daily + h4 + h1 + lower) / 5, 1)

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'Trading Dashboard API',
        'status': 'running',
        'endpoints': {
            'trades': '/api/trades',
            'account_stats': '/api/trades/stats/account',
            'metrics': '/api/trades/stats/metrics',
            'daily_stats': '/api/trades/stats/daily'
        }
    })

@app.route('/api/trades', methods=['GET'])
def get_trades():
    db = next(get_db())
    trades = db.query(Trade).all()
    return jsonify([trade.to_dict() for trade in trades])

@app.route('/api/trades/<int:trade_id>', methods=['GET'])
def get_trade(trade_id):
    db = next(get_db())
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    return jsonify(trade.to_dict())

@app.route('/api/trades', methods=['POST'])
def create_trade():
    db = next(get_db())
    data = request.json
    
    # Calculate total confluence
    total_confluence = calculate_confluence(
        data.get('weekly_tf', 0),
        data.get('daily_tf', 0),
        data.get('h4_tf', 0),
        data.get('h1_tf', 0),
        data.get('lower_tf', 0)
    )
    
    trade = Trade(
        symbol=data['symbol'],
        direction=data['direction'],
        entry_price=data['entry_price'],
        exit_price=data.get('exit_price'),
        lot_size=data['lot_size'],
        weekly_tf=data.get('weekly_tf', 0),
        daily_tf=data.get('daily_tf', 0),
        h4_tf=data.get('h4_tf', 0),
        h1_tf=data.get('h1_tf', 0),
        lower_tf=data.get('lower_tf', 0),
        total_confluence=total_confluence,
        risk_reward=data.get('risk_reward'),
        notes=data.get('notes'),
        status='CLOSED' if data.get('exit_price') else 'OPEN'
    )
    
    # Calculate P&L if exit price provided
    if trade.exit_price:
        trade.pnl = calculate_pnl(trade)
        trade.closed_at = datetime.utcnow()
    
    db.add(trade)
    db.commit()
    db.refresh(trade)
    
    return jsonify(trade.to_dict()), 201

@app.route('/api/trades/<int:trade_id>', methods=['PUT'])
def update_trade(trade_id):
    db = next(get_db())
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    data = request.json
    
    # Update fields
    for field in ['symbol', 'direction', 'entry_price', 'exit_price', 'lot_size', 
                  'weekly_tf', 'daily_tf', 'h4_tf', 'h1_tf', 'lower_tf', 
                  'risk_reward', 'notes']:
        if field in data:
            setattr(trade, field, data[field])
    
    # Recalculate confluence
    trade.total_confluence = calculate_confluence(
        trade.weekly_tf, trade.daily_tf, trade.h4_tf, trade.h1_tf, trade.lower_tf
    )
    
    # Update status and P&L
    if trade.exit_price:
        trade.status = 'CLOSED'
        trade.pnl = calculate_pnl(trade)
        if not trade.closed_at:
            trade.closed_at = datetime.utcnow()
    else:
        trade.status = 'OPEN'
        trade.pnl = 0
        trade.closed_at = None
    
    db.commit()
    return jsonify(trade.to_dict())

@app.route('/api/trades/<int:trade_id>/close', methods=['POST'])
def close_trade(trade_id):
    db = next(get_db())
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    data = request.json
    trade.exit_price = data['exit_price']
    trade.status = 'CLOSED'
    trade.pnl = calculate_pnl(trade)
    trade.closed_at = datetime.utcnow()
    
    db.commit()
    return jsonify(trade.to_dict())

@app.route('/api/trades/<int:trade_id>', methods=['DELETE'])
def delete_trade(trade_id):
    db = next(get_db())
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    db.delete(trade)
    db.commit()
    return '', 204

@app.route('/api/trades/stats/account', methods=['GET'])
def get_account_stats():
    db = next(get_db())
    trades = db.query(Trade).all()
    
    starting_balance = 100000  # Default starting balance
    total_pnl = sum(trade.pnl for trade in trades if trade.status == 'CLOSED')
    current_balance = starting_balance + total_pnl
    
    total_trades = len([t for t in trades if t.status == 'CLOSED'])
    open_trades = len([t for t in trades if t.status == 'OPEN'])
    winning_trades = len([t for t in trades if t.status == 'CLOSED' and t.pnl > 0])
    
    return jsonify({
        'starting_balance': starting_balance,
        'current_balance': current_balance,
        'total_pnl': total_pnl,
        'pnl_percentage': (total_pnl / starting_balance * 100) if starting_balance > 0 else 0,
        'total_trades': total_trades,
        'open_trades': open_trades,
        'winning_trades': winning_trades,
        'losing_trades': total_trades - winning_trades
    })

@app.route('/api/trades/stats/metrics', methods=['GET'])
def get_metrics():
    db = next(get_db())
    closed_trades = db.query(Trade).filter(Trade.status == 'CLOSED').all()
    
    if not closed_trades:
        return jsonify({
            'profit_factor': 0,
            'win_rate': 0,
            'average_win': 0,
            'average_loss': 0,
            'largest_win': 0,
            'largest_loss': 0,
            'average_confluence': 0
        })
    
    winning_trades = [t for t in closed_trades if t.pnl > 0]
    losing_trades = [t for t in closed_trades if t.pnl < 0]
    
    gross_profit = sum(t.pnl for t in winning_trades)
    gross_loss = abs(sum(t.pnl for t in losing_trades))
    
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
    win_rate = len(winning_trades) / len(closed_trades) * 100
    
    average_win = gross_profit / len(winning_trades) if winning_trades else 0
    average_loss = gross_loss / len(losing_trades) if losing_trades else 0
    
    largest_win = max((t.pnl for t in winning_trades), default=0)
    largest_loss = min((t.pnl for t in losing_trades), default=0)
    
    average_confluence = sum(t.total_confluence for t in closed_trades) / len(closed_trades)
    
    return jsonify({
        'profit_factor': round(profit_factor, 2),
        'win_rate': round(win_rate, 1),
        'average_win': round(average_win, 2),
        'average_loss': round(average_loss, 2),
        'largest_win': round(largest_win, 2),
        'largest_loss': round(largest_loss, 2),
        'average_confluence': round(average_confluence, 1)
    })

@app.route('/api/trades/stats/daily', methods=['GET'])
def get_daily_stats():
    db = next(get_db())
    closed_trades = db.query(Trade).filter(Trade.status == 'CLOSED').all()
    
    daily_pnl = {}
    for trade in closed_trades:
        if trade.closed_at:
            date = trade.closed_at.strftime('%Y-%m-%d')
            daily_pnl[date] = daily_pnl.get(date, 0) + trade.pnl
    
    return jsonify([
        {'date': date, 'pnl': round(pnl, 2)}
        for date, pnl in sorted(daily_pnl.items())
    ])

@app.route('/api/trades/stats/monthly', methods=['GET'])
def get_monthly_stats():
    db = next(get_db())
    year = request.args.get('year', datetime.utcnow().year, type=int)
    month = request.args.get('month', datetime.utcnow().month, type=int)
    
    # Get trades for the specified month
    from datetime import date
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    closed_trades = db.query(Trade).filter(
        Trade.status == 'CLOSED',
        Trade.closed_at >= start_date,
        Trade.closed_at < end_date
    ).all()
    
    # Calculate daily P&L
    daily_pnl = {}
    daily_trades = {}
    for trade in closed_trades:
        if trade.closed_at:
            date_str = trade.closed_at.strftime('%Y-%m-%d')
            daily_pnl[date_str] = daily_pnl.get(date_str, 0) + trade.pnl
            daily_trades[date_str] = daily_trades.get(date_str, 0) + 1
    
    # Calculate monthly stats
    total_pnl = sum(daily_pnl.values())
    winning_days = len([pnl for pnl in daily_pnl.values() if pnl > 0])
    losing_days = len([pnl for pnl in daily_pnl.values() if pnl < 0])
    total_days = len(daily_pnl)
    
    best_day = max(daily_pnl.items(), key=lambda x: x[1]) if daily_pnl else (None, 0)
    worst_day = min(daily_pnl.items(), key=lambda x: x[1]) if daily_pnl else (None, 0)
    
    return jsonify({
        'year': year,
        'month': month,
        'total_pnl': round(total_pnl, 2),
        'total_trades': len(closed_trades),
        'trading_days': total_days,
        'winning_days': winning_days,
        'losing_days': losing_days,
        'win_rate': round((winning_days / total_days * 100) if total_days > 0 else 0, 1),
        'best_day': {'date': best_day[0], 'pnl': round(best_day[1], 2)},
        'worst_day': {'date': worst_day[0], 'pnl': round(worst_day[1], 2)},
        'average_daily_pnl': round(total_pnl / total_days, 2) if total_days > 0 else 0,
        'daily_data': [
            {
                'date': date_str,
                'pnl': round(pnl, 2),
                'trades': daily_trades.get(date_str, 0)
            }
            for date_str, pnl in sorted(daily_pnl.items())
        ]
    })

# ============= VIDEO MANAGEMENT ROUTES =============

@app.route('/api/videos', methods=['GET'])
def get_videos():
    """Get all videos"""
    db = next(get_db())
    category = request.args.get('category')
    featured = request.args.get('featured')
    
    query = db.query(Video)
    
    if category:
        query = query.filter(Video.category == category)
    if featured == 'true':
        query = query.filter(Video.is_featured == True)
    
    videos = query.order_by(Video.created_at.desc()).all()
    return jsonify([video.to_dict() for video in videos])

@app.route('/api/videos/<int:video_id>', methods=['GET'])
def get_video(video_id):
    """Get a single video by ID"""
    db = next(get_db())
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        return jsonify({'error': 'Video not found'}), 404
    
    # Increment view count
    video.view_count += 1
    db.commit()
    
    return jsonify(video.to_dict())

@app.route('/api/videos', methods=['POST'])
def create_video():
    """Create a new video entry"""
    db = next(get_db())
    data = request.json
    
    video = Video(
        title=data['title'],
        description=data.get('description'),
        video_url=data['video_url'],
        thumbnail_url=data.get('thumbnail_url'),
        category=data.get('category'),
        duration=data.get('duration'),
        is_featured=data.get('is_featured', False)
    )
    
    db.add(video)
    db.commit()
    db.refresh(video)
    
    return jsonify(video.to_dict()), 201

@app.route('/api/videos/<int:video_id>', methods=['PUT'])
def update_video(video_id):
    """Update a video"""
    db = next(get_db())
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        return jsonify({'error': 'Video not found'}), 404
    
    data = request.json
    
    if 'title' in data:
        video.title = data['title']
    if 'description' in data:
        video.description = data['description']
    if 'video_url' in data:
        video.video_url = data['video_url']
    if 'thumbnail_url' in data:
        video.thumbnail_url = data['thumbnail_url']
    if 'category' in data:
        video.category = data['category']
    if 'duration' in data:
        video.duration = data['duration']
    if 'is_featured' in data:
        video.is_featured = data['is_featured']
    
    db.commit()
    db.refresh(video)
    
    return jsonify(video.to_dict())

@app.route('/api/videos/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    """Delete a video"""
    db = next(get_db())
    video = db.query(Video).filter(Video.id == video_id).first()
    
    if not video:
        return jsonify({'error': 'Video not found'}), 404
    
    db.delete(video)
    db.commit()
    
    return jsonify({'message': 'Video deleted successfully'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)