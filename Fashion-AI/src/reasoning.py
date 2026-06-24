import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_reasoning(outfit_dict, intent_dict):
    try:
        # Load outfits for examples
        outfits_df = pd.read_csv("./data/outfits.csv")
        
        # Get matching stylist rationales
        gender = intent_dict.get("gender")
        raw_occasion = intent_dict.get("occasion")
        examples = []
        
        if gender and raw_occasion:
            matching = outfits_df[
                (outfits_df["gender"] == gender) &
                (outfits_df["occasion"].isin([raw_occasion]))
            ]
            examples = matching["stylist_rationale"].dropna().head(4).tolist()
        
        # Build outfit items string
        outfit_items = []
        for role, item in outfit_dict.items():
            if role == "topwear":
                line = f"- Topwear: {item['name']} by {item['brand']} ({item['category_label']})"
            elif role == "bottomwear":
                line = f"- Bottomwear: {item['name']} by {item['brand']}"
            elif role == "footwear":
                line = f"- Footwear: {item['name']} by {item['brand']}"
            elif role == "accessory":
                line = f"- Accessory: {item['name']} by {item['brand']}"
            outfit_items.append(line)
        
        # Build prompt
        system_prompt = """
You are a professional fashion stylist writing for Vogue magazine.

Write exactly 3 sentences explaining why this outfit works.
Each sentence must mention at least one specific item by name.
Be creative, specific, and fashion-forward.
Do NOT use generic phrases like "carefully curated" or "cohesive look"
or "suitable for your needs".
""".strip()
        
        user_prompt = f"""
OCCASION: {raw_occasion}
USER: {gender}, {intent_dict.get('age_group', '20s')}

OUTFIT ITEMS:
{chr(10).join(outfit_items)}

EXAMPLES OF GOOD STYLIST WRITING (match this tone):
{chr(10).join(examples)}

Write the 3-sentence explanation now. Start directly, no preamble:
""".strip()
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating reasoning: {e}")
        return "This outfit combines stylish pieces perfect for your occasion, balancing comfort and elegance with carefully selected items."
