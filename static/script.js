// DOM Elements
const promptInput = document.getElementById('prompt-input');
const optimizeBtn = document.getElementById('optimize-btn');
const resultsSection = document.getElementById('results-section');
const scoreValue = document.getElementById('score-value');
const categoryValue = document.getElementById('category-value');
const suggestionsValue = document.getElementById('suggestions-value');
const optimizedPromptText = document.getElementById('optimized-prompt-text');

// Event Listeners
optimizeBtn.addEventListener('click', optimizePrompt);

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
        
        // Use real data from backend
        const score = data.score;
        const category = data.category;
        const suggestions = generateSuggestions(prompt);
        const optimizedText = data.optimized_prompt;
        
        // Display results
        scoreValue.textContent = score;
        categoryValue.textContent = category;
        suggestionsValue.textContent = suggestions;
        optimizedPromptText.textContent = optimizedText;
        
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
    
    return suggestions.length > 0 ? suggestions.join(', ') : 'Your prompt looks good!';
}

// Generate Optimized Text (Mock)
function generateOptimizedText(prompt) {
    return `[Optimized] ${prompt} Please provide a detailed response with examples and specific explanations.`;
}
