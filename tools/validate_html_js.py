import re

def check_file(path):
    print(f"Checking {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check script tags
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    print(f"Found {len(scripts)} script block(s).")

    for idx, s in enumerate(scripts):
        # Check brace balance
        open_b = s.count('{')
        close_b = s.count('}')
        print(f"Script block #{idx+1}: {open_b} open braces, {close_b} close braces.")
        if open_b != close_b:
            print(f"WARNING: Brace mismatch in {path} script #{idx+1}!")
        else:
            print(f"Braces perfectly balanced in {path} script #{idx+1}!")

        # Verify key functions exist
        for fn in ['getSimilarity', 'getCardTier', 'getSmartDistractors', 'renderQuiz', 'checkAnswer']:
            if fn in s:
                print(f"  [OK] Function/Reference '{fn}' found.")
            else:
                print(f"  [MISSING] '{fn}' not found in script!")

check_file('d:/Script/ENG/app/templates/index.html')
check_file('d:/Script/ENG/mobile/index.html')
