"""Module to parse and analyze the typo dataset."""

import re
from collections import Counter
from spell import correct_text


def parse_typo_file(filepath='typo.txt'):
    """Parse the typo.txt file and return a dictionary of typo -> correct mappings.
    
    Returns:
        dict: Dictionary with 'typo': 'correct' pairs
    """
    typo_dict = {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse the dictionary structure
        # Format: 'typo': 'correct',
        pattern = r"'([^']+)':\s*'([^']+)'"
        matches = re.findall(pattern, content)
        
        for typo, correct in matches:
            typo_dict[typo] = correct
            
    except Exception as e:
        print(f"Error parsing typo file: {e}")
    
    return typo_dict


def get_dataset_statistics(typo_dict):
    """Calculate statistics about the typo dataset.
    
    Returns:
        dict: Statistics about the dataset
    """
    total_entries = len(typo_dict)
    
    # Calculate average word count
    typo_word_counts = [len(typo.split()) for typo in typo_dict.keys()]
    avg_words_typo = sum(typo_word_counts) / len(typo_word_counts) if typo_word_counts else 0
    
    # Count single vs multi-word typos
    single_word = sum(1 for typo in typo_dict.keys() if len(typo.split()) == 1)
    multi_word = total_entries - single_word
    
    # Common typo patterns
    typo_types = {
        'missing_letters': 0,
        'extra_letters': 0,
        'swapped_letters': 0,
        'wrong_letters': 0
    }
    
    for typo, correct in typo_dict.items():
        if len(typo) < len(correct):
            typo_types['missing_letters'] += 1
        elif len(typo) > len(correct):
            typo_types['extra_letters'] += 1
        else:
            typo_types['wrong_letters'] += 1
    
    # Find common words in typos
    all_words = []
    for typo in typo_dict.keys():
        all_words.extend(typo.lower().split())
    
    common_words = Counter(all_words).most_common(10)
    
    return {
        'total_entries': total_entries,
        'single_word_typos': single_word,
        'multi_word_typos': multi_word,
        'avg_words_per_typo': round(avg_words_typo, 2),
        'typo_types': typo_types,
        'common_words': [{'word': word, 'count': count} for word, count in common_words]
    }


def get_random_samples(typo_dict, count=10):
    """Get random samples from the typo dictionary.
    
    Returns:
        list: List of {'typo': 'text', 'expected': 'correct', 'textblob': 'corrected'} dicts
    """
    import random
    
    items = list(typo_dict.items())
    if len(items) > count:
        items = random.sample(items, count)
    
    samples = []
    for typo, expected in items:
        textblob_result = correct_text(typo)
        samples.append({
            'typo': typo,
            'expected': expected,
            'textblob': textblob_result,
            'matches': textblob_result.lower() == expected.lower()
        })
    
    return samples


def test_correction_accuracy(typo_dict, sample_size=50):
    """Test TextBlob's accuracy on a sample of the dataset.
    
    Returns:
        dict: Accuracy statistics
    """
    import random
    
    items = list(typo_dict.items())
    if len(items) > sample_size:
        items = random.sample(items, sample_size)
    
    correct_count = 0
    total = len(items)
    
    results = []
    for typo, expected in items:
        corrected = correct_text(typo)
        is_correct = corrected.lower() == expected.lower()
        if is_correct:
            correct_count += 1
        
        results.append({
            'typo': typo,
            'expected': expected,
            'corrected': corrected,
            'correct': is_correct
        })
    
    accuracy = (correct_count / total * 100) if total > 0 else 0
    
    return {
        'accuracy': round(accuracy, 2),
        'correct_count': correct_count,
        'total_tested': total,
        'results': results
    }


if __name__ == '__main__':
    # Test the module
    typo_dict = parse_typo_file()
    print(f"Loaded {len(typo_dict)} typo entries")
    
    stats = get_dataset_statistics(typo_dict)
    print("\nDataset Statistics:")
    print(f"Total entries: {stats['total_entries']}")
    print(f"Single-word typos: {stats['single_word_typos']}")
    print(f"Multi-word typos: {stats['multi_word_typos']}")
    print(f"Average words per typo: {stats['avg_words_per_typo']}")
    
    print("\nTesting accuracy...")
    accuracy = test_correction_accuracy(typo_dict, sample_size=20)
    print(f"Accuracy: {accuracy['accuracy']}% ({accuracy['correct_count']}/{accuracy['total_tested']})")
