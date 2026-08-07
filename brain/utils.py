import re
import hashlib

def validate_and_clean_input(raw_input):
    text = raw_input.strip()
    
    # Reject empty inputs or UI prompt echoes
    if not text or "Enter Swarm Mission Topic" in text:
        return None
        
    return text

def generate_tool_name(topic):
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', topic)
    words = [w.lower() for w in clean_text.split() if w.lower() not in ['build', 'a', 'an', 'the', 'engine', 'tool', 'design', 'create']]
    
    # Take at most 3 core keywords
    short_words = words[:3] if words else ["utility"]
    base_slug = "_".join(short_words)[:20]
    
    # Append unique 6-char hash to prevent collision
    short_hash = hashlib.md5(topic.encode()).hexdigest()[:6]
    return f"auto_{base_slug}_{short_hash}.py"
