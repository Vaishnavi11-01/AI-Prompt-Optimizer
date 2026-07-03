def calculate_prompt_score(prompt):
    """
    Calculate a quality score for a prompt based on various criteria.
    Returns a score between 0 and 100.
    """
    if not prompt or not prompt.strip():
        return 0.0
    
    score = 0.0
    prompt_lower = prompt.lower()
    
    # Length criteria (optimal length: 50-500 characters)
    length = len(prompt)
    if 50 <= length <= 500:
        score += 20
    elif length > 500:
        score += 15
    elif length > 20:
        score += 10
    
    # Clarity indicators
    clarity_keywords = ['explain', 'describe', 'analyze', 'compare', 'evaluate', 'summarize', 'define']
    if any(keyword in prompt_lower for keyword in clarity_keywords):
        score += 15
    
    # Specificity indicators
    specificity_keywords = ['specifically', 'detail', 'example', 'step', 'include', 'provide']
    if any(keyword in prompt_lower for keyword in specificity_keywords):
        score += 15
    
    # Context indicators
    context_keywords = ['context', 'background', 'scenario', 'situation', 'given']
    if any(keyword in prompt_lower for keyword in context_keywords):
        score += 10
    
    # Format indicators
    format_keywords = ['format', 'structure', 'list', 'paragraph', 'bullet', 'table']
    if any(keyword in prompt_lower for keyword in format_keywords):
        score += 10
    
    # Question mark presence
    if '?' in prompt:
        score += 10
    
    # Avoid ambiguity
    ambiguous_keywords = ['maybe', 'perhaps', 'possibly', 'might', 'could be']
    if any(keyword in prompt_lower for keyword in ambiguous_keywords):
        score -= 10
    
    # Cap score at 100
    return min(max(score, 0), 100)
