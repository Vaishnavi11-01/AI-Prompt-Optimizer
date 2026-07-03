from flask import Flask, render_template, request, jsonify
from utils.gemini import optimize_prompt
from utils.score import calculate_prompt_score
from utils.category import categorize_prompt

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        # Optimize the prompt using Gemini
        optimized_text = optimize_prompt(prompt)
        
        # Calculate score and category
        score = calculate_prompt_score(prompt)
        category = categorize_prompt(prompt)
        
        return jsonify({
            "optimized_text": optimized_text,
            "score": score,
            "category": category
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
