// DOM Elements
const promptInput = document.getElementById('prompt-input');
const optimizeBtn = document.getElementById('optimize-btn');
const resultsSection = document.getElementById('results-section');
const scoreValue = document.getElementById('score-value');
const scoreLabel = document.getElementById('score-label');
const categoryValue = document.getElementById('category-value');
const suggestionsList = document.getElementById('suggestions-list');
const optimizedPromptText = document.getElementById('optimized-prompt-text');
const copyBtn = document.getElementById('copy-btn');
const pdfBtn = document.getElementById('pdf-btn');

// Score breakdown elements
const lengthScore = document.getElementById('length-score');
const lengthProgress = document.getElementById('length-progress');
const clarityScore = document.getElementById('clarity-score');
const clarityProgress = document.getElementById('clarity-progress');
const specificityScore = document.getElementById('specificity-score');
const specificityProgress = document.getElementById('specificity-progress');
const contextScore = document.getElementById('context-score');
const contextProgress = document.getElementById('context-progress');
const formatScore = document.getElementById('format-score');
const formatProgress = document.getElementById('format-progress');

// Store current optimization data for PDF generation
let currentOptimizationData = null;

// Event Listeners
optimizeBtn.addEventListener('click', optimizePrompt);
copyBtn.addEventListener('click', copyToClipboard);
if (pdfBtn) {
    pdfBtn.addEventListener('click', generatePDF);
}

// Optimize Prompt
async function optimizePrompt() {
    const prompt = promptInput.value.trim();
    
    console.log('Optimize button clicked');
    console.log('Prompt:', prompt);
    
    if (!prompt) {
        alert('Please enter a prompt to optimize');
        return;
    }
    
    // Show loading state
    optimizeBtn.disabled = true;
    optimizeBtn.textContent = 'Optimizing...';
    
    try {
        console.log('Sending request to /optimize');
        const response = await fetch("/optimize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                prompt: prompt
            })
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to optimize prompt');
        }
        
        const data = await response.json();
        console.log('Backend response:', data);
        
        // Display results
        displayResults(data, prompt);
        
        resultsSection.classList.remove('hidden');
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to optimize prompt: ' + error.message);
    } finally {
        // Reset button state
        optimizeBtn.disabled = false;
        optimizeBtn.textContent = 'Optimize';
    }
}

function displayResults(data, prompt) {
    const scores = data.score;
    const category = data.category;
    const suggestions = generateSuggestions(prompt);
    const optimizedText = data.optimized_prompt;
    
    // Store current optimization data for PDF generation
    currentOptimizationData = {
        original_prompt: prompt,
        optimized_prompt: optimizedText,
        score: scores,
        category: category,
        suggestions: suggestions
    };
    
    // Display overall score
    scoreValue.textContent = Math.round(scores.total);
    scoreLabel.textContent = getScoreLabel(scores.total);
    
    // Display category
    categoryValue.textContent = category;
    
    // Display score breakdown
    displayScoreBreakdown(scores);
    
    // Display suggestions
    displaySuggestions(suggestions);
    
    // Display optimized text
    optimizedPromptText.textContent = optimizedText;
}

function displayScoreBreakdown(scores) {
    // Length (max 20)
    lengthScore.textContent = `${scores.length}/20`;
    lengthProgress.style.width = `${(scores.length / 20) * 100}%`;
    
    // Clarity (max 15)
    clarityScore.textContent = `${scores.clarity}/15`;
    clarityProgress.style.width = `${(scores.clarity / 15) * 100}%`;
    
    // Specificity (max 15)
    specificityScore.textContent = `${scores.specificity}/15`;
    specificityProgress.style.width = `${(scores.specificity / 15) * 100}%`;
    
    // Context (max 10)
    contextScore.textContent = `${scores.context}/10`;
    contextProgress.style.width = `${(scores.context / 10) * 100}%`;
    
    // Format (max 10)
    formatScore.textContent = `${scores.format}/10`;
    formatProgress.style.width = `${(scores.format / 10) * 100}%`;
}

