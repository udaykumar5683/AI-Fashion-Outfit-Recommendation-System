
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set dark theme
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 14), facecolor='#0f0f0f')
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis('off')

# Define colors
bg_color = '#0f0f0f'
box_color = '#1a1a1a'
text_color = '#ffffff'
arrow_color = '#ff6b35'  # Orange-red accent
title_color = '#ff6b35'

# Define box properties
box_width = 6.5
box_height = 1.3
box_radius = 0.2

# Helper function to draw a rounded box with text
def draw_box(y, title, content, text_size=10, title_size=12):
    # Box
    rect = patches.FancyBboxPatch(
        (1.75, y), box_width, box_height,
        boxstyle=f"round,pad=0,rounding_size={box_radius}",
        facecolor=box_color, edgecolor='#333333', linewidth=1.5, zorder=2
    )
    ax.add_patch(rect)
    
    # Title
    ax.text(
        5, y + box_height - 0.3, title,
        ha='center', va='center', fontsize=title_size,
        color=title_color, fontweight='bold', zorder=3
    )
    
    # Content
    ax.text(
        5, y + 0.5, content,
        ha='center', va='center', fontsize=text_size,
        color=text_color, zorder=3
    )

# Helper function to draw arrow between boxes
def draw_arrow(y_start, y_end):
    arrow = patches.FancyArrow(
        5, y_start, 0, y_end - y_start,
        width=0.05, head_width=0.2, head_length=0.2,
        length_includes_head=True,
        facecolor=arrow_color, edgecolor=arrow_color,
        linewidth=1.5, zorder=1
    )
    ax.add_patch(arrow)

# Draw each component
draw_box(
    y=12,
    title="User Chat Input",
    content="Natural language request\n(e.g., \"Party outfit for women\")",
    text_size=11
)
draw_arrow(y_start=12, y_end=10.7)

draw_box(
    y=10.2,
    title="Groq LLaMA 3.3 — Intent Parser",
    content="Extracts: gender, occasion, style, age",
    text_size=11
)
draw_arrow(y_start=10.2, y_end=8.9)

draw_box(
    y=8.4,
    title="FashionCLIP Embeddings",
    content="68 products embedded (image + text)\nStored in ChromaDB",
    text_size=11
)
draw_arrow(y_start=8.4, y_end=7.1)

draw_box(
    y=6.6,
    title="Outfit Engine",
    content="Queries ChromaDB for:\nTopwear | Bottomwear | Footwear | Accessory\nFilters by gender + occasion\nPrioritizes 25 curated outfits",
    text_size=10
)
draw_arrow(y_start=6.6, y_end=5.3)

draw_box(
    y=4.8,
    title="Groq LLaMA 3.3 — Reasoning Engine",
    content="Generates stylist explanation\nUses curated stylist_rationale as examples",
    text_size=11
)
draw_arrow(y_start=4.8, y_end=3.5)

draw_box(
    y=3,
    title="Streamlit UI",
    content="Shows outfit cards with images + prices\nChat interface with history",
    text_size=11
)

# Add a small heading at the top
ax.text(
    5, 13.3, "AI Fashion Outfit Recommendation System Architecture",
    ha='center', va='center', fontsize=16,
    color=text_color, fontweight='bold'
)

# Save the figure
plt.tight_layout()
plt.savefig('architecture.png', dpi=150, bbox_inches='tight', facecolor=bg_color)
print("✓ Saved architecture.png!")
plt.close()
