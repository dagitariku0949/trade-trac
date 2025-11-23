// Trades Table Component - Handles trade list display and actions
export function renderTradesTable(trades, onClose, onEdit, onDelete) {
    const container = document.getElementById('trades-table');
    if (!container) return;

    if (!trades || trades.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No trades yet. Click "+ New Trade" to get started.</p>
            </div>
        `;
        return;
    }

    const tableHTML = `
        <div class="table-container">
            <table class="trades-table">
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Direction</th>
                        <th>Entry</th>
                        <th>Exit</th>
                        <th>Lot Size</th>
                        <th>P&L</th>
                        <th>Confluence</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${trades.map(trade => `
                        <tr>
                            <td><strong>${trade.symbol}</strong></td>
                            <td>
                                <span class="badge badge-${trade.direction.toLowerCase()}">
                                    ${trade.direction}
                                </span>
                            </td>
                            <td>${trade.entry_price.toFixed(5)}</td>
                            <td>${trade.exit_price ? trade.exit_price.toFixed(5) : '-'}</td>
                            <td>${trade.lot_size}</td>
                            <td class="${trade.pnl >= 0 ? 'profit' : 'loss'}">
                                ${trade.pnl >= 0 ? '+' : ''}$${trade.pnl.toFixed(2)}
                            </td>
                            <td>
                                <span class="confluence-badge ${getConfluenceClass(trade.total_confluence)}">
                                    ${trade.total_confluence}%
                                </span>
                            </td>
                            <td>
                                <span class="badge badge-${trade.status.toLowerCase()}">
                                    ${trade.status}
                                </span>
                            </td>
                            <td class="actions">
                                ${trade.status === 'OPEN' ? `
                                    <button class="btn btn-sm btn-success" onclick="window.handleCloseTrade(${trade.id})">
                                        Close
                                    </button>
                                ` : ''}
                                <button class="btn btn-sm btn-secondary" onclick="window.handleEditTrade(${trade.id})">
                                    Edit
                                </button>
                                <button class="btn btn-sm btn-danger" onclick="window.handleDeleteTrade(${trade.id})">
                                    Delete
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;

    container.innerHTML = tableHTML;

    // Attach handlers to window for onclick access
    window.handleCloseTrade = onClose;
    window.handleEditTrade = onEdit;
    window.handleDeleteTrade = onDelete;
}

function getConfluenceClass(confluence) {
    if (confluence >= 70) return 'high';
    if (confluence >= 40) return 'medium';
    return 'low';
}