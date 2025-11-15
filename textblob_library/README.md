# 🔤 TextBlob Spell Correction - NLP Library Demo

A practical demonstration of using **TextBlob**, a popular NLP library, for spell correction on search engine queries and user input. This project shows how TextBlob excels at correcting typos in entire phrases, not just individual words.

## 📋 Problem Statement

Search engines often receive queries with typos (approximately 13% of search terms contain spelling errors). This project provides:

1. **Reusable spell correction module** (`spell.py`) with TextBlob + fallback support
2. **CLI tool** for batch processing text files
3. **Web API + Interactive Frontend** with dataset showcase and analytics
4. **Unit tests** to validate functionality

## ✨ New Features - Dataset Showcase

The web interface now includes:
- 📊 **Statistics Dashboard** - View comprehensive dataset analytics
- 🎲 **Random Samples** - Test corrections on random entries from the dataset
- 🎯 **Accuracy Testing** - Measure TextBlob's performance on the dataset
- 📈 **Real-time Analytics** - See match rates, typo types, and common words

### Dataset Highlights
- **3,360 real typos** from e-commerce search queries
- **Single & multi-word typos** (e.g., "vynal grip strip" → "vinyl grip strip")
- **Multiple typo categories**: missing letters, extra letters, wrong letters
- **Common domains**: home improvement, hardware, tools, lighting

## 🚀 Quick Start

### Installation

```powershell
# Clone or navigate to the project
cd textblob_library

# Install dependencies
pip install -r requirements.txt

# Download TextBlob corpora (required for first use)
python -m textblob.download_corpora
```

### Running the Web Application

```powershell
# Start the Flask server
python app.py
```

Then open your browser to: **http://localhost:5000**

The web interface provides:
- ✨ Interactive spell correction
- 🎯 Real-time results
- 💡 Example queries to try
- 📊 Backend status display
- 📈 **Dataset Showcase** with statistics, samples, and accuracy testing
- 🎲 Test random entries from 3,360+ real typos
- 📊 View analytics on typo patterns and common words

### Using the CLI

```powershell
# Test with sample searches
python problem.py

# Process a file with typos
python problem.py --file typo.txt --out corrected_typos.txt
```

### API Usage

**Endpoint:** `POST /api/correct`

```bash
curl -X POST http://localhost:5000/api/correct \
  -H "Content-Type: application/json" \
  -d '{"text": "metal plate cover gcfi"}'
```

**Response:**
```json
{
  "original": "metal plate cover gcfi",
  "corrected": "metal plate cover gfci",
  "backend": "textblob",
  "backend_status": "available"
}
```

### Dataset API Endpoints

**Get Dataset Statistics:**
```bash
curl http://localhost:5000/api/dataset/stats
```

**Get Random Samples:**
```bash
curl http://localhost:5000/api/dataset/samples?count=10
```

**Test Accuracy:**
```bash
curl -X POST http://localhost:5000/api/dataset/test-accuracy \
  -H "Content-Type: application/json" \
  -d '{"sample_size": 50}'
```

## 📂 Project Structure

```
textblob_library/
├── spell.py              # Core spell correction module (TextBlob + fallback)
├── problem.py            # CLI tool for demonstrations
├── app.py                # Flask web server
├── templates/
│   └── index.html        # Web interface
├── static/
│   └── main.js           # Frontend JavaScript
├── tests/
│   └── test_spell.py     # Unit tests
├── typo.txt              # Sample data with 400+ typos
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## 🧪 Running Tests

```powershell
# Run all tests
python -m unittest discover -v

# Run specific test file
python -m unittest tests.test_spell -v
```

## 🎯 Example Corrections

| Original (Typo) | Corrected |
|----------------|-----------|
| `metal plate cover gcfi` | `metal plate cover gfci` |
| `artric air portable` | `arctic air portable` |
| `lawn mower- electic` | `lawn mower- electric` |
| `vynal grip strip` | `vinyl grip strip` |
| `basemetnt window` | `basement window` |
| `roll roofing lap cemet` | `roll roofing lap cement` |

## 🔧 How It Works

### TextBlob Approach
TextBlob uses statistical models trained on large text corpora to:
- Analyze entire phrases (context-aware)
- Handle multiple typos in one pass
- Provide natural language understanding

### Fallback Mode
If TextBlob isn't installed, the module falls back to:
- Dictionary-based corrections (common typos mapped)
- `difflib` for fuzzy matching
- Ensures the code always works

## 📊 Dataset

The `typo.txt` file contains **3,360 real-world search queries** with typos from a home improvement e-commerce dataset. These represent actual user input with various typo patterns:

### Statistics
- **Total entries:** 3,360
- **Single-word typos:** 139 (4%)
- **Multi-word typos:** 3,221 (96%)
- **Average words per typo:** 3.31

### Typo Types Distribution
- **Missing letters:** 1,283 entries (38%)
- **Extra letters:** 899 entries (27%)
- **Wrong letters:** 1,178 entries (35%)

### Most Common Words in Typos
door, light, for, and, water, shower, wall, paint, tile, ceiling

The web interface's **Dataset Showcase** section provides interactive analytics on these patterns!

## 🛠️ Technology Stack

- **Python 3.7+**
- **TextBlob** - NLP library for spell correction
- **Flask** - Web framework for API and frontend
- **Vanilla JavaScript** - Frontend interactivity
- **unittest** - Testing framework

## 📝 Use Cases

1. **Search Engines** - Correct user queries before search
2. **Form Validation** - Help users fix typos in real-time
3. **Data Cleaning** - Batch process text datasets
4. **Chatbots** - Understand misspelled user input
5. **E-commerce** - Improve product search accuracy

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Using TextBlob for practical NLP tasks
- ✅ Building REST APIs with Flask
- ✅ Creating responsive web interfaces
- ✅ Writing unit tests for ML/NLP code
- ✅ Implementing graceful fallbacks

## 🤝 Contributing

This is part of a larger repository for machine learning and deep learning libraries. Feel free to:
- Add more NLP libraries (spaCy, NLTK, etc.)
- Improve the UI/UX
- Add more test cases
- Optimize performance

## 📄 License

This project is for educational purposes. TextBlob is released under the MIT License.

## 🔗 Related Resources

- [TextBlob Documentation](https://textblob.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [NLP Best Practices](https://github.com/microsoft/nlp-recipes)

---

**Created as part of the Machine Learning Techniques repository** 🚀
