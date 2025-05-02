# meme_engine.py - Image processing logic
from PIL import Image, ImageDraw, ImageFont
import io

def generate_meme(image_bytes, top_text="", bottom_text=""):
    """Generate meme with text overlay"""
    image = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(image)
    
    # Use a default font (or add your own .ttf file)
    try:
        font = ImageFont.truetype("impact.ttf", size=40)
    except:
        font = ImageFont.load_default()
    
    # Calculate text positions
    width, height = image.size
    
    # Draw top text
    if top_text:
        draw.text(
            (width/2, 10), 
            top_text, 
            font=font, 
            fill="white", 
            stroke_width=2, 
            stroke_fill="black",
            anchor="mt"
        )
    
    # Draw bottom text
    if bottom_text:
        draw.text(
            (width/2, height-10), 
            bottom_text, 
            font=font, 
            fill="white", 
            stroke_width=2, 
            stroke_fill="black",
            anchor="mb"
        )
    
    # Save to bytes
    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return output
