import pandas as pd
import chromadb
from pathlib import Path

OCCASION_MAP = {
    "beach": ["vacation", "casual", "sports"],
    "office": ["office"],
    "interview": ["office"],
    "party": ["party", "festive"],
    "wedding": ["wedding", "festive"],
    "date": ["party", "casual"],
    "casual": ["casual", "vacation"],
    "formal": ["office", "wedding"],
    "festive": ["festive", "wedding", "party"],
    "vacation": ["vacation", "casual"],
    "winter": ["winter", "casual"],
    "sports": ["sports", "casual"],
    "dinner": ["party", "casual"]
}

ROLE_CATEGORIES = {
    "topwear": [
        "Formal Shirts", "Sweatshirts", "Linen Shirts", "Sherwanis",
        "Party Dresses", "Wedding Sarees", "Sharara Sets", "Casual Shirts",
        "Party Shirts", "Tshirts", "Polo Tshirts", "Kurta Sets",
        "Nehru Jackets", "Casual Dresses", "Activewear", "Denim Jackets",
        "Sweaters", "Tops", "Maxi Dresses", "Co Ord Sets", "Salwar Suits",
        "Long Coats", "Blazers", "Suits"
    ],
    "bottomwear": [
        "Track Pants", "Trousers", "Jeans", "Chinos",
        "Shorts", "Skirts", "Leggings"
    ],
    "footwear": [
        "Running Shoes", "Sneakers", "Ethnic Footwear", "Heels",
        "Boots", "Flats", "Formal Shoes", "Loafers", "Sandals"
    ],
    "accessory": [
        "Necklaces", "Clutches", "Handbags", "Earrings",
        "Sunglasses", "Watches", "Caps"
    ]
}

OCCASION_PREFERRED_CATEGORIES = {
    "beach": {
        "topwear": ["Tshirts", "Polo Tshirts", "Casual Shirts", "Activewear", "Sweatshirts"],
        "bottomwear": ["Shorts", "Jeans", "Track Pants"],
        "footwear": ["Sandals", "Sneakers", "Running Shoes", "Flats"],
        "accessory": ["Sunglasses", "Caps", "Watches"]
    },
    "office": {
        "topwear": ["Formal Shirts", "Blazers", "Linen Shirts", "Suits", "Long Coats", "Tops"],
        "bottomwear": ["Trousers", "Chinos", "Jeans"],
        "footwear": ["Formal Shoes", "Loafers", "Heels", "Flats"],
        "accessory": ["Watches", "Handbags"]
    },
    "interview": {
        "topwear": ["Formal Shirts", "Blazers", "Suits", "Linen Shirts", "Tops"],
        "bottomwear": ["Trousers", "Chinos"],
        "footwear": ["Formal Shoes", "Loafers", "Heels"],
        "accessory": ["Watches", "Handbags"]
    },
    "party": {
        "topwear": ["Party Dresses", "Casual Dresses", "Maxi Dresses", "Co Ord Sets", "Party Shirts", "Tops"],
        "bottomwear": ["Skirts", "Trousers", "Jeans"],
        "footwear": ["Heels", "Boots", "Sneakers", "Sandals"],
        "accessory": ["Clutches", "Necklaces", "Handbags", "Earrings"]
    },
    "wedding": {
        "topwear": ["Wedding Sarees", "Sharara Sets", "Kurta Sets", "Sherwanis", "Nehru Jackets", "Salwar Suits"],
        "bottomwear": ["Trousers", "Chinos"],
        "footwear": ["Heels", "Ethnic Footwear", "Formal Shoes"],
        "accessory": ["Necklaces", "Clutches", "Handbags", "Earrings"]
    },
    "festive": {
        "topwear": ["Kurta Sets", "Sharara Sets", "Salwar Suits", "Co Ord Sets", "Party Shirts", "Nehru Jackets"],
        "bottomwear": ["Trousers", "Skirts", "Chinos"],
        "footwear": ["Ethnic Footwear", "Heels", "Sandals"],
        "accessory": ["Necklaces", "Clutches", "Earrings"]
    },
    "casual": {
        "topwear": ["Tshirts", "Casual Shirts", "Sweatshirts", "Tops", "Denim Jackets", "Sweaters", "Polo Tshirts"],
        "bottomwear": ["Jeans", "Chinos", "Shorts", "Track Pants"],
        "footwear": ["Sneakers", "Loafers", "Sandals", "Flats"],
        "accessory": ["Watches", "Caps", "Sunglasses", "Handbags"]
    },
    "vacation": {
        "topwear": ["Casual Shirts", "Tshirts", "Maxi Dresses", "Co Ord Sets", "Tops", "Polo Tshirts"],
        "bottomwear": ["Shorts", "Jeans", "Skirts"],
        "footwear": ["Sandals", "Sneakers", "Flats"],
        "accessory": ["Sunglasses", "Handbags", "Caps"]
    },
    "date": {
        "topwear": ["Casual Shirts", "Tops", "Maxi Dresses", "Co Ord Sets", "Party Dresses", "Linen Shirts"],
        "bottomwear": ["Jeans", "Chinos", "Skirts", "Trousers"],
        "footwear": ["Loafers", "Heels", "Sneakers", "Sandals", "Boots"],
        "accessory": ["Watches", "Necklaces", "Handbags", "Clutches"]
    },
    "winter": {
        "topwear": ["Sweaters", "Long Coats", "Sweatshirts", "Blazers", "Denim Jackets"],
        "bottomwear": ["Jeans", "Trousers", "Chinos"],
        "footwear": ["Boots", "Loafers", "Formal Shoes"],
        "accessory": ["Watches", "Handbags", "Caps"]
    },
    "sports": {
        "topwear": ["Activewear", "Tshirts", "Sweatshirts"],
        "bottomwear": ["Track Pants", "Shorts", "Leggings"],
        "footwear": ["Running Shoes", "Sneakers"],
        "accessory": ["Caps", "Watches"]
    }
}

