"""Flask web application for spell correction using TextBlob.

This app provides:
- A web interface for interactive spell correction
- REST API endpoint for programmatic access
- Backend info showing which correction engine is in use

Run with:
    python app.py
    
Then visit http://localhost:5000 in your browser.
"""

from flask import Flask, render_template, request, jsonify
from spell import correct_text, get_backend_info
from typo_analyzer import (
    parse_typo_file, 
    get_dataset_statistics, 
    get_random_samples,
    test_correction_accuracy
)

app = Flask(__name__)

# Load typo dataset on startup
TYPO_DICT = parse_typo_file()


@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')


@app.route('/api/correct', methods=['POST'])
def api_correct():
    """API endpoint to correct spelling in text.
    
    Request JSON:
        {
            "text": "text with typos to correct"
        }
    
    Response JSON:
        {
            "original": "original text",
            "corrected": "corrected text",
            "backend": "textblob" or "fallback"
        }
    """
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
    """Get statistics about the typo dataset.
    
    Response JSON:
        {
            "total_entries": 400,
            "single_word_typos": 150,
            "multi_word_typos": 250,
            "avg_words_per_typo": 3.2,
            "typo_types": {...},
            "common_words": [...]
        }
    """
    stats = get_dataset_statistics(TYPO_DICT)
    stats['dataset_name'] = 'typo.txt'
    return jsonify(stats)


@app.route('/api/dataset/samples', methods=['GET'])
def api_dataset_samples():
    """Get random samples from the typo dataset with corrections.
    
    Query params:
        count: Number of samples (default: 10, max: 50)
    
    Response JSON:
        {
            "samples": [
                {
                    "typo": "original typo",
                    "expected": "expected correction",
                    "textblob": "textblob correction",
                    "matches": true/false
                },
                ...
            ]
        }
    """
    count = request.args.get('count', 10, type=int)
    count = min(count, 50)  # Limit to 50 samples max
    
    samples = get_random_samples(TYPO_DICT, count)
    
    return jsonify({
        'samples': samples,
        'count': len(samples)
    })


@app.route('/api/dataset/test-accuracy', methods=['POST'])
def api_test_accuracy():
    """Test TextBlob accuracy on the dataset.
    
    Request JSON:
        {
            "sample_size": 50  (optional, default: 50, max: 100)
        }
    
    Response JSON:
        {
            "accuracy": 75.5,
            "correct_count": 38,
            "total_tested": 50,
            "results": [...]
        }
    """
    data = request.get_json() or {}
    sample_size = data.get('sample_size', 50)
    sample_size = min(sample_size, 100)  # Limit to 100 samples max
    
    accuracy_data = test_correction_accuracy(TYPO_DICT, sample_size)
    
    return jsonify(accuracy_data)


if __name__ == '__main__':
    backend = get_backend_info()
    print(f"\n{'='*60}")
    print(f"🚀 Spell Correction API Starting...")
    print(f"📚 Backend: {backend['backend']}")
    print(f"✅ Status: {backend['status']}")
    print(f"🌐 Visit: http://localhost:5000")
    print(f"{'='*60}\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
