// Enhanced Monthly Calendar Component
let currentCalendarDate = new Date();
let selectedDay = null;

export function renderMonthlyCalendar(monthlyData) {
    const container = document.getElementById('monthly-calendar');
    if (!container) return;

    const { year, month, daily_data } = monthlyData;
    
    // Create a map for quick lookup
    const dataMap = {};
    daily_data.forEach(day => {
        dataMap[day.date] = day;
    });

    // Get days in month
    const daysInMonth = new Date(year, month, 0).getDate();
    const firstDay = new Date(year, month - 1, 1).getDay();
    
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December'];

    let calendarHTML = `
        <div class="calendar-header">
            <div class="calendar-nav">
                <button class="btn-calendar-nav" id="prevMonth" title="Previous Month">
                    <i class="fas fa-chevron-left"></i>
                </button>
                <div class="calendar-title">
                    <h3>${monthNames[month - 1]} ${year}</h3>
                    <div class="calendar-subtitle">Trading Performance Overview</div>
                </div>
                <button class="btn-calendar-nav" id="nextMonth" title="Next Month">
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
            <div class="calendar-legend">
                <div class="legend-item">
                    <div class="legend-color profit"></div>
                    <span>Profit Days</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color loss"></div>
                    <span>Loss Days</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color breakeven"></div>
                    <span>Breakeven</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color no-trades"></div>
                    <span>No Trades</span>
                </div>
            </div>
        </div>
        <div class="calendar-grid">
            <div class="calendar-day-header">Sun</div>
            <div class="calendar-day-header">Mon</div>
            <div class="calendar-day-header">Tue</div>
            <div class="calendar-day-header">Wed</div>
            <div class="calendar-day-header">Thu</div>
            <div class="calendar-day-header">Fri</div>
            <div class="calendar-day-header">Sat</div>
    `;

    // Empty cells for days before month starts
    for (let i = 0; i < firstDay; i++) {
        calendarHTML += '<div class="calendar-day empty"></div>';
    }

    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const dayData = dataMap[dateStr];
        const isToday = isDateToday(year, month - 1, day);
        
        let className = 'calendar-day interactive';
        let content = `<div class="day-number ${isToday ? 'today' : ''}">${day}</div>`;
        
        if (dayData) {
            const pnl = dayData.pnl;
            const winRate = dayData.winning_trades ? (dayData.winning_trades / dayData.trades * 100) : 0;
            
            if (pnl > 0) {
                className += ' profit';
                const intensity = Math.min(Math.abs(pnl) / 1000, 1);
                content += `
                    <div class="day-pnl profit" style="opacity: ${0.4 + intensity * 0.6}">
                        +$${formatNumber(pnl)}
                    </div>
                    <div class="day-details">
                        <div class="day-trades">${dayData.trades} trade${dayData.trades > 1 ? 's' : ''}</div>
                        <div class="day-winrate">${winRate.toFixed(0)}% WR</div>
                    </div>
                `;
            } else if (pnl < 0) {
                className += ' loss';
                const intensity = Math.min(Math.abs(pnl) / 1000, 1);
                content += `
                    <div class="day-pnl loss" style="opacity: ${0.4 + intensity * 0.6}">
                        -$${formatNumber(Math.abs(pnl))}
                    </div>
                    <div class="day-details">
                        <div class="day-trades">${dayData.trades} trade${dayData.trades > 1 ? 's' : ''}</div>
                        <div class="day-winrate">${winRate.toFixed(0)}% WR</div>
                    </div>
                `;
            } else {
                className += ' breakeven';
                content += `
                    <div class="day-pnl breakeven">$0</div>
                    <div class="day-details">
                        <div class="day-trades">${dayData.trades} trade${dayData.trades > 1 ? 's' : ''}</div>
                        <div class="day-winrate">${winRate.toFixed(0)}% WR</div>
                    </div>
                `;
            }
            
            // Add performance indicator
            if (dayData.trades > 0) {
                const performanceClass = pnl > 0 ? 'excellent' : pnl < 0 ? 'poor' : 'neutral';
                content += `<div class="performance-indicator ${performanceClass}"></div>`;
            }
        } else {
            className += ' no-trades';
            content += '<div class="day-empty">No trades</div>';
        }
        
        calendarHTML += `
            <div class="${className}" 
                 data-date="${dateStr}" 
                 data-day-data='${dayData ? JSON.stringify(dayData) : '{}'}' 
                 onclick="selectCalendarDay('${dateStr}', this)">
                ${content}
            </div>
        `;
    }

    calendarHTML += '</div>';
    
    // Add day detail panel
    calendarHTML += `
        <div class="day-detail-panel" id="dayDetailPanel" style="display: none;">
            <div class="detail-header">
                <h4 id="selectedDate">Select a day to view details</h4>
                <button class="btn-close-detail" onclick="closeDayDetail()">×</button>
            </div>
            <div class="detail-content" id="dayDetailContent">
                <!-- Day details will be populated here -->
            </div>
        </div>
    `;
    
    container.innerHTML = calendarHTML;
    
    // Add event listeners for navigation
    setupCalendarNavigation();
}

