def analyze_improvements(original_prompt, optimized_prompt, original_score, optimized_score):
    """
    Analyze the improvements made to a prompt and generate explanations.
    
    Args:
        original_prompt (str): The original prompt
        optimized_prompt (str): The optimized prompt
        original_score (dict): Original score breakdown
        optimized_score (dict): Optimized score breakdown
    
    Returns:
        list: List of improvement explanations
    """
    improvements = []
    
    # Analyze score improvements
    score_improvements = []
    
    if optimized_score.get('length', 0) > original_score.get('length', 0):
        score_improvements.append("Improved length (more detailed)")
    
    if optimized_score.get('clarity', 0) > original_score.get('clarity', 0):
        score_improvements.append("Enhanced clarity")
    
    if optimized_score.get('specificity', 0) > original_score.get('specificity', 0):
        score_improvements.append("Increased specificity")
    
    if optimized_score.get('context', 0) > original_score.get('context', 0):
        score_improvements.append("Added context")
    
    if optimized_score.get('format', 0) > original_score.get('format', 0):
        score_improvements.append("Better formatting")
    
    # Analyze content changes
    original_lower = original_prompt.lower()
    optimized_lower = optimized_prompt.lower()
    
    # Check for added context
    context_keywords = ['context', 'background', 'scenario', 'situation', 'given', 'assume']
    original_context = any(kw in original_lower for kw in context_keywords)
    optimized_context = any(kw in optimized_lower for kw in context_keywords)
    
    if not original_context and optimized_context:
        improvements.append("✓ Added context/background information")
    
    # Check for expected output specification
    output_keywords = ['output', 'result', 'return', 'provide', 'generate', 'should']
    original_output = any(kw in original_lower for kw in output_keywords)
    optimized_output = any(kw in optimized_lower for kw in output_keywords)
    
    if not original_output and optimized_output:
        improvements.append("✓ Specified expected output format")
    
    # Check for constraints
    constraint_keywords = ['constraint', 'limit', 'within', 'maximum', 'minimum', 'must', 'should not']
    original_constraints = any(kw in original_lower for kw in constraint_keywords)
    optimized_constraints = any(kw in optimized_lower for kw in constraint_keywords)
    
    if not original_constraints and optimized_constraints:
        improvements.append("✓ Added constraints/limitations")
    
    # Check for examples
    example_keywords = ['example', 'for instance', 'such as', 'like', 'sample']
    original_examples = any(kw in original_lower for kw in example_keywords)
    optimized_examples = any(kw in optimized_lower for kw in example_keywords)
    
    if not original_examples and optimized_examples:
        improvements.append("✓ Included examples")
    
    # Check for structure/formatting
    structure_keywords = ['format', 'structure', 'list', 'bullet', 'numbered', 'paragraph']
    original_structure = any(kw in original_lower for kw in structure_keywords)
    optimized_structure = any(kw in optimized_lower for kw in structure_keywords)
    
    if not original_structure and optimized_structure:
        improvements.append("✓ Improved structure/formatting")
    
    # Check for clarity verbs
    clarity_verbs = ['explain', 'describe', 'analyze', 'compare', 'evaluate', 'summarize', 'define']
    original_clarity = any(kw in original_lower for kw in clarity_verbs)
    optimized_clarity = any(kw in optimized_lower for kw in clarity_verbs)
    
    if not original_clarity and optimized_clarity:
        improvements.append("✓ Enhanced clarity with action verbs")
    
    # Check for specificity
    specificity_keywords = ['specifically', 'detail', 'step-by-step', 'precise', 'exact', 'specific']
    original_specificity = any(kw in original_lower for kw in specificity_keywords)
    optimized_specificity = any(kw in optimized_lower for kw in specificity_keywords)
    
    if not original_specificity and optimized_specificity:
        improvements.append("✓ Increased specificity")
    
    # Check for length increase
    if len(optimized_prompt) > len(original_prompt) * 1.5:
        improvements.append("✓ Expanded with more detail")
    
    # Add score-based improvements if no content improvements found
    if not improvements and score_improvements:
        improvements.extend([f"✓ {imp}" for imp in score_improvements])
    
    # If still no improvements, add a general message
    if not improvements:
        improvements.append("✓ Refined prompt for better quality")
    
    return improvements
