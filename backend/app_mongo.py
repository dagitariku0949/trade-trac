from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

# Configure Flask
frontend_dir = Path(__file__).parent.parent / 'frontend'
app = Flask(__name__, static_folder=str(frontend_dir), static_url_path='')
CORS(app)

# MongoDB connection
MONGO_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['trading_dashboard']
trades_collection = db['trades']

# Helper to convert ObjectId to string
def serialize_trade(trade):
    if trade:
        trade['_id'] = str(trade['_id'])
    return trade

# Serve frontend
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory(app.static_folder, path)
    except:
        return send_from_directory(app.static_folder, 'index.html')

# API Routes
@app.route('/api/trades', methods=['GET'])
def get_trades():
    trades = list(trades_collection.find())
    return jsonify([serialize_trade(t) for t in trades])

@app.route('/api/trades/<trade_id>', methods=['GET'])
def get_trade(trade_id):
    trade = trades_collection.find_one({'_id': ObjectId(trade_id)})
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    return jsonify(serialize_trade(trade))

@app.route('/api/trades', methods=['POST'])
def create_trade():
    data = request.json
    
    # Calculate confluence
    total_confluence = round((
        data.get('weekly_tf', 0) +
        data.get('daily_tf', 0) +
        data.get('h4_tf', 0) +
        data.get('h1_tf', 0) +
        data.get('lower_tf', 0)
    ) / 5, 1)
    
    trade = {
        'symbol': data['symbol'],
        'direction': data['direction'],
        'entry_price': data['entry_price'],
        'exit_price': data.get('exit_price'),
        'lot_size': data['lot_size'],
        'weekly_tf': data.get('weekly_tf', 0),
        'daily_tf': data.get('daily_tf', 0),
        'h4_tf': data.get('h4_tf', 0),
        'h1_tf': data.get('h1_tf', 0),
        'lower_tf': data.get('lower_tf', 0),
        'total_confluence': total_confluence,
        'risk_reward': data.get('risk_reward'),
        'notes': data.get('notes'),
        'status': 'CLOSED' if data.get('exit_price') else 'OPEN',
        'pnl': 0,
        'created_at': datetime.utcnow(),
        'closed_at': None
    }
    
    # Calculate P&L if closed
    if trade['exit_price']:
        if trade['direction'] == 'LONG':
            trade['pnl'] = (trade['exit_price'] - trade['entry_price']) * trade['lot_size'] * 100000
        else:
            trade['pnl'] = (trade['entry_price'] - trade['exit_price']) * trade['lot_size'] * 100000
        trade['pnl'] = round(trade['pnl'], 2)
        trade['closed_at'] = datetime.utcnow()
    
    result = trades_collection.insert_one(trade)
    trade['_id'] = str(result.inserted_id)
    
    return jsonify(trade), 201

@app.route('/api/trades/<trade_id>', methods=['PUT'])
def update_trade(trade_id):
    data = request.json
    
    update_data = {}
    for field in ['symbol', 'direction', 'entry_price', 'exit_price', 'lot_size',
                  'weekly_tf', 'daily_tf', 'h4_tf', 'h1_tf', 'lower_tf',
                  'risk_reward', 'notes']:
        if field in data:
            update_data[field] = data[field]
    
    # Recalculate confluence
    if any(f in data for f in ['weekly_tf', 'daily_tf', 'h4_tf', 'h1_tf', 'lower_tf']):
        trade = trades_collection.find_one({'_id': ObjectId(trade_id)})
        update_data['total_confluence'] = round((
            update_data.get('weekly_tf', trade.get('weekly_tf', 0)) +
            update_data.get('daily_tf', trade.get('daily_tf', 0)) +
            update_data.get('h4_tf', trade.get('h4_tf', 0)) +
            update_data.get('h1_tf', trade.get('h1_tf', 0)) +
            update_data.get('lower_tf', trade.get('lower_tf', 0))
        ) / 5, 1)
    
    # Update status and P&L
    if 'exit_price' in data and data['exit_price']:
        trade = trades_collection.find_one({'_id': ObjectId(trade_id)})
        entry = update_data.get('entry_price', trade['entry_price'])
        exit_p = data['exit_price']
        lot = update_data.get('lot_size', trade['lot_size'])
        direction = update_data.get('direction', trade['direction'])
        
        if direction == 'LONG':
            pnl = (exit_p - entry) * lot * 100000
        else:
            pnl = (entry - exit_p) * lot * 100000
        
        update_data['pnl'] = round(pnl, 2)
        update_data['status'] = 'CLOSED'
        update_data['closed_at'] = datetime.utcnow()
    
    trades_collection.update_one({'_id': ObjectId(trade_id)}, {'$set': update_data})
    
    trade = trades_collection.find_one({'_id': ObjectId(trade_id)})
    return jsonify(serialize_trade(trade))

@app.route('/api/trades/<trade_id>', methods=['DELETE'])
def delete_trade(trade_id):
    trades_collection.delete_one({'_id': ObjectId(trade_id)})
    return '', 204

@app.route('/api/trades/stats/account', methods=['GET'])
def get_account_stats():
    trades = list(trades_collection.find())
    
    starting_balance = 100000
    total_pnl = sum(t.get('pnl', 0) for t in trades if t.get('status') == 'CLOSED')
    current_balance = starting_balance + total_pnl
    
    total_trades = len([t for t in trades if t.get('status') == 'CLOSED'])
    open_trades = len([t for t in trades if t.get('status') == 'OPEN'])
    winning_trades = len([t for t in trades if t.get('status') == 'CLOSED' and t.get('pnl', 0) > 0])
    
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
    closed_trades = list(trades_collection.find({'status': 'CLOSED'}))
    
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
    
    winning = [t for t in closed_trades if t.get('pnl', 0) > 0]
    losing = [t for t in closed_trades if t.get('pnl', 0) < 0]
    
    gross_profit = sum(t.get('pnl', 0) for t in winning)
    gross_loss = abs(sum(t.get('pnl', 0) for t in losing))
    
    return jsonify({
        'profit_factor': round(gross_profit / gross_loss, 2) if gross_loss > 0 else 0,
        'win_rate': round(len(winning) / len(closed_trades) * 100, 1),
        'average_win': round(gross_profit / len(winning), 2) if winning else 0,
        'average_loss': round(gross_loss / len(losing), 2) if losing else 0,
        'largest_win': round(max((t.get('pnl', 0) for t in winning), default=0), 2),
        'largest_loss': round(min((t.get('pnl', 0) for t in losing), default=0), 2),
        'average_confluence': round(sum(t.get('total_confluence', 0) for t in closed_trades) / len(closed_trades), 1)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') != 'production')
