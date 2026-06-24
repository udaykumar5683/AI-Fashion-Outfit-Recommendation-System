import streamlit as st
import chromadb
import sys
import os

sys.path.insert(0, os.path.abspath("./src"))

from src import intent_parser, outfit_engine, reasoning

# Page config
st.set_page_config(
    page_title="AI Fashion Assistant",
    page_icon="✨",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0f0f0f;
        color: #ffffff;
    }
    .card {
        background-color: #1a1a1a;
        border-radius: 12px;
        border: 1px solid #2a2a2a;
        padding: 16px;
        margin: 8px 0;
    }
    .category-badge {
        display: inline-block;
        background-color: #3b82f6;
        color: white;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        margin-bottom: 8px;
    }
    .product-name {
        font-weight: bold;
        font-size: 16px;
        margin: 4px 0;
    }
    .product-brand {
        color: #888;
        font-size: 14px;
    }
    .product-price {
        color: #10b981;
        font-size: 18px;
        font-weight: bold;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "profile" not in st.session_state:
    st.session_state.profile = {}

# Sidebar for profile
with st.sidebar:
    st.header("Your Profile")
    st.caption("Tell us about yourself")
    
    gender = st.selectbox("Gender", ["men", "women"], index=0)
    age = st.slider("Age", 16, 60, 25)
    occasion = st.selectbox("Occasion", [
        "casual", "office", "party", "wedding", "beach",
        "festive", "vacation", "sports", "winter", "date"
    ])
    style = st.selectbox("Style Preference", [
        "casual", "smart-casual", "formal", "ethnic", "western"
    ])
    
    if st.button("Update Profile", type="primary"):
        st.session_state.profile = {
            "gender": gender,
            "age": age,
            "occasion": occasion,
            "style": style
        }
        st.success("Profile updated!")

# Main area
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>✨ AI Fashion Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; margin-top: 0; margin-bottom: 32px;'>Powered by FashionCLIP & Groq</p>", unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "outfit" in msg:
            # Display outfit
            st.markdown(f"### Here's your outfit for {msg['occasion']}:")
            roles = list(msg["outfit"].keys())
            cols = st.columns(len(roles))
            for i, role in enumerate(roles):
                item = msg["outfit"][role]
                with cols[i]:
                    st.image("./data/" + item["image"], use_container_width=True)
                    st.markdown(f"<div class='category-badge'>{item['category_label']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='product-name'>{item['name']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='product-brand'>{item['brand']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='product-price'>₹{item['price_inr']:.0f}</div>", unsafe_allow_html=True)
            st.divider()
            st.info(msg["reasoning"])
        else:
            st.write(msg["content"])

# Chat input
if prompt := st.chat_input("What outfit are you looking for?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Process
    with st.spinner("Styling your outfit..."):
        intent = intent_parser.parse_intent(prompt, st.session_state.profile)
        
        if not intent.get("is_fashion_query"):
            response = """I'm your fashion assistant! Ask me things like:
• "I need an outfit for a wedding"
• "Suggest a beach look for men"
• "Party outfit for women"
"""
            with st.chat_message("assistant"):
                st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            outfit = outfit_engine.get_outfit(intent)
            reasoning_text = reasoning.generate_reasoning(outfit, intent)
            
            # Display
            with st.chat_message("assistant"):
                st.markdown(f"### Here's your outfit for {intent.get('occasion', 'your occasion')}:")
                roles = list(outfit.keys())
                cols = st.columns(len(roles))
                for i, role in enumerate(roles):
                    item = outfit[role]
                    with cols[i]:
                        st.image("./data/" + item["image"], use_container_width=True)
                        st.markdown(f"<div class='category-badge'>{item['category_label']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='product-name'>{item['name']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='product-brand'>{item['brand']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='product-price'>₹{item['price_inr']:.0f}</div>", unsafe_allow_html=True)
                st.divider()
                st.info(reasoning_text)
            
            # Save to session state
            st.session_state.messages.append({
                "role": "assistant",
                "outfit": outfit,
                "reasoning": reasoning_text,
                "occasion": intent.get("occasion")
            })

# Initialize ChromaDB
@st.cache_resource
def get_collection():
    client = chromadb.PersistentClient(path="./chroma_db")
    return client.get_or_create_collection(name="fashion_products")

# Call to initialize
get_collection()
