import pandas as pd
import chromadb
from pathlib import Path

# Set up base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# OCCASION_MAP maps user-facing occasions to dataset occasions
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

# ROLE_CATEGORIES defines what categories fall into each role
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

# OCCASION_PREFERRED_CATEGORIES prioritizes categories for each occasion
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

# ONE_PIECE_CATEGORIES are categories that don't need bottomwear
ONE_PIECE_CATEGORIES = [
    "Party Dresses", "Wedding Sarees", "Sharara Sets", "Casual Dresses",
    "Maxi Dresses", "Co Ord Sets", "Salwar Suits"
]

# BEACH_EXCLUSIONS are categories to exclude for beach occasions
BEACH_EXCLUSIONS = [
    "Formal Shirts", "Blazers", "Sherwanis", "Nehru Jackets", "Long Coats",
    "Wedding Sarees", "Suits", "Formal Shoes", "Heels", "Boots"
]

# Initialize ChromaDB
client = chromadb.PersistentClient(path=str(BASE_DIR / "chroma_db"))
collection = client.get_or_create_collection(name="fashion_products")

# Load products data for fallback outfit building
products_df = pd.read_csv(BASE_DIR / "data" / "products.csv")

# Load curated outfits data
outfits_df = pd.read_csv(BASE_DIR / "data" / "outfits.csv")


def get_outfit(intent_dict):
    """
    Generate a complete outfit recommendation based on user intent.
    
    Args:
        intent_dict: Dictionary containing user intent with keys:
            - gender: 'men' or 'women'
            - occasion: The occasion for the outfit
            - style: Optional style preference
            
    Returns:
        Dictionary with outfit items organized by role
    """
    gender = intent_dict.get("gender")
    raw_occasion = intent_dict.get("occasion")
    db_occasions = OCCASION_MAP.get(raw_occasion, ["casual"])
    
    print(f"DEBUG: Intent received - gender: {gender}, occasion: {raw_occasion}")
    print(f"DEBUG: DB occasions to check: {db_occasions}")
    
    # First try to use curated outfits
    curated_outfit = get_curated_outfit(gender, raw_occasion, db_occasions)
    if curated_outfit:
        print(f"DEBUG: Using curated outfit: {list(curated_outfit.keys())}")
        return curated_outfit
    
    print(f"DEBUG: No curated outfit found, building from products")
    
    # Fall back to building outfit from products
    outfit = build_outfit_from_products(gender, raw_occasion, db_occasions)
    print(f"DEBUG: Built outfit with items: {list(outfit.keys())}")
    
    return outfit


def get_curated_outfit(gender, raw_occasion, db_occasions):
    """
    Try to find a suitable curated outfit.
    
    Args:
        gender: User's gender
        raw_occasion: Original user occasion
        db_occasions: List of dataset occasions to match
        
    Returns:
        Curated outfit dict if found, None otherwise
    """
    try:
        matching_outfits = outfits_df[
            (outfits_df["gender"] == gender) &
            (outfits_df["occasion"].isin(db_occasions))
        ]
        
        print(f"DEBUG: Found {len(matching_outfits)} matching curated outfits")
        
        if len(matching_outfits) == 0:
            return None
        
        # Pick the first matching outfit
        outfit_row = matching_outfits.iloc[0]
        
        # Build outfit from the curated outfit
        outfit = {}
        
        # Map the outfit columns to roles
        role_map = {
            "hero_id": "topwear",
            "second_id": "bottomwear",
            "layer_id": "topwear",  # Layer goes under topwear
            "footwear_id": "footwear",
            "accessory_1_id": "accessory",
            "accessory_2_id": "accessory"
        }
        
        for col, role in role_map.items():
            product_id = outfit_row.get(col)
            if pd.notna(product_id):
                product = get_product_by_id(str(product_id))
                if product:
                    # Only add one item per role
                    if role not in outfit:
                        outfit[role] = product
        
        print(f"DEBUG: Curated outfit built with items: {list(outfit.keys())}")
        return outfit
        
    except Exception as e:
        print(f"DEBUG: Error getting curated outfit: {e}")
        return None


def build_outfit_from_products(gender, raw_occasion, db_occasions):
    """
    Build an outfit from scratch using product database.
    
    Args:
        gender: User's gender
        raw_occasion: Original user occasion
        db_occasions: List of dataset occasions to match
        
    Returns:
        Built outfit dict
    """
    outfit = {}
    curated_ids = []
    
    # Try to find one curated product as hero
    try:
        matching_curated = outfits_df[
            (outfits_df["gender"] == gender) &
            (outfits_df["occasion"].isin(db_occasions))
        ]
        for _, row in matching_curated.iterrows():
            for col in ["hero_id", "second_id", "layer_id", "footwear_id", "accessory_1_id", "accessory_2_id"]:
                if pd.notna(row[col]):
                    curated_ids.append(str(row[col]))
        curated_ids = list(set(curated_ids))
        print(f"DEBUG: Found {len(curated_ids)} curated product IDs")
    except Exception as e:
        print(f"DEBUG: Error loading curated product IDs: {e}")
    
    # Get each role item
    roles = ["topwear", "bottomwear", "footwear", "accessory"]
    for role in roles:
        product = query_for_role(role, gender, raw_occasion, db_occasions, curated_ids)
        if product:
            outfit[role] = product
    
    # Skip bottomwear if we have a one-piece topwear
    if "topwear" in outfit and outfit["topwear"]["category_label"] in ONE_PIECE_CATEGORIES:
        if "bottomwear" in outfit:
            del outfit["bottomwear"]
        print("DEBUG: Removed bottomwear since topwear is one-piece")
    
    return outfit


