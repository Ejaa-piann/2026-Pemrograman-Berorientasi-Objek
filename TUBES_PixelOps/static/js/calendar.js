document.addEventListener('DOMContentLoaded', () => {
    const calendarWidget = document.getElementById('calendar');
    
    if (window.__deadlineProjects && calendarWidget) {
        let projects = window.__deadlineProjects;
        
        let currentDate = new Date();
        let currentMonth = currentDate.getMonth();
        let currentYear = currentDate.getFullYear();
        
        // Helper to get deadlines for a specific date (YYYY-MM-DD)
        const getDeadlinesForDate = (year, month, date) => {
            const dateString = `${year}-${String(month + 1).padStart(2, '0')}-${String(date).padStart(2, '0')}`;
            return projects.filter(p => p.deadline === dateString);
        };

        const renderCalendar = () => {
            const firstDayIndex = new Date(currentYear, currentMonth, 1).getDay(); // 0 is Sun
            const lastDate = new Date(currentYear, currentMonth + 1, 0).getDate();
            const prevLastDate = new Date(currentYear, currentMonth, 0).getDate();
            
            const monthNames = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"];
            
            let html = `
                <div class="mini-calendar" style="background: var(--bg-surface); border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid var(--border);">
                    <div class="calendar-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <button id="prevMonth" class="btn btn-secondary btn-sm"><i class="fas fa-chevron-left"></i></button>
                        <h3 id="monthTitle" style="margin: 0; font-size: 1.1rem; color: var(--text); cursor: pointer; transition: color 0.2s;" title="Tampilkan semua deadline bulan ini">${monthNames[currentMonth]} ${currentYear}</h3>
                        <button id="nextMonth" class="btn btn-secondary btn-sm"><i class="fas fa-chevron-right"></i></button>
                    </div>
                    <div class="calendar-weekdays" style="display: grid; grid-template-columns: repeat(7, 1fr); text-align: center; font-weight: 600; font-size: 0.85rem; color: var(--text-muted); margin-bottom: 10px;">
                        <div>Min</div><div>Sen</div><div>Sel</div><div>Rab</div><div>Kam</div><div>Jum</div><div>Sab</div>
                    </div>
                    <div class="calendar-days" style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px;">
            `;
            
            // Adjust to start on Sunday (0)
            let dayCount = 1;
            let nextMonthDayCount = 1;
            let prevMonthDayCount = prevLastDate - firstDayIndex + 1;
            
            for (let i = 0; i < 42; i++) {
                if (i < firstDayIndex) {
                    // Prev month days
                    html += `<div class="calendar-day prev-month" style="padding: 8px; text-align: center; color: var(--text-muted-alt); font-size: 0.9rem;">${prevMonthDayCount}</div>`;
                    prevMonthDayCount++;
                } else if (dayCount <= lastDate) {
                    // Current month days
                    const deadlines = getDeadlinesForDate(currentYear, currentMonth, dayCount);
                    
                    const isToday = new Date().getDate() === dayCount && new Date().getMonth() === currentMonth && new Date().getFullYear() === currentYear;
                    
                    let bgStyle = 'background: transparent; color: var(--text);';
                    let badgeHtml = '';
                    
                    if (isToday) {
                        bgStyle = 'background: rgba(59, 130, 246, 0.2); color: #60A5FA; font-weight: bold; border: 1px solid #3B82F6;';
                    }
                    
                    let colorData = '';
                    if (deadlines.length > 0) {
                        const targetDate = new Date(currentYear, currentMonth, dayCount);
                        const today = new Date();
                        today.setHours(0,0,0,0);
                        
                        const diffTime = targetDate - today;
                        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                        
                        let gradient = 'linear-gradient(135deg, #10B981, #34D399)'; // Safe (Green)
                        let shadow = 'rgba(16, 185, 129, 0.3)';
                        let colorIndicator = '#10B981';
                        
                        if (diffDays < 0) {
                            gradient = 'linear-gradient(135deg, #EF4444, #F87171)'; // Overdue (Red)
                            shadow = 'rgba(239, 68, 68, 0.3)';
                            colorIndicator = '#EF4444';
                        } else if (diffDays <= 3) {
                            gradient = 'linear-gradient(135deg, #F59E0B, #FBBF24)'; // Near (Yellow)
                            shadow = 'rgba(245, 158, 11, 0.3)';
                            colorIndicator = '#F59E0B';
                        }
                        
                        bgStyle = `background: ${gradient}; color: white; font-weight: bold; cursor: pointer; box-shadow: 0 4px 10px ${shadow};`;
                        badgeHtml = `<div style="position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%); width: 4px; height: 4px; background: white; border-radius: 50%;"></div>`;
                        colorData = `data-color="${colorIndicator}"`;
                    }
                    
                    const tooltipData = deadlines.length > 0 ? `data-deadlines='${JSON.stringify(deadlines.map(d => d.nama))}'` : '';
                    
                    html += `
                        <div class="calendar-day current-month has-tooltip" ${tooltipData} ${colorData} data-date="${dayCount}" style="position: relative; padding: 8px; text-align: center; border-radius: 8px; font-size: 0.9rem; transition: all 0.2s; ${bgStyle}">
                            ${dayCount}
                            ${badgeHtml}
                        </div>
                    `;
                    dayCount++;
                } else {
                    // Next month days
                    html += `<div class="calendar-day next-month" style="padding: 8px; text-align: center; color: var(--text-muted-alt); font-size: 0.9rem;">${nextMonthDayCount}</div>`;
                    nextMonthDayCount++;
                }
            }
            
            html += `
                    </div>
                </div>
                <div id="calendar-details" style="margin-top: 16px; padding: 16px; background: rgba(30, 41, 59, 0.4); border-radius: 12px; display: none;">
                    <h4 id="calendar-details-title" style="margin-bottom: 12px; font-size: 1rem; color: var(--text);"><i class="fas fa-list-ul" style="margin-right: 8px; color: #8B5CF6;"></i>Deadline Tanggal Ini</h4>
                    <ul id="calendar-details-list" style="list-style: none; padding: 0; margin: 0; font-size: 0.9rem; color: var(--text-muted); display: flex; flex-direction: column; gap: 8px;">
                    </ul>
                </div>
            `;
            
            calendarWidget.innerHTML = html;
            
            // Attach event listeners
            document.getElementById('prevMonth').addEventListener('click', () => {
                currentMonth--;
                if (currentMonth < 0) {
                    currentMonth = 11;
                    currentYear--;
                }
                renderCalendar();
            });
            
            document.getElementById('nextMonth').addEventListener('click', () => {
                currentMonth++;
                if (currentMonth > 11) {
                    currentMonth = 0;
                    currentYear++;
                }
                renderCalendar();
            });
            
            // Tooltip / Details click handler
            const daysWithDeadlines = document.querySelectorAll('.calendar-day.current-month.has-tooltip');
            const detailsBox = document.getElementById('calendar-details');
            const detailsTitle = document.getElementById('calendar-details-title');
            const detailsList = document.getElementById('calendar-details-list');
            
            daysWithDeadlines.forEach(day => {
                const deadlineData = day.getAttribute('data-deadlines');
                if (deadlineData) {
                    day.addEventListener('click', () => {
                        const date = day.getAttribute('data-date');
                        const parsedDeadlines = JSON.parse(deadlineData);
                        const color = day.getAttribute('data-color') || '#8B5CF6';
                        
                        detailsTitle.innerHTML = `<i class="fas fa-list-ul" style="margin-right: 8px; color: ${color};"></i>Deadline ${date} ${monthNames[currentMonth]} ${currentYear}`;
                        
                        let listHtml = '';
                        parsedDeadlines.forEach(nama => {
                            listHtml += `<li style="padding: 8px 12px; background: var(--bg-surface); border-radius: 6px; border-left: 3px solid ${color};">${nama}</li>`;
                        });
                        
                        detailsList.innerHTML = listHtml;
                        detailsBox.style.display = 'block';
                        
                        // Add active state to clicked day
                        document.querySelectorAll('.calendar-day').forEach(d => d.style.transform = 'scale(1)');
                        day.style.transform = 'scale(1.1)';
                    });
                }
            });
            
            // Month title click handler (show all deadlines for the month)
            document.getElementById('monthTitle').addEventListener('click', () => {
                let monthDeadlines = [];
                for (let day = 1; day <= lastDate; day++) {
                    let daily = getDeadlinesForDate(currentYear, currentMonth, day);
                    daily.forEach(d => {
                        monthDeadlines.push({ date: day, nama: d.nama });
                    });
                }
                
                detailsTitle.innerHTML = `<i class="fas fa-list-ul" style="margin-right: 8px; color: #8B5CF6;"></i>Semua Deadline ${monthNames[currentMonth]} ${currentYear}`;
                
                if (monthDeadlines.length === 0) {
                    detailsList.innerHTML = `<li style="padding: 8px 12px; color: var(--text-muted); font-style: italic;">Tidak ada deadline bulan ini.</li>`;
                } else {
                    let listHtml = '';
                    monthDeadlines.forEach(item => {
                        listHtml += `<li style="padding: 8px 12px; background: var(--bg-surface); border-radius: 6px; border-left: 3px solid #8B5CF6; display: flex; justify-content: space-between;">
                            <span>${item.nama}</span>
                            <span style="color: var(--text-muted-alt); font-size: 0.85rem;">Tgl ${item.date}</span>
                        </li>`;
                    });
                    detailsList.innerHTML = listHtml;
                }
                
                detailsBox.style.display = 'block';
                
                // Visual feedback
                document.querySelectorAll('.calendar-day').forEach(d => d.style.transform = 'scale(1)');
                const titleEl = document.getElementById('monthTitle');
                titleEl.style.color = '#8B5CF6';
                setTimeout(() => { titleEl.style.color = 'var(--text)'; }, 300);
            });
        };

        renderCalendar();
    }
});
