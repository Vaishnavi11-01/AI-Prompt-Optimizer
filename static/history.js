// DOM Elements
const searchInput = document.getElementById('search-input');
const historyList = document.getElementById('history-list');
const filterButtons = document.querySelectorAll('.filter-btn');
const exportBtn = document.getElementById('export-btn');
const darkModeToggle = document.getElementById('dark-mode-toggle');

let allHistory = [];
let currentFilter = 'all';

// Load dark mode preference from Local Storage
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    if (darkModeToggle) {
        darkModeToggle.textContent = '☀️';
    }
}

// Event Listeners
searchInput.addEventListener('input', handleSearch);
filterButtons.forEach(btn => {
    btn.addEventListener('click', handleFilter);
});

if (exportBtn) {
    exportBtn.addEventListener('click', exportToJSON);
}

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

// Load history on page load
loadHistory();

async function loadHistory() {
    try {
        const response = await fetch('/history');
        const data = await response.json();
        
        if (data.status === 'success') {
            allHistory = data.history;
            displayHistory(allHistory);
        } else {
            historyList.innerHTML = '<p class="empty-state">Failed to load history</p>';
        }
    } catch (error) {
        console.error('Error loading history:', error);
        historyList.innerHTML = '<p class="empty-state">Failed to load history</p>';
    }
}

function displayHistory(history) {
    historyList.innerHTML = '';
    
    if (history.length === 0) {
        historyList.innerHTML = '<p class="empty-state">No prompts found</p>';
        return;
    }
    
    history.forEach(item => {
        const historyItem = createHistoryItem(item);
        historyList.appendChild(historyItem);
    });
}

function createHistoryItem(item) {
    const div = document.createElement('div');
    div.className = 'history-item';
    div.dataset.id = item.id;
    
    const date = new Date(item.created_at);
    const formattedDate = formatDate(date);
    
    div.innerHTML = `
        <div class="history-item-header">
            <div class="history-item-title">
                <span class="category-badge">${item.category}</span>
                <span class="score-badge">Score: ${Math.round(item.score)}</span>
            </div>
            <div class="history-item-meta">
                <span>${formattedDate}</span>
                <span>${item.model_used}</span>
            </div>
        </div>
        <div class="history-item-content">
            <div class="history-prompt">
                <strong>Original:</strong> ${truncateText(item.original_prompt, 100)}
            </div>
            <div class="history-optimized">
                <strong>Optimized:</strong> ${truncateText(item.optimized_prompt, 100)}
            </div>
        </div>
        <div class="history-item-actions">
            <button class="action-btn" onclick="copyOriginal(${item.id})">Copy Original</button>
            <button class="action-btn" onclick="copyOptimized(${item.id})">Copy Optimized</button>
            <button class="action-btn" onclick="reusePrompt(${item.id})">Reuse</button>
            <button class="action-btn delete" onclick="deletePrompt(${item.id})">Delete</button>
        </div>
    `;
    
    return div;
}

function handleSearch(e) {
    const searchTerm = e.target.value.toLowerCase();
    const filtered = allHistory.filter(item => 
        item.original_prompt.toLowerCase().includes(searchTerm) ||
        item.optimized_prompt.toLowerCase().includes(searchTerm) ||
        item.category.toLowerCase().includes(searchTerm)
    );
    
    applyFilter(filtered);
}

function handleFilter(e) {
    // Update active button
    filterButtons.forEach(btn => btn.classList.remove('active'));
    e.target.classList.add('active');
    
    currentFilter = e.target.dataset.filter;
    applyFilter(allHistory);
}

function applyFilter(history) {
    let filtered = history;
    
    if (currentFilter === 'today') {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        filtered = history.filter(item => new Date(item.created_at) >= today);
    } else if (currentFilter === 'yesterday') {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        filtered = history.filter(item => {
            const date = new Date(item.created_at);
            return date >= yesterday && date < today;
        });
    } else if (currentFilter === 'week') {
        const weekAgo = new Date();
        weekAgo.setDate(weekAgo.getDate() - 7);
        filtered = history.filter(item => new Date(item.created_at) >= weekAgo);
    }
    
    displayHistory(filtered);
}

async function copyOriginal(id) {
    const item = allHistory.find(h => h.id === id);
    if (item) {
        await navigator.clipboard.writeText(item.original_prompt);
        alert('Original prompt copied to clipboard');
    }
}

async function copyOptimized(id) {
    const item = allHistory.find(h => h.id === id);
    if (item) {
        await navigator.clipboard.writeText(item.optimized_prompt);
        alert('Optimized prompt copied to clipboard');
    }
}

function reusePrompt(id) {
    const item = allHistory.find(h => h.id === id);
    if (item) {
        localStorage.setItem('promptToReuse', item.original_prompt);
        window.location.href = '/';
    }
}

async function deletePrompt(id) {
    if (!confirm('Are you sure you want to delete this prompt?')) {
        return;
    }
    
    try {
        const response = await fetch(`/history/${id}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        
        if (data.status === 'success') {
            allHistory = allHistory.filter(h => h.id !== id);
            applyFilter(allHistory);
        } else {
            alert('Failed to delete prompt');
        }
    } catch (error) {
        console.error('Error deleting prompt:', error);
        alert('Failed to delete prompt');
    }
}

function formatDate(date) {
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)} minutes ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)} hours ago`;
    if (diff < 604800000) return `${Math.floor(diff / 86400000)} days ago`;
    
    return date.toLocaleDateString();
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

async function exportToJSON() {
    try {
        const response = await fetch('/export/json');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'prompt_history.json';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        console.error('Error exporting JSON:', error);
        alert('Failed to export JSON');
    }
}

// Check for reused prompt on page load
window.addEventListener('load', () => {
    const promptToReuse = localStorage.getItem('promptToReuse');
    if (promptToReuse) {
        localStorage.removeItem('promptToReuse');
        // If on home page, fill the input
        if (window.location.pathname === '/') {
            const promptInput = document.getElementById('prompt-input');
            if (promptInput) {
                promptInput.value = promptToReuse;
            }
        }
    }
});
