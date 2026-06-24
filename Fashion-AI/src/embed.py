import pandas as pd
import chromadb
import numpy as np
import os
from pathlib import Path
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

# Set base directory
BASE_DIR = Path(__file__).resolve().parent.parent

def main():
    # Load products
    df = pd.read_csv(BASE_DIR / "data" / "products.csv")
    
    # Initialize CLIP model and processor
    model_name = "patrickjohncyh/fashion-clip"
    model = CLIPModel.from_pretrained(model_name)
    processor = CLIPProcessor.from_pretrained(model_name)
    
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path=str(BASE_DIR / "chroma_db"))
    
    # Delete existing collection if it exists (to ensure fresh start)
    try:
        client.delete_collection(name="fashion_products")
        print("Deleted existing collection for fresh start")
    except:
        pass  # Collection doesn't exist yet
        
    collection = client.create_collection(name="fashion_products")
    
    # Process each product
    ids = []
    embeddings = []
    metadatas = []
    
    for idx, row in df.iterrows():
        # Build image path
        img_path = BASE_DIR / "data" / row["image"]
        image = None
        if img_path.exists():
            try:
                image = Image.open(img_path).convert("RGB")
            except Exception as e:
                print(f"Warning: Could not load image {img_path}: {e}")
        
        # Build text (truncated to avoid max length issues)
        text = f"{row['name']} {row['category_label']} {row['occasion']} {row['tags']}"
        text = text[:200]  # Truncate to keep it short
        
        # Get embedding
        if image:
            inputs = processor(text=[text], images=[image], return_tensors="pt", padding=True, truncation=True)
            outputs = model(**inputs)
            # Average image and text embeddings
            img_emb = outputs.image_embeds[0].detach().numpy()
            txt_emb = outputs.text_embeds[0].detach().numpy()
            embedding = (img_emb + txt_emb) / 2
        else:
            inputs = processor(text=[text], return_tensors="pt", padding=True, truncation=True)
            outputs = model.get_text_features(**inputs)
            embedding = outputs[0].detach().numpy()
        
        # Normalize embedding
        embedding = embedding / np.linalg.norm(embedding, ord=2, keepdims=True)
        
        # Prepare metadata
        metadata = {
            "id": str(row["id"]),
            "name": str(row["name"]),
            "brand": str(row["brand"]),
            "price_inr": float(row["price_inr"]) if pd.notna(row["price_inr"]) else 0.0,
            "category_label": str(row["category_label"]),
            "gender": str(row["gender"]),
            "occasion": str(row["occasion"]),
            "wear_type": str(row["wear_type"]),
            "tags": str(row["tags"]),
            "image": str(row["image"])
        }
        
        ids.append(str(row["id"]))
        embeddings.append(embedding.tolist())
        metadatas.append(metadata)
        
        # Print progress
        if (idx + 1) % 10 == 0:
            print(f"Processed {idx + 1}/{len(df)} products")
    
    # Add to collection
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    print(f"Done! Embedded {len(ids)} products")

if __name__ == "__main__":
    main()
