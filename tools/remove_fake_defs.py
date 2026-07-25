import json, os

def main():
    vocab_path = os.path.join(os.path.dirname(__file__), '..', 'vocab.json')
    with open(vocab_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    removed = 0
    for c in data.get('cards', []):
        en_def = c.get('en_def', '')
        if "commonly used in" in en_def:
            c['en_def'] = ""
            removed += 1
            
    with open(vocab_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Removed {removed} fake definitions.")

if __name__ == '__main__':
    main()
