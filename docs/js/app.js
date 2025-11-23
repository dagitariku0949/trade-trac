// Main Application Entry Point
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Trading Dashboard Loaded');
    
    // Initialize dashboard
    await loadDashboard();
    
    // Set up event listeners
    setupEventListeners();
    
    // Load initial data
    await refreshData();
});

async function loadDashboard() {
    try {
        await refreshData();
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showError('Failed to load dashboard data. Backend may not be running.');
    }
}

function setupEventListeners() {
    // New Trade Button
    const newTradeBtn = document.getElementById('newTradeBtn');
    if (newTradeBtn) {
        newTradeBtn.addEventListener('click', () => {
            openTradeModal();
        });
    }
    
    // Status Filter
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter) {
        statusFilter.addEventListener('change', async (e) => {
            await refreshData(e.target.value);
        });
    }
    
    // Modal Close Buttons
    const closeModal = document.getElementById('closeModal');
    if (closeModal) {
        closeModal.addEventListener('click', () => {
            document.getElementById('tradeModal').style.display = 'none';
        });
    }
    
    const cancelBtn = document.getElementById('cancelBtn');
    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
            document.getElementById('tradeModal').style.display = 'none';
        });
    }
    
    // Trade Form Submit
    const tradeForm = document.getElementById('tradeForm');
    if (tradeForm) {
        tradeForm.addEventListener('submit', handleTradeSubmit);
    }
    
    // Confluence Sliders
    setupConfluenceSliders();
}

function setupConfluenceSliders() {
    const sliders = ['weeklyTf', 'dailyTf', 'h4Tf', 'h1Tf', 'lowerTf'];
    
    sliders.forEach(sliderId => {
        const slider = document.getElementById(sliderId);
        const valueSpan = document.getElementById(sliderId.replace('Tf', 'Value'));
        
        if (slider && valueSpan) {
            slider.addEventListener('input', (e) => {
                valueSpan.textContent = e.target.value;
                updateTotalConfluence();
            });
        }
    });
}

function updateTotalConfluence() {
    const weekly = parseInt(document.getElementById('weeklyTf').value) || 0;
    const daily = parseInt(document.getElementById('dailyTf').value) || 0;
    const h4 = parseInt(document.getElementById('h4Tf').value) || 0;
    const h1 = parseInt(document.getElementById('h1Tf').value) || 0;
    const lower = parseInt(document.getElementById('lowerTf').value) || 0;
    
    const total = Math.round((weekly + daily + h4 + h1 + lower) / 5);
    document.getElementById('totalConfluence').textContent = total + '%';
}

async function refreshData(status = 'all') {
    try {
        // Try to load from API, but show demo data if backend is not available
        const trades = await api.getTrades().catch(() => []);
        const stats = await api.getAccountStats().catch(() => ({
            current_balance: 100000,
            starting_balance: 100000,
            total_pnl: 0,
            total_trades: 0,
            winning_trades: 0,
            losing_trades: 0,
            open_trades: 0
        }));
        const metrics = await api.getMetrics().catch(() => ({
            profit_factor: 0,
            win_rate: 0,
            average_win: 0,
            average_loss: 0,
            largest_win: 0,
            largest_loss: 0,
            average_confluence: 0
        }));
        
        // Update UI
        updateAccountSummary(stats);
        updateMetrics(metrics);
        updateTradesTable(trades, status);
        
        // Show warning if backend is not available
        if (trades.length === 0 && stats.total_trades === 0) {
            showWarning('Backend not connected. Showing demo interface only.');
        }
    } catch (error) {
        console.error('Error refreshing data:', error);
        showError('Backend not available. Please start the Python server.');
    }
}

function updateAccountSummary(stats) {
    document.getElementById('currentBalance').textContent = 
        '$' + stats.current_balance.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    
    const pnlPercent = ((stats.total_pnl / stats.starting_balance) * 100).toFixed(2);
    const pnlElement = document.getElementById('totalPnl');
    pnlElement.textContent = `${stats.total_pnl >= 0 ? '+' : ''}$${stats.total_pnl.toFixed(2)} (${pnlPercent}%)`;
    pnlElement.className = stats.total_pnl >= 0 ? 'pnl positive' : 'pnl negative';
    
    document.getElementById('totalTrades').textContent = stats.total_trades;
    document.getElementById('winLoss').textContent = `${stats.winning_trades}W / ${stats.losing_trades}L`;
    document.getElementById('openTrades').textContent = stats.open_trades;
}

function updateMetrics(metrics) {
    document.getElementById('profitFactor').textContent = metrics.profit_factor.toFixed(2);
    document.getElementById('winRate').textContent = metrics.win_rate.toFixed(1) + '%';
    document.getElementById('averageWin').textContent = '$' + metrics.average_win.toFixed(2);
    document.getElementById('averageLoss').textContent = '$' + metrics.average_loss.toFixed(2);
    document.getElementById('largestWin').textContent = '$' + metrics.largest_win.toFixed(2);
    document.getElementById('largestLoss').textContent = '$' + metrics.largest_loss.toFixed(2);
}

