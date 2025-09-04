from flask import Flask, render_template, request, jsonify
from main import AIToolRecommendationSystem
import json
import os

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

@app.route('/find-with-ai', methods=['POST'])
def find_with_ai():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Please provide a query'}), 400
        
        result = system.find_with_ai(query)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Tool Recommendation Web Server...")
    
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get('PORT', 5000))
    
    # Bind to 0.0.0.0 for production deployment
    host = '0.0.0.0'
    
    print(f"📍 Visit: http://localhost:{port}")
    
    # Use debug=False for production
    app.run(debug=False, host=host, port=port)
