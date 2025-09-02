from flask import Flask, render_template, request, jsonify
from main import AIToolRecommendationSystem
import json

app = Flask(__name__)
system = AIToolRecommendationSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Please provide a query'}), 400
        
        result = system.recommend_tools(query)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Tool Recommendation Web Server...")
    print("📍 Visit: http://localhost:5000")
    app.run(debug=True, port=5000)
