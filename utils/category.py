def categorize_prompt(prompt):
    """
    Categorize a prompt based on its content and intent.
    Returns a category string.
    """
    if not prompt or not prompt.strip():
        return "General"
    
    prompt_lower = prompt.lower()
    
    categories = {
        "Creative Writing": ['write', 'story', 'creative', 'narrative', 'fiction', 'poem', 'character'],
        "Code & Programming": ['code', 'programming', 'function', 'algorithm', 'debug', 'python', 'javascript', 'api'],
        "Data Analysis": ['analyze', 'data', 'statistics', 'chart', 'graph', 'trend', 'dataset'],
        "Business": ['business', 'marketing', 'strategy', 'sales', 'revenue', 'customer', 'market'],
        "Education": ['teach', 'learn', 'explain', 'education', 'tutorial', 'lesson', 'study'],
        "Research": ['research', 'paper', 'academic', 'citation', 'reference', 'literature', 'study'],
        "Technical": ['technical', 'documentation', 'manual', 'guide', 'specification', 'implementation'],
        "Communication": ['email', 'message', 'letter', 'communication', 'response', 'reply'],
        "Problem Solving": ['solve', 'problem', 'solution', 'fix', 'resolve', 'troubleshoot'],
        "General": []
    }
    
    category_scores = {}
    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword in prompt_lower)
        if score > 0:
            category_scores[category] = score
    
    if category_scores:
        return max(category_scores, key=category_scores.get)
    
    return "General"
