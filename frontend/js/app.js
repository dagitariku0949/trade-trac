// Main App JavaScript - Handles landing page and navigation

document.addEventListener('DOMContentLoaded', () => {
    // Get elements
    const landingPage = document.getElementById('landingPage');
    const mainDashboard = document.getElementById('mainDashboard');
    const enterDashboardBtn = document.getElementById('enterDashboard');
    const leapBtn = document.getElementById('leapBtn');

    // Enter Dashboard button
    if (enterDashboardBtn) {
        enterDashboardBtn.addEventListener('click', () => {
            landingPage.style.display = 'none';
            mainDashboard.style.display = 'block';
            
            // Trigger dashboard data load
            const event = new CustomEvent('dashboardEntered');
            document.dispatchEvent(event);
        });
    }

    // LEAP button - scroll to top or refresh
    if (leapBtn) {
        leapBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            
            // Optional: Refresh dashboard data
            const event = new CustomEvent('tradesUpdated');
            document.dispatchEvent(event);
        });
    }

    // Feature cards animation on hover
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });

    // Learning cards animation
    const learningCards = document.querySelectorAll('.learning-resource-card');
    learningCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });

    console.log('Trading Dashboard App Initialized');
});
