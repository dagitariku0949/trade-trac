// Monthly Calendar Component
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
            <button class="btn btn-secondary btn-small" id="prevMonth">← Prev</button>
            <h3>${monthNames[month - 1]} ${year}</h3>
            <button class="btn btn-secondary btn-small" id="nextMonth">Next →</button>
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
        
        let className = 'calendar-day';
        let content = `<div class="day-number">${day}</div>`;
        
        if (dayData) {
            const pnl = dayData.pnl;
            if (pnl > 0) {
                className += ' profit';
                const intensity = Math.min(Math.abs(pnl) / 1000, 1);
                content += `<div class="day-pnl profit" style="opacity: ${0.3 + intensity * 0.7}">+$${pnl.toFixed(0)}</div>`;
            } else if (pnl < 0) {
                className += ' loss';
                const intensity = Math.min(Math.abs(pnl) / 1000, 1);
                content += `<div class="day-pnl loss" style="opacity: ${0.3 + intensity * 0.7}">-$${Math.abs(pnl).toFixed(0)}</div>`;
            } else {
                className += ' breakeven';
                content += `<div class="day-pnl">$0</div>`;
            }
            content += `<div class="day-trades">${dayData.trades} trade${dayData.trades > 1 ? 's' : ''}</div>`;
        }
        
        calendarHTML += `<div class="${className}">${content}</div>`;
    }

    calendarHTML += '</div>';
    container.innerHTML = calendarHTML;
}

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
            <div class="stat-card">
                <h4>Monthly P&L</h4>
                <div class="stat-value ${total_pnl >= 0 ? 'profit' : 'loss'}">
                    ${total_pnl >= 0 ? '+' : ''}$${total_pnl.toFixed(2)}
                </div>
            </div>
            <div class="stat-card">
                <h4>Total Trades</h4>
                <div class="stat-value">${total_trades}</div>
            </div>
            <div class="stat-card">
                <h4>Trading Days</h4>
                <div class="stat-value">${trading_days}</div>
                <div class="stat-detail">${winning_days}W / ${losing_days}L</div>
            </div>
            <div class="stat-card">
                <h4>Daily Win Rate</h4>
                <div class="stat-value">${win_rate}%</div>
            </div>
            <div class="stat-card">
                <h4>Avg Daily P&L</h4>
                <div class="stat-value ${average_daily_pnl >= 0 ? 'profit' : 'loss'}">
                    ${average_daily_pnl >= 0 ? '+' : ''}$${average_daily_pnl.toFixed(2)}
                </div>
            </div>
            <div class="stat-card">
                <h4>Best Day</h4>
                <div class="stat-value profit">+$${best_day.pnl.toFixed(2)}</div>
                <div class="stat-detail">${best_day.date || 'N/A'}</div>
            </div>
            <div class="stat-card">
                <h4>Worst Day</h4>
                <div class="stat-value loss">$${worst_day.pnl.toFixed(2)}</div>
                <div class="stat-detail">${worst_day.date || 'N/A'}</div>
            </div>
        </div>
    `;
}
