// Trade Form Component - Handles trade creation and editing
class TradeForm {
    constructor() {
        this.modal = document.getElementById('tradeModal');
        this.form = document.getElementById('tradeForm');
        this.isEditing = false;
        this.editingTradeId = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupConfluenceSliders();
    }

    setupEventListeners() {
        // Open modal button
        document.getElementById('newTradeBtn').addEventListener('click', () => {
            this.openModal();
        });

        // Close modal buttons
        document.getElementById('closeModal').addEventListener('click', () => {
            this.closeModal();
        });

        document.getElementById('cancelBtn').addEventListener('click', () => {
            this.closeModal();
        });

        // Form submission
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });

        // Close modal when clicking outside
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });

        // Listen for edit trade events
        document.addEventListener('editTrade', (e) => {
            this.openModal(e.detail.trade);
        });
    }

    setupConfluenceSliders() {
        const sliders = ['weeklyTf', 'dailyTf', 'h4Tf', 'h1Tf', 'lowerTf'];
        
        sliders.forEach(sliderId => {
            const slider = document.getElementById(sliderId);
            const valueSpan = document.getElementById(sliderId.replace('Tf', 'Value'));
            
            slider.addEventListener('input', () => {
                valueSpan.textContent = slider.value;
                this.updateTotalConfluence();
            });
        });
    }

    updateTotalConfluence() {
        const weekly = parseInt(document.getElementById('weeklyTf').value);
        const daily = parseInt(document.getElementById('dailyTf').value);
        const h4 = parseInt(document.getElementById('h4Tf').value);
        const h1 = parseInt(document.getElementById('h1Tf').value);
        const lower = parseInt(document.getElementById('lowerTf').value);
        
        const total = (weekly + daily + h4 + h1 + lower) / 5;
        document.getElementById('totalConfluence').textContent = `${total.toFixed(1)}%`;
    }

    openModal(trade = null) {
        this.isEditing = !!trade;
        this.editingTradeId = trade ? trade.id : null;
        
        // Update modal title and button text
        document.getElementById('modalTitle').textContent = this.isEditing ? 'Edit Trade' : 'New Trade';
        document.getElementById('submitBtn').textContent = this.isEditing ? 'Update Trade' : 'Create Trade';
        
        if (this.isEditing) {
            this.populateForm(trade);
        } else {
            this.resetForm();
        }
        
        this.modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        this.modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        this.resetForm();
    }

    populateForm(trade) {
        document.getElementById('symbol').value = trade.symbol;
        document.getElementById('direction').value = trade.direction;
        document.getElementById('entryPrice').value = trade.entry_price;
        document.getElementById('exitPrice').value = trade.exit_price || '';
        document.getElementById('lotSize').value = trade.lot_size;
        document.getElementById('riskReward').value = trade.risk_reward || '';
        document.getElementById('notes').value = trade.notes || '';
        
        // Set confluence sliders
        document.getElementById('weeklyTf').value = trade.weekly_tf;
        document.getElementById('dailyTf').value = trade.daily_tf;
        document.getElementById('h4Tf').value = trade.h4_tf;
        document.getElementById('h1Tf').value = trade.h1_tf;
        document.getElementById('lowerTf').value = trade.lower_tf;
        
        // Update slider displays
        document.getElementById('weeklyValue').textContent = trade.weekly_tf;
        document.getElementById('dailyValue').textContent = trade.daily_tf;
        document.getElementById('h4Value').textContent = trade.h4_tf;
        document.getElementById('h1Value').textContent = trade.h1_tf;
        document.getElementById('lowerValue').textContent = trade.lower_tf;
        
        this.updateTotalConfluence();
    }

    resetForm() {
        this.form.reset();
        this.isEditing = false;
        this.editingTradeId = null;
        
        // Reset slider displays
        const sliders = ['weeklyValue', 'dailyValue', 'h4Value', 'h1Value', 'lowerValue'];
        sliders.forEach(id => {
            document.getElementById(id).textContent = '0';
        });
        
        document.getElementById('totalConfluence').textContent = '0%';
    }

    async handleSubmit() {
        try {
            const formData = new FormData(this.form);
            const tradeData = {};
            
            // Convert form data to object
            for (let [key, value] of formData.entries()) {
                if (value !== '') {
                    // Convert numeric fields
                    if (['entry_price', 'exit_price', 'lot_size', 'risk_reward'].includes(key)) {
                        tradeData[key] = parseFloat(value);
                    } else if (['weekly_tf', 'daily_tf', 'h4_tf', 'h1_tf', 'lower_tf'].includes(key)) {
                        tradeData[key] = parseInt(value);
                    } else {
                        tradeData[key] = value;
                    }
                }
            }

            let result;
            if (this.isEditing) {
                result = await api.updateTrade(this.editingTradeId, tradeData);
            } else {
                result = await api.createTrade(tradeData);
            }

            this.closeModal();
            
            // Dispatch event to refresh trades table and dashboard
            document.dispatchEvent(new CustomEvent('tradesUpdated'));
            
            this.showSuccess(this.isEditing ? 'Trade updated successfully!' : 'Trade created successfully!');
            
        } catch (error) {
            console.error('Failed to save trade:', error);
            this.showError('Failed to save trade. Please try again.');
        }
    }

    showSuccess(message) {
        // Simple success display - could be enhanced with a proper notification system
        console.log(message);
        // You could implement a toast notification here
    }

    showError(message) {
        // Simple error display - could be enhanced with a proper notification system
        console.error(message);
        alert(message);
    }
}