from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configure Flask
frontend_dir = Path(__file__).parent.parent / 'frontend'
app = Flask(__name__, static_folder=str(frontend_dir), static_url_path='')
CORS(app)

# Simple JSON file database
DATA_FILE = Path(__file__).parent / 'trades_data.json'

def load_trades():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_trades(trades):
    with open(DATA_FILE, 'w') as f:
        json.dump(trades, f, indent=2, default=str)

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
    return jsonify(load_trades())

@app.route('/api/trades/<int:trade_id>', methods=['GET'])
def get_trade(trade_id):
    trades = load_trades()
    trade = next((t for t in trades if t['id'] == trade_id), None)
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    return jsonify(trade)

@app.route('/api/trades', methods=['POST'])
def create_trade():
    data = request.json
    trades = load_trades()
    
    # Generate ID
    new_id = max([t['id'] for t in trades], default=0) + 1
    
    # Calculate confluence
    total_confluence = round((
        data.get('weekly_tf', 0) +
        data.get('daily_tf', 0) +
        data.get('h4_tf', 0) +
        data.get('h1_tf', 0) +
        data.get('lower_tf', 0)
    ) / 5, 1)
    
    trade = {
        'id': new_id,
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
        'created_at': datetime.utcnow().isoformat(),
        'closed_at': None
    }
    
    # Calculate P&L
    if trade['exit_price']:
        if trade['direction'] == 'LONG':
            trade['pnl'] = (trade['exit_price'] - trade['entry_price']) * trade['lot_size'] * 100000
        else:
            trade['pnl'] = (trade['entry_price'] - trade['exit_price']) * trade['lot_size'] * 100000
        trade['pnl'] = round(trade['pnl'], 2)
        trade['closed_at'] = datetime.utcnow().isoformat()
    
    trades.append(trade)
    save_trades(trades)
    
    return jsonify(trade), 201

@app.route('/api/trades/<int:trade_id>', methods=['PUT'])
def update_trade(trade_id):
    trades = load_trades()
    trade = next((t for t in trades if t['id'] == trade_id), None)
    
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    data = request.json
    
    # Update fields
    for field in ['symbol', 'direction', 'entry_price', 'exit_price', 'lot_size',
                  'weekly_tf', 'daily_tf', 'h4_tf', 'h1_tf', 'lower_tf',
                  'risk_reward', 'notes']:
        if field in data:
            trade[field] = data[field]
    
    # Recalculate
    trade['total_confluence'] = round((
        trade['weekly_tf'] + trade['daily_tf'] + trade['h4_tf'] + 
        trade['h1_tf'] + trade['lower_tf']
    ) / 5, 1)
    
    if trade['exit_price']:
        if trade['direction'] == 'LONG':
            trade['pnl'] = (trade['exit_price'] - trade['entry_price']) * trade['lot_size'] * 100000
        else:
            trade['pnl'] = (trade['entry_price'] - trade['exit_price']) * trade['lot_size'] * 100000
        trade['pnl'] = round(trade['pnl'], 2)
        trade['status'] = 'CLOSED'
        trade['closed_at'] = datetime.utcnow().isoformat()
    
    save_trades(trades)
    return jsonify(trade)

@app.route('/api/trades/<int:trade_id>', methods=['DELETE'])
def delete_trade(trade_id):
    trades = load_trades()
    trades = [t for t in trades if t['id'] != trade_id]
    save_trades(trades)
    return '', 204

@app.route('/api/trades/stats/account', methods=['GET'])
def get_account_stats():
    trades = load_trades()
    
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
    closed_trades = [t for t in load_trades() if t.get('status') == 'CLOSED']
    
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
