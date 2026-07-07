from flask import Flask, render_template, request, jsonify, send_file
from utils.gemini import optimize_prompt
from utils.score import calculate_prompt_score
from utils.category import categorize_prompt
from utils.pdf_generator import generate_pdf_report
from utils.improvement_analyzer import analyze_improvements
from utils.diff_generator import generate_inline_diff
import sqlite3
import os
import json
from datetime import datetime
from io import BytesIO

app = Flask(__name__)

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'prompts.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.get_json()
    prompt = data.get("prompt", "")
    model_name = data.get("model", "flash")  # Default to flash
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        # Calculate original score
        original_scores = calculate_prompt_score(prompt)
        
        # Optimize the prompt using Gemini with selected model
        optimized_prompt = optimize_prompt(prompt, model_name)
        
        # Calculate optimized score
        optimized_scores = calculate_prompt_score(optimized_prompt)
        
        # Calculate improvement
        improvement = optimized_scores['total'] - original_scores['total']
        
        # Categorize the original prompt
        category = categorize_prompt(prompt)
        
        # Analyze improvements
        improvements = analyze_improvements(prompt, optimized_prompt, original_scores, optimized_scores)
        
        # Generate diff
        diff_html = generate_inline_diff(prompt, optimized_prompt)
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO prompts (original_prompt, optimized_prompt, category, score, model_used)
            VALUES (?, ?, ?, ?, ?)
        ''', (prompt, optimized_prompt, category, optimized_scores['total'], f'gemini-1.5-{model_name}'))
        conn.commit()
        conn.close()
        
        return jsonify({
            "optimized_prompt": optimized_prompt,
            "original_score": original_scores,
            "optimized_score": optimized_scores,
            "improvement": improvement,
            "category": category,
            "improvements": improvements,
            "diff": diff_html,
            "model_used": f'gemini-1.5-{model_name}',
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route("/history", methods=["GET"])
def get_history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, original_prompt, optimized_prompt, category, score, model_used, created_at
            FROM prompts
            ORDER BY created_at DESC
        ''')
        prompts = cursor.fetchall()
        conn.close()
        
        history = []
        for prompt in prompts:
            history.append({
                "id": prompt['id'],
                "original_prompt": prompt['original_prompt'],
                "optimized_prompt": prompt['optimized_prompt'],
                "category": prompt['category'],
                "score": prompt['score'],
                "model_used": prompt['model_used'],
                "created_at": prompt['created_at']
            })
        
        return jsonify({"history": history, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route("/history/<int:prompt_id>", methods=["GET"])
def get_prompt(prompt_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, original_prompt, optimized_prompt, category, score, model_used, created_at
            FROM prompts
            WHERE id = ?
        ''', (prompt_id,))
        prompt = cursor.fetchone()
        conn.close()
        
        if not prompt:
            return jsonify({"error": "Prompt not found", "status": "error"}), 404
        
        return jsonify({
            "id": prompt['id'],
            "original_prompt": prompt['original_prompt'],
            "optimized_prompt": prompt['optimized_prompt'],
            "category": prompt['category'],
            "score": prompt['score'],
            "model_used": prompt['model_used'],
            "created_at": prompt['created_at'],
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route("/history/<int:prompt_id>", methods=["DELETE"])
def delete_prompt(prompt_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM prompts WHERE id = ?', (prompt_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Prompt deleted successfully", "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route("/stats", methods=["GET"])
def get_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total prompts
        cursor.execute('SELECT COUNT(*) as total FROM prompts')
        total_prompts = cursor.fetchone()['total']
        
        # Average score
        cursor.execute('SELECT AVG(score) as avg_score FROM prompts')
        avg_score = cursor.fetchone()['avg_score'] or 0
        
        # Most used category
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM prompts 
            GROUP BY category 
            ORDER BY count DESC 
            LIMIT 1
        ''')
        most_used = cursor.fetchone()
        most_used_category = most_used['category'] if most_used else 'N/A'
        
        # Category distribution
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM prompts 
            GROUP BY category
        ''')
        category_distribution = {}
        for row in cursor.fetchall():
            category_distribution[row['category']] = row['count']
        
        # Monthly usage (last 6 months)
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', created_at) as month,
                COUNT(*) as count
            FROM prompts
            WHERE created_at >= date('now', '-6 months')
            GROUP BY month
            ORDER BY month
        ''')
        monthly_usage = {}
        for row in cursor.fetchall():
            monthly_usage[row['month']] = row['count']
        
        conn.close()
        
        return jsonify({
            "total_prompts": total_prompts,
            "average_score": round(avg_score, 2),
            "most_used_category": most_used_category,
            "category_distribution": category_distribution,
            "monthly_usage": monthly_usage,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route("/export/json", methods=["GET"])
def export_json():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, original_prompt, optimized_prompt, category, score, model_used, created_at
            FROM prompts
            ORDER BY created_at DESC
        ''')
        prompts = cursor.fetchall()
        conn.close()
        
        export_data = []
        for prompt in prompts:
            export_data.append({
                "id": prompt['id'],
                "original_prompt": prompt['original_prompt'],
                "optimized_prompt": prompt['optimized_prompt'],
                "category": prompt['category'],
                "score": prompt['score'],
                "model_used": prompt['model_used'],
                "created_at": prompt['created_at']
            })
        
        response = jsonify({
            "export_date": str(datetime.now()),
            "total_prompts": len(export_data),
            "prompts": export_data
        })
        response.headers['Content-Disposition'] = 'attachment; filename=prompt_history.json'
        return response
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    try:
        data = request.get_json()
        original_prompt = data.get("original_prompt", "")
        optimized_prompt = data.get("optimized_prompt", "")
        original_score = data.get("original_score", {})
        optimized_score = data.get("optimized_score", {})
        improvement = data.get("improvement", 0)
        category = data.get("category", "")
        suggestions = data.get("suggestions", [])
        
        # Generate PDF
        pdf_content = generate_pdf_report(
            original_prompt,
            optimized_prompt,
            original_score,
            optimized_score,
            improvement,
            category,
            suggestions
        )
        
        # Send file
        buffer = BytesIO(pdf_content)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"prompt_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
