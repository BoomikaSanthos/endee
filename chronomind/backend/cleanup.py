import re
import sys

filepath = 'main.py'

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove all separator lines containing # ─────
    content = re.sub(r'^# ─+.*$', '', content, flags=re.MULTILINE)
    
    # Remove empty lines that were left behind
    content = re.sub(r'^\s*$', '\n', content, flags=re.MULTILINE)
    content = re.sub(r'\n{3,}', '\n\n', content)

    # Remove `response_model=...` inside @app.post, @app.get, @app.delete decorators
    content = re.sub(r'^\s*response_model=\w+,\s*\n', '', content, flags=re.MULTILINE)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully cleaned up main.py")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
