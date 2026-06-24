import sys
sys.path.insert(0, "./src")
from src import outfit_engine

# Test with sample intent
test_intent = {
    "gender": "women",
    "occasion": "party",
    "style": "casual",
    "age_group": "20s",
    "key_items": [],
    "is_fashion_query": True
}

print("Testing outfit_engine.get_outfit...")
outfit = outfit_engine.get_outfit(test_intent)
print("✓ Got outfit!")
for role, item in outfit.items():
    print(f"  {role}: {item['name']} by {item['brand']}")

print("\nTest passed!")