function isDateToday(year, month, day) {
    const today = new Date();
    return today.getFullYear() === year && 
           today.getMonth() === month && 
           today.getDate() === day;
}

function formatNumber(num) {
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k';
    }
    return num.toFixed(0);
}

function setupCalendarNavigation() {
    const prevBtn = document.getElementById('prevMonth');
    const nextBtn = document.getElementById('nextMonth');
    
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            currentCalendarDate.setMonth(currentCalendarDate.getMonth() - 1);
            // Trigger calendar refresh - you'll need to implement this based on your app structure
            console.log('Navigate to previous month:', currentCalendarDate);
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            currentCalendarDate.setMonth(currentCalendarDate.getMonth() + 1);
            // Trigger calendar refresh - you'll need to implement this based on your app structure
            console.log('Navigate to next month:', currentCalendarDate);
        });
    }
}

// Global function for day selection
window.selectCalendarDay = function(dateStr, element) {
    // Remove previous selection
    document.querySelectorAll('.calendar-day.selected').forEach(day => {
        day.classList.remove('selected');
    });
    
    // Add selection to current day
    element.classList.add('selected');
    selectedDay = dateStr;
    
    // Get day data
    const dayData = JSON.parse(element.getAttribute('data-day-data') || '{}');
    
    // Show day details
    showDayDetails(dateStr, dayData);
};

