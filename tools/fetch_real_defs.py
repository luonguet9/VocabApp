import urllib.request, json, ssl, os, time

DUMMY_PATTERNS = [
    "A common workplace expression or phrase used in daily team communication",
    "A professional English phrase and workplace expression commonly utilized in",
    "An action verb used in",
    "An adjective describing a condition, quality, or characteristic of",
    "An adverbial modifier expressing the manner, frequency, or degree of",
    "A connecting grammatical term or preposition used in",
    "A standard technical or professional terminology item referenced frequently across",
    "To put forward an idea, technical proposal, or approach for consideration by the team."
]

def is_dummy(def_str):
    for p in DUMMY_PATTERNS:
        if def_str.startswith(p) or def_str == p:
            return True
    return False

def get_def(word):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        # get the first word if it's a phrase, maybe dictionary API fails on phrases
        # but let's try the full term first
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(word)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, context=ctx)
        data = json.loads(resp.read())
        for m in data[0].get('meanings', []):
            for d in m.get('definitions', []):
                return d.get('definition')
    except Exception as e:
        return None
    return None

def main():
    vocab_path = os.path.join(os.path.dirname(__file__), '..', 'vocab.json')
    with open(vocab_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    cards = data.get('cards', [])
    updated = 0
    failed = 0
    
    # We will only process a subset if it takes too long, but let's try all
    for i, c in enumerate(cards):
        en_def = c.get('en_def', '')
        if is_dummy(en_def):
            term = c.get('term', '').strip()
            real_def = get_def(term)
            if real_def:
                c['en_def'] = real_def
                updated += 1
                print(f"Updated: {term} -> {real_def}")
            else:
                # If it's a phrase or dictionary fails, create a simpler fallback without sounding like a robot
                pos = c.get('pos', '').replace('.', '')
                if pos:
                    c['en_def'] = f"A {pos} commonly used in {c.get('topic', 'Business')} contexts."
                else:
                    c['en_def'] = f"A term commonly used in {c.get('topic', 'Business')} contexts."
                failed += 1
            # sleep slightly to avoid rate limit
            time.sleep(0.05)
            
    with open(vocab_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Done! Updated {updated} with real definitions, {failed} used simple fallback.")

if __name__ == '__main__':
    main()