function updateTradesTable(trades, status) {
    const filteredTrades = status === 'all' ? trades : 
        trades.filter(t => t.status.toLowerCase() === status.toLowerCase());
    
    const tbody = document.getElementById('tradesTableBody');
    
    if (filteredTrades.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="9" style="text-align: center; padding: 40px; color: #a0aec0;">
                    No trades found. ${status !== 'all' ? 'Try changing the filter.' : 'Click "+ New Trade" to get started.'}
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = filteredTrades.map(trade => `
        <tr>
            <td><strong>${trade.symbol}</strong></td>
            <td><span class="direction-${trade.direction.toLowerCase()}">${trade.direction}</span></td>
            <td>${trade.entry_price.toFixed(5)}</td>
            <td>${trade.exit_price ? trade.exit_price.toFixed(5) : '-'}</td>
            <td>${trade.lot_size}</td>
            <td><span class="confluence-badge">${trade.total_confluence}%</span></td>
            <td class="${trade.pnl >= 0 ? 'pnl-positive' : 'pnl-negative'}">
                ${trade.pnl >= 0 ? '+' : ''}$${trade.pnl.toFixed(2)}
            </td>
            <td><span class="status-badge status-${trade.status.toLowerCase()}">${trade.status}</span></td>
            <td>
                ${trade.status === 'OPEN' ? `<button class="btn btn-success btn-small" onclick="closeTrade(${trade.id})">Close</button>` : ''}
                <button class="btn btn-secondary btn-small" onclick="editTrade(${trade.id})">Edit</button>
                <button class="btn btn-danger btn-small" onclick="deleteTrade(${trade.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

function openTradeModal(trade = null) {
    const modal = document.getElementById('tradeModal');
    const form = document.getElementById('tradeForm');
    const title = document.getElementById('modalTitle');
    
    if (trade) {
        title.textContent = 'Edit Trade';
        // Populate form with trade data
        document.getElementById('symbol').value = trade.symbol;
        document.getElementById('direction').value = trade.direction;
        document.getElementById('entryPrice').value = trade.entry_price;
        document.getElementById('exitPrice').value = trade.exit_price || '';
        document.getElementById('lotSize').value = trade.lot_size;
        document.getElementById('weeklyTf').value = trade.weekly_tf;
        document.getElementById('dailyTf').value = trade.daily_tf;
        document.getElementById('h4Tf').value = trade.h4_tf;
        document.getElementById('h1Tf').value = trade.h1_tf;
        document.getElementById('lowerTf').value = trade.lower_tf;
        document.getElementById('riskReward').value = trade.risk_reward || '';
        document.getElementById('notes').value = trade.notes || '';
        
        form.dataset.tradeId = trade.id;
    } else {
        title.textContent = 'New Trade';
        form.reset();
        delete form.dataset.tradeId;
    }
    
    updateTotalConfluence();
    modal.style.display = 'block';
}

async function handleTradeSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Convert numeric fields
    data.entry_price = parseFloat(data.entry_price);
    data.exit_price = data.exit_price ? parseFloat(data.exit_price) : null;
    data.lot_size = parseFloat(data.lot_size);
    data.weekly_tf = parseInt(data.weekly_tf);
    data.daily_tf = parseInt(data.daily_tf);
    data.h4_tf = parseInt(data.h4_tf);
    data.h1_tf = parseInt(data.h1_tf);
    data.lower_tf = parseInt(data.lower_tf);
    data.risk_reward = data.risk_reward ? parseFloat(data.risk_reward) : null;
    
    try {
        if (form.dataset.tradeId) {
            await api.updateTrade(form.dataset.tradeId, data);
        } else {
            await api.createTrade(data);
        }
        
        document.getElementById('tradeModal').style.display = 'none';
        await refreshData();
        showSuccess('Trade saved successfully!');
    } catch (error) {
        console.error('Error saving trade:', error);
        showError('Failed to save trade. Make sure the backend server is running.');
    }
}

async function closeTrade(id) {
    const exitPrice = prompt('Enter exit price:');
    if (!exitPrice) return;
    
    try {
        await api.updateTrade(id, { exit_price: parseFloat(exitPrice), status: 'CLOSED' });
        await refreshData();
        showSuccess('Trade closed successfully!');
    } catch (error) {
        console.error('Error closing trade:', error);
        showError('Failed to close trade.');
    }
}

async function editTrade(id) {
    try {
        const trade = await api.getTrade(id);
        openTradeModal(trade);
    } catch (error) {
        console.error('Error loading trade:', error);
        showError('Failed to load trade.');
    }
}

async function deleteTrade(id) {
    if (!confirm('Are you sure you want to delete this trade?')) return;
    
    try {
        await api.deleteTrade(id);
        await refreshData();
        showSuccess('Trade deleted successfully!');
    } catch (error) {
        console.error('Error deleting trade:', error);
        showError('Failed to delete trade.');
    }
}

function showSuccess(message) {
    alert(message);
}

function showError(message) {
    alert('Error: ' + message);
}

function showWarning(message) {
    console.warn(message);
}
