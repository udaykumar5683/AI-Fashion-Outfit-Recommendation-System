# AI Fashion Outfit Recommendation System

An intelligent AI-powered fashion outfit recommendation system that uses FashionCLIP for product embeddings and Groq LLaMA 3.3 for natural language understanding and reasoning.

## Features

- **Natural Language Query**: Ask for outfit recommendations in plain English
- **Personalized Profile**: Customize based on gender, age, occasion, and style preferences
- **AI Stylist**: Powered by Groq LLaMA 3.3 for intent parsing and reasoning
- **FashionCLIP Embeddings**: Semantic product understanding using CLIP
- **ChromaDB Vector Search**: Fast similarity search across products
- **Curated Products**: 68 products from Ajio, Myntra, and Nykaa
- **Outfit Curation**: Intelligent combination of Topwear, Bottomwear, Footwear, and Accessories

## Tech Stack

- **Frontend**: Streamlit
- **LLM**: Groq (LLaMA 3.3)
- **Embeddings**: FashionCLIP
- **Vector Database**: ChromaDB
- **Data Processing**: Pandas, NumPy
- **Computer Vision**: PyTorch, TorchVision

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   cd Fashion-AI
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   cd Fashion-AI
   streamlit run app.py
   ```
2. Open http://localhost:8501 in your browser
3. Update your profile in the sidebar
4. Ask for outfit recommendations in the chat interface

## Project Structure

```
Fashion/
├── Fashion-AI/
│   ├── app.py                 # Main Streamlit application
│   ├── requirements.txt       # Python dependencies
│   ├── chroma_db/             # ChromaDB vector storage
│   ├── data/                  # Datasets and product images
│   │   ├── products.csv       # 68 fashion products
│   │   ├── outfits.csv        # 25 curated outfits
│   │   └── images/            # Product images from Ajio, Myntra, Nykaa
│   └── src/                   # Core modules
│       ├── intent_parser.py   # NLP intent extraction
│       ├── outfit_engine.py   # Outfit recommendation logic
│       ├── reasoning.py       # Stylist explanation generation
│       └── embed.py           # FashionCLIP embeddings
└── *.ipynb                    # Exploratory notebooks
```

## Architecture

The system uses a multi-agent architecture:
1. **Intent Parser**: Extracts fashion preferences and occasion from user input
2. **Outfit Engine**: Queries ChromaDB for complementary products across categories
3. **Reasoning Engine**: Generates stylist-like explanations for the recommended outfits

## License

MIT License
