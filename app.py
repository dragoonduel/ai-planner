from flask import Flask, request, jsonify, render_template

# Ensure to load asyncio and trip_planner
import asyncio
from trip_planner import main as plan_trip

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan', methods=['POST'])
def plan():
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"error": "Prompt is required"}), 400
    
    prompt = data['prompt']
    
    try:
        # Run the async function synchronously to avoid Flask async requirements
        result = asyncio.run(plan_trip(prompt))
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True, port=5000, use_reloader=False)
