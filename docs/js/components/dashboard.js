// Dashboard Component - Handles main dashboard functionality
class Dashboard {
    constructor() {
        this.chart = null;
        this.init();
    }

    async init() {
        await this.loadDashboardData();
        this.setupEventListeners();
    }

    async loadDashboardData() {
        try {
            // Load all dashboard data
            const [accountStats, metrics, dailyStats, trades] = await Promise.all([
                api.getAccountStats(),
                api.getMetrics(),
                api.getDailyStats(),
                api.getTrades()
            ]);

            this.updateAccountSummary(accountStats);
            this.updateMetrics(metrics);
            this.updateConfluence(trades);
            this.updateChart(dailyStats);
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
            this.showError('Failed to load dashboard data');
        }
    }

    updateAccountSummary(stats) {
        const currentBalance = document.getElementById('currentBalance');
        const totalPnl = document.getElementById('totalPnl');
        const totalTrades = document.getElementById('totalTrades');
        const winLoss = document.getElementById('winLoss');
        const openTrades = document.getElementById('openTrades');

        currentBalance.textContent = this.formatCurrency(stats.current_balance);
        
        const pnlElement = totalPnl;
        const pnlText = `${stats.total_pnl >= 0 ? '+' : ''}${this.formatCurrency(stats.total_pnl)} (${stats.pnl_percentage.toFixed(2)}%)`;
        pnlElement.textContent = pnlText;
        pnlElement.className = `pnl ${stats.total_pnl >= 0 ? 'positive' : 'negative'}`;

        totalTrades.textContent = stats.total_trades;
        winLoss.textContent = `${stats.winning_trades}W / ${stats.losing_trades}L`;
        openTrades.textContent = stats.open_trades;
    }

    updateMetrics(metrics) {
        document.getElementById('profitFactor').textContent = metrics.profit_factor.toFixed(2);
        document.getElementById('winRate').textContent = `${metrics.win_rate.toFixed(1)}%`;
        document.getElementById('averageWin').textContent = this.formatCurrency(metrics.average_win);
        document.getElementById('averageLoss').textContent = this.formatCurrency(Math.abs(metrics.average_loss));
        document.getElementById('largestWin').textContent = this.formatCurrency(metrics.largest_win);
        document.getElementById('largestLoss').textContent = this.formatCurrency(Math.abs(metrics.largest_loss));
    }

    updateConfluence(trades) {
        const openTrades = trades.filter(trade => trade.status === 'OPEN');
        const overallConfluenceEl = document.getElementById('overallConfluence');
        const confluenceLevelEl = document.getElementById('confluenceLevel');

        if (openTrades.length === 0) {
            overallConfluenceEl.textContent = '0%';
            confluenceLevelEl.textContent = 'No Open Trades';
            confluenceLevelEl.className = 'confluence-level';
            return;
        }

        const avgConfluence = openTrades.reduce((sum, trade) => sum + trade.total_confluence, 0) / openTrades.length;
        overallConfluenceEl.textContent = `${avgConfluence.toFixed(1)}%`;

        let level, className;
        if (avgConfluence >= 70) {
            level = 'High Confluence';
            className = 'confluence-level high';
        } else if (avgConfluence >= 40) {
            level = 'Medium Confluence';
            className = 'confluence-level medium';
        } else {
            level = 'Low Confluence';
            className = 'confluence-level low';
        }

        confluenceLevelEl.textContent = level;
        confluenceLevelEl.className = className;
    }

    updateChart(dailyStats) {
        const ctx = document.getElementById('dailyPnlChart').getContext('2d');
        
        if (this.chart) {
            this.chart.destroy();
        }

        const labels = dailyStats.map(item => {
            const date = new Date(item.date);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });

        const data = dailyStats.map(item => item.pnl);
        const backgroundColors = data.map(pnl => pnl >= 0 ? 'rgba(72, 187, 120, 0.8)' : 'rgba(245, 101, 101, 0.8)');
        const borderColors = data.map(pnl => pnl >= 0 ? 'rgba(72, 187, 120, 1)' : 'rgba(245, 101, 101, 1)');

        this.chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Daily P&L',
                    data: data,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                return `P&L: ${this.formatCurrency(context.parsed.y)}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#a0aec0',
                            callback: (value) => this.formatCurrency(value)
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#a0aec0'
                        }
                    }
                }
            }
        });
    }

    setupEventListeners() {
        // Refresh dashboard when trades are updated
        document.addEventListener('tradesUpdated', () => {
            this.loadDashboardData();
        });
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }

    showError(message) {
        // Simple error display - could be enhanced with a proper notification system
        console.error(message);
        alert(message);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Dashboard();
});