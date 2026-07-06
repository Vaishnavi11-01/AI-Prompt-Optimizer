// DOM Elements
const totalPromptsEl = document.getElementById('total-prompts');
const averageScoreEl = document.getElementById('average-score');
const mostUsedCategoryEl = document.getElementById('most-used-category');
const categoryChart = document.getElementById('category-chart');
const usageChart = document.getElementById('usage-chart');
const darkModeToggle = document.getElementById('dark-mode-toggle');

let categoryChartInstance = null;
let usageChartInstance = null;

// Load dark mode preference from Local Storage
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    if (darkModeToggle) {
        darkModeToggle.textContent = '☀️';
    }
}

// Dark mode toggle
if (darkModeToggle) {
    darkModeToggle.addEventListener('click', toggleDarkMode);
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDarkMode = document.body.classList.contains('dark-mode');
    
    // Save preference to Local Storage
    localStorage.setItem('darkMode', isDarkMode);
    
    // Update toggle icon
    darkModeToggle.textContent = isDarkMode ? '☀️' : '🌙';
}

// Load stats on page load
loadStats();

async function loadStats() {
    try {
        const response = await fetch('/stats');
        const data = await response.json();
        
        if (data.status === 'success') {
            displayStats(data);
        } else {
            console.error('Failed to load stats:', data.error);
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function displayStats(data) {
    // Update summary cards
    totalPromptsEl.textContent = data.total_prompts;
    averageScoreEl.textContent = data.average_score;
    mostUsedCategoryEl.textContent = data.most_used_category;
    
    // Render charts
    renderCategoryChart(data.category_distribution);
    renderUsageChart(data.monthly_usage);
}

function renderCategoryChart(distribution) {
    const labels = Object.keys(distribution);
    const values = Object.values(distribution);
    
    // Destroy existing chart if it exists
    if (categoryChartInstance) {
        categoryChartInstance.destroy();
    }
    
    categoryChartInstance = new Chart(categoryChart, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    '#6366f1',
                    '#8b5cf6',
                    '#ec4899',
                    '#f59e0b',
                    '#10b981',
                    '#3b82f6',
                    '#ef4444',
                    '#6b7280'
                ],
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            }
        }
    });
}

function renderUsageChart(usage) {
    const labels = Object.keys(usage);
    const values = Object.values(usage);
    
    // Destroy existing chart if it exists
    if (usageChartInstance) {
        usageChartInstance.destroy();
    }
    
    usageChartInstance = new Chart(usageChart, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Prompts',
                data: values,
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#6366f1',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}
