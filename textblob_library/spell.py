"""Spell correction module using TextBlob with fallback support.

This module provides spell correction capabilities, preferring TextBlob
when available, and falling back to a dictionary-based approach with
difflib for similarity matching.
"""

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    import difflib


# Common typo corrections from the dataset
CORRECTION_MAP = {
    'steele stake': 'steel stake',
    'gas mowe': 'gas mower',
    'metal plate cover gcfi': 'metal plate cover gfci',
    'lawn sprkinler': 'lawn sprinkler',
    'basemetnt window': 'basement window',
    'vynal grip strip': 'vinyl grip strip',
    'lawn mower- electic': 'lawn mower- electric',
    'artric air portable': 'arctic air portable',
    'roll roofing lap cemet': 'roll roofing lap cement',
    'cieling': 'ceiling',
    'celling light': 'ceiling light',
    'vynal': 'vinyl',
    'electic': 'electric',
    'tolet': 'toilet',
    'toliet': 'toilet',
    'flourescent': 'fluorescent',
    'florescent': 'fluorescent',
}


def correct_text(text):
    """Correct spelling in the given text.
    
    Args:
        text (str): Input text with potential typos
        
    Returns:
        str: Corrected text
    """
    if not text or not text.strip():
        return text
    
    if TEXTBLOB_AVAILABLE:
        return _correct_with_textblob(text)
    else:
        return _correct_with_fallback(text)


def _correct_with_textblob(text):
    """Correct text using TextBlob library."""
    blob = TextBlob(text)
    return str(blob.correct())


def _correct_with_fallback(text):
    """Fallback correction using dictionary and difflib."""
    # First, check if the entire text is in our correction map
    text_lower = text.lower()
    if text_lower in CORRECTION_MAP:
        return CORRECTION_MAP[text_lower]
    
    # Try word-by-word correction
    words = text.split()
    corrected_words = []
    
    for word in words:
        word_lower = word.lower()
        if word_lower in CORRECTION_MAP:
            corrected_words.append(CORRECTION_MAP[word_lower])
        else:
            # Try to find close matches in our dictionary
            matches = difflib.get_close_matches(word_lower, CORRECTION_MAP.keys(), n=1, cutoff=0.8)
            if matches:
                corrected_words.append(CORRECTION_MAP[matches[0]])
            else:
                corrected_words.append(word)
    
    return ' '.join(corrected_words)


def get_backend_info():
    """Return information about which correction backend is being used."""
    if TEXTBLOB_AVAILABLE:
        return {"backend": "textblob", "status": "available"}
    else:
        return {"backend": "fallback (dictionary + difflib)", "status": "textblob not installed"}
