/**
 * Authentication System for Trading Dashboard
 */

class AuthSystem {
    constructor() {
        this.init();
    }
    
    init() {
        // Check authentication on page load
        this.checkAuth();
        
        // Add logout functionality
        this.addLogoutButton();
    }
    
    checkAuth() {
        const isAuthenticated = localStorage.getItem('tradingDashboardAuth') === 'authenticated';
        const currentPage = window.location.pathname;
        
        // If not authenticated and not on login page, redirect to login
        if (!isAuthenticated && !currentPage.includes('login.html')) {
            window.location.href = 'login.html';
            return false;
        }
        
        // If authenticated and on login page, redirect to dashboard
        if (isAuthenticated && currentPage.includes('login.html')) {
            window.location.href = 'index.html';
            return false;
        }
        
        return isAuthenticated;
    }
    
    addLogoutButton() {
        // Add logout button to header if authenticated
        if (localStorage.getItem('tradingDashboardAuth') === 'authenticated') {
            const header = document.querySelector('.header-content');
            if (header) {
                const username = localStorage.getItem('tradingDashboardUser') || 'User';
                
                const userInfo = document.createElement('div');
                userInfo.className = 'user-info';
                userInfo.innerHTML = `
                    <span class="welcome-text">Welcome, ${username}</span>
                    <button class="btn btn-secondary logout-btn" onclick="authSystem.logout()">
                        <i class="fas fa-sign-out-alt"></i> Logout
                    </button>
                `;
                
                header.appendChild(userInfo);
                
                // Add CSS for user info
                const style = document.createElement('style');
                style.textContent = `
                    .user-info {
                        display: flex;
                        align-items: center;
                        gap: 15px;
                        margin-left: auto;
                    }
                    
                    .welcome-text {
                        color: #fff;
                        font-weight: 500;
                    }
                    
                    .logout-btn {
                        padding: 8px 16px !important;
                        font-size: 14px !important;
                    }
                    
                    .header-content {
                        display: flex;
                        align-items: center;
                        width: 100%;
                    }
                `;
                document.head.appendChild(style);
            }
        }
    }
    
    logout() {
        // Clear authentication
        localStorage.removeItem('tradingDashboardAuth');
        localStorage.removeItem('tradingDashboardUser');
        
        // Redirect to login
        window.location.href = 'login.html';
    }
    
    isAuthenticated() {
        return localStorage.getItem('tradingDashboardAuth') === 'authenticated';
    }
    
    getUser() {
        return localStorage.getItem('tradingDashboardUser');
    }
}

// Initialize authentication system
const authSystem = new AuthSystem();

// Make it globally available
window.authSystem = authSystem;