function displaySuggestions(suggestions) {
    suggestionsList.innerHTML = '';
    
    if (suggestions.length === 0) {
        suggestionsList.innerHTML = '<li>Your prompt looks good!</li>';
        return;
    }
    
    suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = suggestion;
        suggestionsList.appendChild(li);
    });
}

function getScoreLabel(score) {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    if (score >= 20) return 'Poor';
    return 'Very Poor';
}

function copyToClipboard() {
    const text = optimizedPromptText.textContent;
    navigator.clipboard.writeText(text).then(() => {
        copyBtn.textContent = 'Copied!';
        setTimeout(() => {
            copyBtn.textContent = 'Copy to Clipboard';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy to clipboard');
    });
}

async function generatePDF() {
    if (!currentOptimizationData) {
        alert('No optimization data available. Please optimize a prompt first.');
        return;
    }
    
    pdfBtn.disabled = true;
    pdfBtn.textContent = 'Generating PDF...';
    
    try {
        const response = await fetch('/generate-pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(currentOptimizationData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate PDF');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `prompt_report_${new Date().toISOString().slice(0,10)}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
    } catch (error) {
        console.error('Error generating PDF:', error);
        alert('Failed to generate PDF: ' + error.message);
    } finally {
        pdfBtn.disabled = false;
        pdfBtn.textContent = 'Download PDF Report';
    }
}

// Calculate Score (Mock)
function calculateScore(prompt) {
    if (!prompt || !prompt.trim()) return 0;
    
    let score = 50; // Base score
    
    const length = prompt.length;
    if (length >= 50 && length <= 500) score += 20;
    else if (length > 500) score += 10;
    else if (length > 20) score += 5;
    
    const promptLower = prompt.toLowerCase();
    const clarityKeywords = ['explain', 'describe', 'analyze', 'compare', 'evaluate', 'summarize', 'define'];
    if (clarityKeywords.some(keyword => promptLower.includes(keyword))) score += 10;
    
    const specificityKeywords = ['specifically', 'detail', 'example', 'step', 'include', 'provide'];
    if (specificityKeywords.some(keyword => promptLower.includes(keyword))) score += 10;
    
    if (prompt.includes('?')) score += 5;
    
    return Math.min(Math.max(score, 0), 100);
}

// Categorize Prompt (Mock)
function categorizePrompt(prompt) {
    if (!prompt || !prompt.trim()) return 'General';
    
    const promptLower = prompt.toLowerCase();
    
    const categories = {
        'Creative Writing': ['write', 'story', 'creative', 'narrative', 'fiction', 'poem', 'character'],
        'Code & Programming': ['code', 'programming', 'function', 'algorithm', 'debug', 'python', 'javascript'],
        'Data Analysis': ['analyze', 'data', 'statistics', 'chart', 'graph', 'trend'],
        'Business': ['business', 'marketing', 'strategy', 'sales', 'revenue', 'customer'],
        'Education': ['teach', 'learn', 'explain', 'education', 'tutorial', 'lesson'],
        'Research': ['research', 'paper', 'academic', 'citation', 'reference'],
        'Technical': ['technical', 'documentation', 'manual', 'guide', 'specification'],
        'Communication': ['email', 'message', 'letter', 'communication'],
        'Problem Solving': ['solve', 'problem', 'solution', 'fix', 'resolve'],
    };
    
    for (const [category, keywords] of Object.entries(categories)) {
        if (keywords.some(keyword => promptLower.includes(keyword))) {
            return category;
        }
    }
    
    return 'General';
}

// Generate Suggestions (Mock)
function generateSuggestions(prompt) {
    const suggestions = [];
    
    if (prompt.length < 50) {
        suggestions.push('Add more detail to your prompt');
    }
    
    if (!prompt.includes('?')) {
        suggestions.push('Consider framing as a question');
    }
    
    const promptLower = prompt.toLowerCase();
    if (!promptLower.includes('explain') && !promptLower.includes('describe')) {
        suggestions.push('Be more specific about what you want');
    }
    
    if (!promptLower.includes('example')) {
        suggestions.push('Request examples for clarity');
    }
    
    return suggestions;
}

// Generate Optimized Text (Mock)
function generateOptimizedText(prompt) {
    return `[Optimized] ${prompt} Please provide a detailed response with examples and specific explanations.`;
}
