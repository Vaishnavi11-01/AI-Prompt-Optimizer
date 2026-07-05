from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

def generate_pdf_report(original_prompt, optimized_prompt, original_score, category, suggestions):
    """
    Generate a PDF report for prompt optimization.
    
    Args:
        original_prompt (str): The original prompt
        optimized_prompt (str): The optimized prompt
        original_score (dict): Score breakdown with total
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
    
    # Score Information
    total_score = original_score.get('total', 0)
    story.append(Paragraph(f"<b>Overall Score:</b> {round(total_score)}/100", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Score Breakdown Table
    score_data = [
        ['Metric', 'Score', 'Maximum'],
        ['Length', str(original_score.get('length', 0)), '20'],
        ['Clarity', str(original_score.get('clarity', 0)), '15'],
        ['Specificity', str(original_score.get('specificity', 0)), '15'],
        ['Context', str(original_score.get('context', 0)), '10'],
        ['Format', str(original_score.get('format', 0)), '10'],
    ]
    
    score_table = Table(score_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(score_table)
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
