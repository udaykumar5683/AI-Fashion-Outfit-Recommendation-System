import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def parse_intent(user_message, profile=None):
    try:
        system_prompt = """
You are a fashion intent parser. Extract information from the user message.

Return ONLY a valid JSON object, no other text, no markdown:
{{
  "gender": "men or women (use profile gender if message doesn't mention)",
  "occasion": "one of: party/office/casual/wedding/beach/festive/vacation/winter/sports/date/interview/dinner or null",
  "style": "formal/smart-casual/casual/ethnic/western or null",
  "age_group": "teen/20s/30s/40s+ or null",
  "key_items": [],
  "is_fashion_query": true or false
}}

Occasion mapping rules:
- beach/pool/sea/shore → "beach"
- interview/job/work meeting → "interview"
- wedding/marriage/shaadi/reception → "wedding"
- vacation/holiday/travel/trip → "vacation"
- party/club/night out/celebration → "party"
- dinner/date/romantic → "date"
- office/work/professional/business → "office"
- festival/diwali/eid/puja/holi → "festive"
- gym/workout/running/sports → "sports"
- cold/snow/winter → "winter"

Set is_fashion_query to false if user is asking about something
completely unrelated to fashion or outfits (like sleep, food, weather).
""".strip()
        
        user_prompt = f"""
User message: "{user_message}"
User profile (use as fallback if message doesn't specify): {profile}
""".strip()
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=500
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Clean up response
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        
        result = json.loads(result_text.strip())
        
        if not result.get("is_fashion_query"):
            return {"is_fashion_query": False}
        
        # Fallback to profile gender
        if profile and not result.get("gender"):
            result["gender"] = profile.get("gender")
        
        return result
    except Exception as e:
        print(f"Error parsing intent: {e}")
        return {"is_fashion_query": False}
