def generate_diff(original_text, optimized_text):
    """
    Generate a word-level diff between original and optimized text.
    
    Args:
        original_text (str): The original text
        optimized_text (str): The optimized text
    
    Returns:
        list: List of diff segments with type ('add', 'remove', 'equal') and content
    """
    import difflib
    
    # Split into words for better granularity
    original_words = original_text.split()
    optimized_words = optimized_text.split()
    
    # Use difflib to get the diff
    matcher = difflib.SequenceMatcher(None, original_words, optimized_words)
    
    diff_result = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        original_segment = ' '.join(original_words[i1:i2])
        optimized_segment = ' '.join(optimized_words[j1:j2])
        
        if tag == 'equal':
            diff_result.append({
                'type': 'equal',
                'content': optimized_segment
            })
        elif tag == 'replace':
            if original_segment:
                diff_result.append({
                    'type': 'remove',
                    'content': original_segment
                })
            if optimized_segment:
                diff_result.append({
                    'type': 'add',
                    'content': optimized_segment
                })
        elif tag == 'delete':
            diff_result.append({
                'type': 'remove',
                'content': original_segment
            })
        elif tag == 'insert':
            diff_result.append({
                'type': 'add',
                'content': optimized_segment
            })
    
    return diff_result

def generate_inline_diff(original_text, optimized_text):
    """
    Generate an inline diff with HTML formatting.
    
    Args:
        original_text (str): The original text
        optimized_text (str): The optimized text
    
    Returns:
        str: HTML-formatted diff with green additions and red removals
    """
    diff_segments = generate_diff(original_text, optimized_text)
    
    html_diff = []
    
    for segment in diff_segments:
        if segment['type'] == 'equal':
            html_diff.append(segment['content'])
        elif segment['type'] == 'add':
            html_diff.append(f'<span class="diff-add">+ {segment["content"]}</span>')
        elif segment['type'] == 'remove':
            html_diff.append(f'<span class="diff-remove">- {segment["content"]}</span>')
    
    return ' '.join(html_diff)