function showDayDetails(dateStr, dayData) {
    const panel = document.getElementById('dayDetailPanel');
    const dateHeader = document.getElementById('selectedDate');
    const content = document.getElementById('dayDetailContent');
    
    if (!panel || !dateHeader || !content) return;
    
    // Format date
    const date = new Date(dateStr);
    const formattedDate = date.toLocaleDateString('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    
    dateHeader.textContent = formattedDate;
    
    if (Object.keys(dayData).length === 0) {
        content.innerHTML = `
            <div class="no-data">
                <i class="fas fa-calendar-times"></i>
                <p>No trading activity on this day</p>
                <button class="btn btn-primary btn-small" onclick="addTradeForDate('${dateStr}')">
                    Add Trade
                </button>
            </div>
        `;
    } else {
        const winRate = dayData.winning_trades ? (dayData.winning_trades / dayData.trades * 100).toFixed(1) : '0.0';
        const avgTradeSize = dayData.total_volume ? (dayData.total_volume / dayData.trades) : 0;
        
        content.innerHTML = `
            <div class="day-stats-grid">
                <div class="day-stat">
                    <div class="stat-icon profit">
                        <i class="fas fa-dollar-sign"></i>
                    </div>
                    <div class="stat-info">
                        <div class="stat-label">P&L</div>
                        <div class="stat-value ${dayData.pnl >= 0 ? 'profit' : 'loss'}">
                            ${dayData.pnl >= 0 ? '+' : ''}$${dayData.pnl.toFixed(2)}
                        </div>
                    </div>
                </div>
                
                <div class="day-stat">
                    <div class="stat-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <div class="stat-info">
                        <div class="stat-label">Trades</div>
                        <div class="stat-value">${dayData.trades}</div>
                    </div>
                </div>
                
                <div class="day-stat">
                    <div class="stat-icon">
                        <i class="fas fa-percentage"></i>
                    </div>
                    <div class="stat-info">
                        <div class="stat-label">Win Rate</div>
                        <div class="stat-value">${winRate}%</div>
                    </div>
                </div>
                
                <div class="day-stat">
                    <div class="stat-icon">
                        <i class="fas fa-coins"></i>
                    </div>
                    <div class="stat-info">
                        <div class="stat-label">Avg Size</div>
                        <div class="stat-value">$${avgTradeSize.toFixed(0)}</div>
                    </div>
                </div>
            </div>
            
            <div class="day-actions">
                <button class="btn btn-primary btn-small" onclick="viewDayTrades('${dateStr}')">
                    <i class="fas fa-list"></i> View Trades
                </button>
                <button class="btn btn-secondary btn-small" onclick="addTradeForDate('${dateStr}')">
                    <i class="fas fa-plus"></i> Add Trade
                </button>
            </div>
        `;
    }
    
    panel.style.display = 'block';
    panel.classList.add('show');
}

window.closeDayDetail = function() {
    const panel = document.getElementById('dayDetailPanel');
    if (panel) {
        panel.classList.remove('show');
        setTimeout(() => {
            panel.style.display = 'none';
        }, 300);
    }
    
    // Remove selection
    document.querySelectorAll('.calendar-day.selected').forEach(day => {
        day.classList.remove('selected');
    });
    selectedDay = null;
};

window.addTradeForDate = function(dateStr) {
    // This should integrate with your existing trade form
    console.log('Add trade for date:', dateStr);
    // You can trigger your existing trade modal here and pre-fill the date
};

window.viewDayTrades = function(dateStr) {
    // This should filter and show trades for the specific day
    console.log('View trades for date:', dateStr);
    // You can integrate this with your existing trades table filtering
};

export function renderMonthlyStats(monthlyData) {
    const container = document.getElementById('monthly-stats');
    if (!container) return;

    const {
        total_pnl,
        total_trades,
        trading_days,
        winning_days,
        losing_days,
        win_rate,
        best_day,
        worst_day,
        average_daily_pnl
    } = monthlyData;

    container.innerHTML = `
        <div class="monthly-stats-grid">
            <div class="stat-card highlight">
                <div class="stat-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <h4>Monthly P&L</h4>
                <div class="stat-value ${total_pnl >= 0 ? 'profit' : 'loss'}">
                    ${total_pnl >= 0 ? '+' : ''}$${total_pnl.toFixed(2)}
                </div>
                <div class="stat-trend ${total_pnl >= 0 ? 'up' : 'down'}">
                    <i class="fas fa-arrow-${total_pnl >= 0 ? 'up' : 'down'}"></i>
                    ${Math.abs(total_pnl).toFixed(2)}
                </div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-exchange-alt"></i>
                </div>
                <h4>Total Trades</h4>
                <div class="stat-value">${total_trades}</div>
                <div class="stat-detail">Executed this month</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-calendar-check"></i>
                </div>
                <h4>Trading Days</h4>
                <div class="stat-value">${trading_days}</div>
                <div class="stat-detail">${winning_days}W / ${losing_days}L</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-percentage"></i>
                </div>
                <h4>Daily Win Rate</h4>
                <div class="stat-value">${win_rate}%</div>
                <div class="stat-detail">Success rate</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-calculator"></i>
                </div>
                <h4>Avg Daily P&L</h4>
                <div class="stat-value ${average_daily_pnl >= 0 ? 'profit' : 'loss'}">
                    ${average_daily_pnl >= 0 ? '+' : ''}$${average_daily_pnl.toFixed(2)}
                </div>
                <div class="stat-detail">Per trading day</div>
            </div>
            
            <div class="stat-card best-day">
                <div class="stat-icon profit">
                    <i class="fas fa-trophy"></i>
                </div>
                <h4>Best Day</h4>
                <div class="stat-value profit">+$${best_day.pnl.toFixed(2)}</div>
                <div class="stat-detail">${best_day.date || 'N/A'}</div>
            </div>
            
            <div class="stat-card worst-day">
                <div class="stat-icon loss">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h4>Worst Day</h4>
                <div class="stat-value loss">$${worst_day.pnl.toFixed(2)}</div>
                <div class="stat-detail">${worst_day.date || 'N/A'}</div>
            </div>
        </div>
    `;
}