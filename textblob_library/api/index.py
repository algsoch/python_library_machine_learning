"""Vercel serverless function entry point for Flask app.

This file is required for Vercel deployment.
It wraps the Flask app for serverless execution.
"""

import sys
import os

# Add parent directory to path so we can import from textblob_library
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from spell import correct_text, get_backend_info
from typo_analyzer import (
    parse_typo_file, 
    get_dataset_statistics, 
    get_random_samples,
    test_correction_accuracy
)

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

# Load typo dataset on startup (with correct path for Vercel)
import os
typo_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'typo.txt')
TYPO_DICT = parse_typo_file(typo_file_path)


@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')


@app.route('/api/correct', methods=['POST'])
def api_correct():
    """API endpoint to correct spelling in text."""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing "text" field in request'}), 400
    
    original_text = data['text']
    corrected_text = correct_text(original_text)
    backend = get_backend_info()
    
    return jsonify({
        'original': original_text,
        'corrected': corrected_text,
        'backend': backend['backend'],
        'backend_status': backend['status']
    })


@app.route('/api/info', methods=['GET'])
def api_info():
    """Get information about the correction backend."""
    return jsonify(get_backend_info())


@app.route('/api/dataset/stats', methods=['GET'])
def api_dataset_stats():
    """Get statistics about the typo dataset."""
    stats = get_dataset_statistics(TYPO_DICT)
    stats['dataset_name'] = 'typo.txt'
    return jsonify(stats)


@app.route('/api/dataset/samples', methods=['GET'])
def api_dataset_samples():
    """Get random samples from the typo dataset with corrections."""
    count = request.args.get('count', 10, type=int)
    count = min(count, 50)
    
    samples = get_random_samples(TYPO_DICT, count)
    
    return jsonify({
        'samples': samples,
        'count': len(samples)
    })


@app.route('/api/dataset/test-accuracy', methods=['POST'])
def api_test_accuracy():
    """Test TextBlob accuracy on the dataset."""
    data = request.get_json() or {}
    sample_size = data.get('sample_size', 50)
    sample_size = min(sample_size, 100)
    
    accuracy_data = test_correction_accuracy(TYPO_DICT, sample_size)
    
    return jsonify(accuracy_data)


# Vercel serverless function handler
def handler(request):
    """Handler function for Vercel serverless."""
    with app.request_context(request.environ):
        return app.full_dispatch_request()


# For Vercel
app = app
