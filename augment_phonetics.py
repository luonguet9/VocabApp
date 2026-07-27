import json
import urllib.request
import re
import os

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
            word = parts[0].lower().split('(')[0]
            phones = [re.sub(r'\d+', '', p) for p in parts[1].split()]
            if word not in cmu_dict:
                cmu_dict[word] = phones
    print(f"Loaded {len(cmu_dict)} unique words from CMU.")
    return cmu_dict

import json
import urllib.request
import re
import os
import ssl

def load_common_words():
    print("Downloading Top 10,000 common English words...")
    url = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    common = set()
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = response.read().decode('utf-8')
        for w in data.split('\n'):
            w = w.strip().lower()
            if w: common.add(w)
        print(f"Loaded {len(common)} common words.")
    except Exception as e:
        print("Could not download common words list. Will rely on alphabetical filter.", e)
    return common

def augment_file(filepath, cmu_dict, common_words):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found!")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    cards = data.get('cards', [])
    updated = 0
    
    deck_words = {c['term'].lower() for c in cards}
    
    search_pool = {}
    for w in deck_words.union(common_words):
        if w in cmu_dict:
            search_pool[w] = cmu_dict[w]
            
    print(f"[{filepath}] Search pool size: {len(search_pool)} words.")

    for i, c in enumerate(cards):
        target_word = c['term'].lower()
        if target_word not in cmu_dict:
            continue
            
        target_phones = cmu_dict[target_word]
        distractors = []
        
        for word, phones in search_pool.items():
            if word == target_word or target_word in word or word in target_word:
                continue
            if abs(len(phones) - len(target_phones)) > 2:
                continue
                
            dist = edit_distance(target_phones, phones)
            if dist > 0:
                score = dist
                if word in deck_words:
                    score -= 0.5 
                
                distractors.append((score, word, phones))
                
        distractors.sort(key=lambda x: x[0])
        
        results = []
        seen = set()
        valid_2 = {'is','it','in','on','to','do','go','no','so','be','he','me','we','as','at','by','my','of','or','up','us','an','am','if','oh','ah'}
        for s, word, phones in distractors:
            if not word.isalpha():
                continue
            if len(word) <= 2 and word not in valid_2 and word not in deck_words:
                continue
            if word not in seen:
                seen.add(word)
                results.append(word)
            if len(results) == 5:
                break
                
        c['phonetic_distractors'] = results
        updated += 1
        
        if i % 100 == 0 and i > 0:
            print(f"[{filepath}] Processed {i} cards...")
            
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully augmented {updated} cards in {filepath}")

if __name__ == '__main__':
    cmu_dict = load_cmu()
    common_words = load_common_words()
    
    augment_file('data/luong/vocab.json', cmu_dict, common_words)
    augment_file('data/khanh/vocab.json', cmu_dict, common_words)