ONE_PIECE_CATEGORIES = [
    "Party Dresses", "Wedding Sarees", "Sharara Sets", "Casual Dresses",
    "Maxi Dresses", "Co Ord Sets", "Salwar Suits"
]

BEACH_EXCLUSIONS = [
    "Formal Shirts", "Blazers", "Sherwanis", "Nehru Jackets", "Long Coats",
    "Wedding Sarees", "Suits", "Formal Shoes", "Heels", "Boots"
]

# Set base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize ChromaDB
client = chromadb.PersistentClient(path=str(BASE_DIR / "chroma_db"))
collection = client.get_or_create_collection(name="fashion_products")

def get_outfit(intent_dict):
    gender = intent_dict.get("gender")
    raw_occasion = intent_dict.get("occasion")
    db_occasions = OCCASION_MAP.get(raw_occasion, ["casual"])
    
    # Load curated outfits
    outfits_df = pd.read_csv(BASE_DIR / "data" / "outfits.csv")
    curated_ids = []
    if gender and raw_occasion:
        matching_outfits = outfits_df[
            (outfits_df["gender"] == gender) &
            (outfits_df["occasion"].isin(db_occasions))
        ]
        for _, row in matching_outfits.iterrows():
            for col in ["hero_id", "second_id", "layer_id", "footwear_id", "accessory_1_id", "accessory_2_id"]:
                if pd.notna(row[col]):
                    curated_ids.append(str(row[col]))
    curated_ids = list(set(curated_ids))
    
    # Query each role
    outfit = {}
    roles = ["topwear", "bottomwear", "footwear", "accessory"]
    for role in roles:
        product = query_for_role(role, gender, raw_occasion, db_occasions, curated_ids)
        if product:
            outfit[role] = product
    
    # Skip bottomwear if one-piece
    if "topwear" in outfit and outfit["topwear"]["category_label"] in ONE_PIECE_CATEGORIES:
        if "bottomwear" in outfit:
            del outfit["bottomwear"]
    
    return outfit

def query_for_role(role, gender, raw_occasion, db_occasions, curated_ids):
    strategies = []
    
    # Strategy 1: preferred categories + gender + occasion
    if raw_occasion in OCCASION_PREFERRED_CATEGORIES:
        pref_cats = OCCASION_PREFERRED_CATEGORIES[raw_occasion].get(role, [])
        if pref_cats:
            strategies.append({
                "categories": pref_cats,
                "gender": gender,
                "occasions": db_occasions
            })
    
    # Strategy 2: preferred categories + gender
    if raw_occasion in OCCASION_PREFERRED_CATEGORIES:
        pref_cats = OCCASION_PREFERRED_CATEGORIES[raw_occasion].get(role, [])
        if pref_cats:
            strategies.append({
                "categories": pref_cats,
                "gender": gender,
                "occasions": None
            })
    
    # Strategy 3: all role categories + gender + occasion
    strategies.append({
        "categories": ROLE_CATEGORIES[role],
        "gender": gender,
        "occasions": db_occasions
    })
    
    # Strategy 4: all role categories + gender
    strategies.append({
        "categories": ROLE_CATEGORIES[role],
        "gender": gender,
        "occasions": None
    })
    
    # Strategy 5: all role categories (skip for bottomwear)
    if role != "bottomwear":
        strategies.append({
            "categories": ROLE_CATEGORIES[role],
            "gender": None,
            "occasions": None
        })
    
    for strategy in strategies:
        # Build proper ChromaDB where filter with $and
        conditions = []
        
        # Category condition
        conditions.append({"category_label": {"$in": strategy["categories"]}})
        
        # Gender condition
        if strategy["gender"]:
            conditions.append({"gender": strategy["gender"]})
            
        # Occasion condition
        if strategy["occasions"]:
            conditions.append({"occasion": {"$in": strategy["occasions"]}})
            
        # Combine with $and
        where_filter = {"$and": conditions} if len(conditions) > 1 else conditions[0]
        
        try:
            # First, just get all products matching the where filter using get()
            results = collection.get(
                where=where_filter,
                include=["metadatas"]
            )
            
            if not results["ids"]:
                continue
                
            # Process results
            products = []
            for i in range(len(results["ids"])):
                product = {
                    "id": results["ids"][i],
                    **results["metadatas"][i]
                }
                # Exclusions for beach
                if raw_occasion == "beach" and product["category_label"] in BEACH_EXCLUSIONS:
                    continue
                products.append(product)
            
            if not products:
                continue
            
            # Prioritize curated items
            products_sorted = sorted(
                products,
                key=lambda p: 0 if p["id"] in curated_ids else 1
            )
            
            return products_sorted[0]
        except Exception as e:
            print(f"Error querying {role}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    return None
