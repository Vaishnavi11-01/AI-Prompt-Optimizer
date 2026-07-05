def calculate_prompt_score(prompt):
    """
    Calculate a quality score for a prompt based on various criteria.
    Returns a dictionary with individual category scores and total score.
    """
    if not prompt or not prompt.strip():
        return {
            'total': 0.0,
            'length': 0,
            'clarity': 0,
            'specificity': 0,
            'context': 0,
            'format': 0
        }
    
    scores = {
        'length': 0,
        'clarity': 0,
        'specificity': 0,
        'context': 0,
        'format': 0
    }
    
    prompt_lower = prompt.lower()
    
    # Length criteria (optimal length: 50-500 characters)
    length = len(prompt)
    if 50 <= length <= 500:
        scores['length'] = 20
    elif length > 500:
        scores['length'] = 15
    elif length > 20:
        scores['length'] = 10
    
    # Clarity indicators
    clarity_keywords = ['explain', 'describe', 'analyze', 'compare', 'evaluate', 'summarize', 'define']
    if any(keyword in prompt_lower for keyword in clarity_keywords):
        scores['clarity'] = 15
    
    # Specificity indicators
    specificity_keywords = ['specifically', 'detail', 'example', 'step', 'include', 'provide']
    if any(keyword in prompt_lower for keyword in specificity_keywords):
        scores['specificity'] = 15
    
    # Context indicators
    context_keywords = ['context', 'background', 'scenario', 'situation', 'given']
    if any(keyword in prompt_lower for keyword in context_keywords):
        scores['context'] = 10
    
    # Format indicators
    format_keywords = ['format', 'structure', 'list', 'paragraph', 'bullet', 'table']
    if any(keyword in prompt_lower for keyword in format_keywords):
        scores['format'] = 10
    
    # Calculate total score
    total = sum(scores.values())
    
    # Avoid ambiguity penalty
    ambiguous_keywords = ['maybe', 'perhaps', 'possibly', 'might', 'could be']
    if any(keyword in prompt_lower for keyword in ambiguous_keywords):
        total -= 10
    
    # Cap score at 100
    total = min(max(total, 0), 100)
    
    scores['total'] = total
    return scores
