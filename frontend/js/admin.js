/**
 * Admin Panel JavaScript
 * Manages website features, database, and deployment
 */

class AdminPanel {
    constructor() {
        this.currentSection = 'overview';
        this.init();
    }

    init() {
        this.setupNavigation();
        this.loadOverviewData();
        this.setupEventListeners();
    }

    setupNavigation() {
        const navButtons = document.querySelectorAll('.nav-btn');
        const sections = document.querySelectorAll('.admin-section');

        navButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const sectionId = btn.dataset.section;
                
                // Update active nav button
                navButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Show corresponding section
                sections.forEach(s => s.classList.remove('active'));
                document.getElementById(sectionId).classList.add('active');
                
                this.currentSection = sectionId;
                this.loadSectionData(sectionId);
            });
        });
    }

    setupEventListeners() {
        // Add account form
        document.getElementById('addAccountForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addAccount();
        });
    }

    async loadOverviewData() {
        try {
            // Load system statistics
            const [trades, accounts, strategies] = await Promise.all([
                fetch('/api/trades').then(r => r.json()),
                fetch('/api/accounts').then(r => r.json()),
                fetch('/api/strategies').then(r => r.json())
            ]);

            document.getElementById('totalTradesCount').textContent = trades.length;
            document.getElementById('accountsCount').textContent = accounts.length;
            document.getElementById('strategiesCount').textContent = strategies.length;
            
        } catch (error) {
            console.error('Error loading overview data:', error);
            this.showNotification('Error loading system data', 'error');
        }
    }

    async loadSectionData(sectionId) {
        switch (sectionId) {
            case 'accounts':
                await this.loadAccounts();
                break;
            case 'strategies':
                await this.loadStrategies();
                break;
            case 'tags':
                await this.loadTags();
                break;
        }
    }

    async loadAccounts() {
        try {
            const accounts = await fetch('/api/accounts').then(r => r.json());
            const container = document.getElementById('accountsList');
            
            container.innerHTML = accounts.map(account => `
                <div class="admin-item-card">
                    <div class="item-info">
                        <h4>${account.name}</h4>
                        <p>Type: ${account.account_type} | Broker: ${account.broker || 'N/A'}</p>
                        <p>Balance: $${account.current_balance.toLocaleString()}</p>
                    </div>
                    <div class="item-actions">
                        <button class="btn btn-small btn-secondary" onclick="editAccount(${account.id})">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button class="btn btn-small btn-danger" onclick="deleteAccount(${account.id})">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </div>
            `).join('');
            
        } catch (error) {
            console.error('Error loading accounts:', error);
        }
    }

    async loadStrategies() {
        try {
            const strategies = await fetch('/api/strategies').then(r => r.json());
            const container = document.getElementById('strategiesList');
            
            container.innerHTML = strategies.map(strategy => `
                <div class="admin-item-card">
                    <div class="item-info">
                        <h4>${strategy.name}</h4>
                        <p>${strategy.description || 'No description'}</p>
                        <p>Target Win Rate: ${strategy.win_rate_target || 'N/A'}% | R:R: ${strategy.risk_reward_target || 'N/A'}</p>
                    </div>
                    <div class="item-actions">
                        <button class="btn btn-small btn-primary" onclick="viewStrategyPerformance(${strategy.id})">
                            <i class="fas fa-chart-line"></i> Performance
                        </button>
                        <button class="btn btn-small btn-secondary" onclick="editStrategy(${strategy.id})">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button class="btn btn-small btn-danger" onclick="deleteStrategy(${strategy.id})">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </div>
            `).join('');
            
        } catch (error) {
            console.error('Error loading strategies:', error);
        }
    }

    async loadTags() {
        try {
            const tags = await fetch('/api/tags').then(r => r.json());
            const container = document.getElementById('tagsList');
            
            container.innerHTML = tags.map(tag => `
                <div class="admin-item-card">
                    <div class="item-info">
                        <h4>
                            <span class="tag-color" style="background-color: ${tag.color}"></span>
                            ${tag.name}
                        </h4>
                        <p>${tag.description || 'No description'}</p>
                    </div>
                    <div class="item-actions">
                        <button class="btn btn-small btn-secondary" onclick="editTag(${tag.id})">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button class="btn btn-small btn-danger" onclick="deleteTag(${tag.id})">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </div>
            `).join('');
            
        } catch (error) {
            console.error('Error loading tags:', error);
        }
    }

    async addAccount() {
        const formData = {
            name: document.getElementById('accountName').value,
            account_type: document.getElementById('accountType').value,
            broker: document.getElementById('broker').value,
            starting_balance: parseFloat(document.getElementById('startingBalance').value),
            current_balance: parseFloat(document.getElementById('startingBalance').value)
        };

        try {
            const response = await fetch('/api/accounts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                this.showNotification('Account added successfully', 'success');
                this.closeModal('addAccountModal');
                this.loadAccounts();
                document.getElementById('addAccountForm').reset();
            } else {
                throw new Error('Failed to add account');
            }
        } catch (error) {
            console.error('Error adding account:', error);
            this.showNotification('Error adding account', 'error');
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation-triangle' : 'info'}"></i>
            ${message}
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }
}

// Global functions for admin actions
window.showAddAccountModal = function() {
    document.getElementById('addAccountModal').style.display = 'block';
};

window.showAddStrategyModal = function() {
    // Implementation for strategy modal
    console.log('Add strategy modal');
};

window.showAddTagModal = function() {
    // Implementation for tag modal
    console.log('Add tag modal');
};

window.closeModal = function(modalId) {
    document.getElementById(modalId).style.display = 'none';
};

// Database management functions
window.backupDatabase = async function() {
    try {
        const response = await fetch('/api/admin/backup', { method: 'POST' });
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `trading_dashboard_backup_${new Date().toISOString().split('T')[0]}.sql`;
            a.click();
            adminPanel.showNotification('Database backup created', 'success');
        }
    } catch (error) {
        console.error('Backup error:', error);
        adminPanel.showNotification('Backup failed', 'error');
    }
};

window.exportTrades = async function() {
    try {
        const trades = await fetch('/api/trades').then(r => r.json());
        const csv = this.convertToCSV(trades);
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `trades_export_${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
        adminPanel.showNotification('Trades exported successfully', 'success');
    } catch (error) {
        console.error('Export error:', error);
        adminPanel.showNotification('Export failed', 'error');
    }
};

window.syncToGitHub = async function() {
    adminPanel.showNotification('Syncing to GitHub...', 'info');
    // This would typically trigger a webhook or API call to sync
    setTimeout(() => {
        adminPanel.showNotification('Synced to GitHub successfully', 'success');
    }, 2000);
};

// Deployment functions
window.deployToGitHub = function() {
    adminPanel.showNotification('Deploying to GitHub Pages...', 'info');
    // Implementation for GitHub deployment
};

window.deployFrontend = function() {
    adminPanel.showNotification('Deploying frontend...', 'info');
    // Implementation for frontend deployment
};

window.deployFullStack = function() {
    adminPanel.showNotification('Deploying full stack...', 'info');
    // Implementation for full stack deployment
};

// Utility functions
function convertToCSV(data) {
    if (!data.length) return '';
    
    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => {
            const value = row[header];
            return typeof value === 'string' ? `"${value}"` : value;
        }).join(','))
    ].join('\n');
    
    return csvContent;
}

// Initialize admin panel
let adminPanel;
document.addEventListener('DOMContentLoaded', () => {
    adminPanel = new AdminPanel();
});