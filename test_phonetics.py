import json
import urllib.request
import re

def edit_distance(list1, list2):
    if len(list1) < len(list2):
        return edit_distance(list2, list1)
    if len(list2) == 0:
        return len(list1)
    previous_row = range(len(list2) + 1)
    for i, c1 in enumerate(list1):
        current_row = [i + 1]
        for j, c2 in enumerate(list2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def load_cmu():
    print("Downloading CMU Pronouncing Dictionary...")
    url = 'http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    cmu_dict = {}
    with urllib.request.urlopen(req) as response:
        data = response.read().decode('ISO-8859-1')
    for line in data.split('\n'):
        if line.startswith(';') or not line.strip():
            continue
        parts = line.strip().split('  ')
        if len(parts) == 2:
            word = parts[0].lower().split('(')[0] # remove (1), (2) variants
            # Remove stress numbers from phonemes for broader matching
            phones = [re.sub(r'\d+', '', p) for p in parts[1].split()]
            if word not in cmu_dict:
                cmu_dict[word] = phones
    print(f"Loaded {len(cmu_dict)} unique words.")
    return cmu_dict

def test_10_words():
    cmu_dict = load_cmu()
    
    with open('data/luong/vocab.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    cards = data.get('cards', [])
    
    # Pick 10 specific cards for demonstration (skip simple ones if possible)
    test_cards = cards[10:20] 
    
    for c in test_cards:
        target_word = c['term'].lower()
        if target_word not in cmu_dict:
            print(f"\n[{target_word.upper()}] -> Not found in CMU dict.")
            continue
            
        target_phones = cmu_dict[target_word]
        
        distractors = []
        for word, phones in cmu_dict.items():
            # Skip exact matches or sub-words
            if word == target_word or target_word in word or word in target_word:
                continue
            # Must have similar length of phonemes
            if abs(len(phones) - len(target_phones)) > 2:
                continue
                
            dist = edit_distance(target_phones, phones)
            if dist > 0:
                distractors.append((dist, word, phones))
                
        distractors.sort(key=lambda x: x[0])
        
        # Pick top 5 distinct distractors
        results = []
        seen = set()
        for d, word, phones in distractors:
            if word not in seen:
                seen.add(word)
                results.append(word)
            if len(results) == 5:
                break
                
        print(f"\n[{target_word.upper()}] (Phones: {' '.join(target_phones)})")
        print(f"-> Distractors: {', '.join(results)}")

if __name__ == '__main__':
    test_10_words()
