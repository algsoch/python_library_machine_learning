"""Quick demo script to showcase spell correction capabilities."""

from spell import correct_text, get_backend_info

def main():
    # Show backend info
    backend = get_backend_info()
    print("=" * 70)
    print("🔤 TEXTBLOB SPELL CORRECTION DEMO")
    print("=" * 70)
    print(f"Backend: {backend['backend']}")
    print(f"Status: {backend['status']}")
    print("=" * 70)
    print()
    
    # Example corrections from real search queries
    examples = [
        "metal plate cover gcfi",
        "artric air portable", 
        "roll roofing lap cemet",
        "basemetnt window",
        "vynal grip strip",
        "lawn mower- electic",
        "cieling fan",
        "flourescent light bulbs",
        "dewalt cordless drill",
        "kitchen celing lights"
    ]
    
    print("📝 Example Corrections:")
    print("-" * 70)
    
    for text in examples:
        corrected = correct_text(text)
        status = "✓" if text != corrected else "→"
        print(f"{status} '{text}'")
        if text != corrected:
            print(f"  → '{corrected}'")
        print()
    
    print("=" * 70)
    print("\n💡 To try the web interface, run: python app.py")
    print("💡 To process a file, run: python problem.py --file typo.txt")
    print("💡 To run tests, run: python -m unittest discover tests -v")
    print()

if __name__ == '__main__':
    main()