def query_for_role(role, gender, raw_occasion, db_occasions, curated_ids):
    """
    Query ChromaDB for a product matching the given role and criteria.
    
    Args:
        role: Role to query (topwear, bottomwear, etc.)
        gender: User's gender
        raw_occasion: Original user occasion
        db_occasions: List of dataset occasions to match
        curated_ids: List of curated product IDs to prioritize
        
    Returns:
        Product dict if found, None otherwise
    """
    try:
        # Get preferred categories for this occasion
        pref_cats = []
        if raw_occasion in OCCASION_PREFERRED_CATEGORIES:
            pref_cats = OCCASION_PREFERRED_CATEGORIES[raw_occasion].get(role, [])
        
        # Define query strategies in priority order
        strategies = []
        
        # Strategy 1: Preferred categories + gender + occasion
        if pref_cats:
            strategies.append({
                "categories": pref_cats,
                "gender": gender,
                "occasions": db_occasions
            })
        
        # Strategy 2: Preferred categories + gender
        if pref_cats:
            strategies.append({
                "categories": pref_cats,
                "gender": gender,
                "occasions": None
            })
        
        # Strategy 3: All role categories + gender + occasion
        strategies.append({
            "categories": ROLE_CATEGORIES[role],
            "gender": gender,
            "occasions": db_occasions
        })
        
        # Strategy 4: All role categories + gender
        strategies.append({
            "categories": ROLE_CATEGORIES[role],
            "gender": gender,
            "occasions": None
        })
        
        # Strategy 5: All role categories, any gender (skip for bottomwear)
        if role != "bottomwear":
            strategies.append({
                "categories": ROLE_CATEGORIES[role],
                "gender": None,
                "occasions": None
            })
        
        # Try each strategy in order
        for i, strategy in enumerate(strategies):
            print(f"DEBUG: Trying strategy {i+1} for {role}: {strategy}")
            product = try_query_strategy(strategy, raw_occasion, curated_ids)
            if product:
                print(f"DEBUG: Found product with strategy {i+1} for {role}: {product['name']}")
                return product
        
        print(f"DEBUG: No product found for role {role}")
        return None
        
    except Exception as e:
        print(f"DEBUG: Error querying for role {role}: {e}")
        import traceback
        traceback.print_exc()
        return None


def try_query_strategy(strategy, raw_occasion, curated_ids):
    """
    Try a single query strategy.
    
    Args:
        strategy: Query strategy dict
        raw_occasion: Original user occasion
        curated_ids: List of curated product IDs to prioritize
        
    Returns:
        Product dict if found, None otherwise
    """
    try:
        # Build where conditions
        where_conditions = []
        
        # Category condition
        where_conditions.append({"category_label": {"$in": strategy["categories"]}})
        
        # Gender condition
        if strategy["gender"]:
            where_conditions.append({"gender": strategy["gender"]})
        
        # Occasion condition
        if strategy["occasions"]:
            where_conditions.append({"occasion": {"$in": strategy["occasions"]}})
        
        # Combine conditions
        where_filter = {"$and": where_conditions} if len(where_conditions) > 1 else where_conditions[0]
        
        # Execute query
        results = collection.get(
            where=where_filter,
            include=["metadatas"]
        )
        
        if not results["ids"]:
            return None
        
        # Process products
        products = []
        for i in range(len(results["ids"])):
            product = {
                "id": results["ids"][i],
                **results["metadatas"][i]
            }
            
            # Apply exclusions
            if raw_occasion == "beach" and product["category_label"] in BEACH_EXCLUSIONS:
                continue
                
            products.append(product)
        
        if not products:
            return None
        
        # Prioritize curated items
        products_sorted = sorted(
            products,
            key=lambda p: 0 if p["id"] in curated_ids else 1
        )
        
        return products_sorted[0]
        
    except Exception as e:
        print(f"DEBUG: Error in query strategy: {e}")
        return None


def get_product_by_id(product_id):
    """
    Get a product by its ID from the products dataframe.
    
    Args:
        product_id: Product ID string
        
    Returns:
        Product dict if found, None otherwise
    """
    try:
        # Find product in dataframe
        product_row = products_df[products_df["id"] == product_id]
        if len(product_row) == 0:
            print(f"DEBUG: Product {product_id} not found in CSV")
            return None
        
        # Convert to dict
        product = product_row.iloc[0].to_dict()
        
        # Ensure numeric fields are correct type
        product["price_inr"] = float(product["price_inr"]) if pd.notna(product["price_inr"]) else 0.0
        
        return product
        
    except Exception as e:
        print(f"DEBUG: Error getting product by ID {product_id}: {e}")
        return None
