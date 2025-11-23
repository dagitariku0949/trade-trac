// API Client for Trading Dashboard
class ApiClient {
    constructor() {
        // Use environment variable or default to localhost
        this.baseURL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? 'http://localhost:5000/api'
            : 'https://trade-trac.onrender.com/api';
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            // Handle empty responses (like DELETE)
            if (response.status === 204) {
                return null;
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Trade endpoints
    async getTrades() {
        return this.request('/trades');
    }

    async getTrade(id) {
        return this.request(`/trades/${id}`);
    }

    async createTrade(tradeData) {
        return this.request('/trades', {
            method: 'POST',
            body: JSON.stringify(tradeData)
        });
    }

    async updateTrade(id, tradeData) {
        return this.request(`/trades/${id}`, {
            method: 'PUT',
            body: JSON.stringify(tradeData)
        });
    }

    async closeTrade(id, exitPrice) {
        return this.request(`/trades/${id}/close`, {
            method: 'POST',
            body: JSON.stringify({ exit_price: exitPrice })
        });
    }

    async deleteTrade(id) {
        return this.request(`/trades/${id}`, {
            method: 'DELETE'
        });
    }

    // Statistics endpoints
    async getAccountStats() {
        return this.request('/trades/stats/account');
    }

    async getMetrics() {
        return this.request('/trades/stats/metrics');
    }

    async getDailyStats() {
        return this.request('/trades/stats/daily');
    }
}

// Create global API client instance
const api = new ApiClient();