from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

def generate_pdf_report(original_prompt, optimized_prompt, original_score, optimized_score, improvement, category, suggestions):
    """
    Generate a PDF report for prompt optimization.
    
    Args:
        original_prompt (str): The original prompt
        optimized_prompt (str): The optimized prompt
        original_score (dict): Original score breakdown with total
        optimized_score (dict): Optimized score breakdown with total
        improvement (float): Score improvement
        category (str): Prompt category
        suggestions (list): List of suggestions
    
    Returns:
        bytes: PDF file content
    """
    from io import BytesIO
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#6366f1'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#374151'),
        spaceAfter=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#4b5563'),
        spaceAfter=12
    )
    
    # Build the story
    story = []
    
    # Title
    story.append(Paragraph("Prompt Optimization Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Date and Time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"<b>Generated:</b> {current_time}", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Category
    story.append(Paragraph(f"<b>Category:</b> {category}", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Score Comparison Table
    score_comparison_data = [
        ['Metric', 'Original', 'Optimized', 'Improvement'],
        ['Total Score', str(round(original_score.get('total', 0))), str(round(optimized_score.get('total', 0))), f"+{round(improvement)}" if improvement >= 0 else str(round(improvement))],
        ['Length', str(original_score.get('length', 0)), str(optimized_score.get('length', 0)), str(optimized_score.get('length', 0) - original_score.get('length', 0))],
        ['Clarity', str(original_score.get('clarity', 0)), str(optimized_score.get('clarity', 0)), str(optimized_score.get('clarity', 0) - original_score.get('clarity', 0))],
        ['Specificity', str(original_score.get('specificity', 0)), str(optimized_score.get('specificity', 0)), str(optimized_score.get('specificity', 0) - original_score.get('specificity', 0))],
        ['Context', str(original_score.get('context', 0)), str(optimized_score.get('context', 0)), str(optimized_score.get('context', 0) - original_score.get('context', 0))],
        ['Format', str(original_score.get('format', 0)), str(optimized_score.get('format', 0)), str(optimized_score.get('format', 0) - original_score.get('format', 0))],
    ]
    
    score_comparison_table = Table(score_comparison_data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
    score_comparison_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(score_comparison_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Original Prompt
    story.append(Paragraph("Original Prompt", heading_style))
    story.append(Paragraph(original_prompt, normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Optimized Prompt
    story.append(Paragraph("Optimized Prompt", heading_style))
    story.append(Paragraph(optimized_prompt, normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Suggestions
    if suggestions and len(suggestions) > 0:
        story.append(Paragraph("Suggestions for Improvement", heading_style))
        for i, suggestion in enumerate(suggestions, 1):
            story.append(Paragraph(f"{i}. {suggestion}", normal_style))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF content
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return pdf_content
