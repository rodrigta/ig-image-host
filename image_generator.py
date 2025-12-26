"""
Image generation using OpenAI image generation API.
"""

import requests
from PIL import Image, ImageDraw, ImageFont
import io
import os
import sys
import textwrap
from openai import OpenAI
import config


def add_text_overlay(image: Image.Image, caption: str) -> Image.Image:
    """
    Add caption text overlay to the image with elegant styling.
    
    Args:
        image: PIL Image object
        caption: Text caption to overlay
        
    Returns:
        PIL Image with text overlay
    """
    # Convert to RGBA for transparency support
    if image.mode != 'RGBA':
        img_with_text = image.convert('RGBA')
    else:
        img_with_text = image.copy()
    
    draw = ImageDraw.Draw(img_with_text)
    
    # Get image dimensions
    width, height = img_with_text.size
    
    # Calculate font size based on image width (approximately 4.5% of width)
    base_font_size = int(width * 0.045)
    if base_font_size < 24:
        base_font_size = 24
    elif base_font_size > 60:
        base_font_size = 60
    
    # Try to load a nice font, fallback to default if not available
    font = None
    try:
        if sys.platform == "win32":
            # Try Calibri first, then Arial
            for font_name in ["calibri.ttf", "arial.ttf", "arialbd.ttf"]:
                font_path = f"C:/Windows/Fonts/{font_name}"
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, base_font_size)
                    break
        elif sys.platform == "darwin":
            font_path = "/Library/Fonts/Arial.ttf"
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, base_font_size)
        else:
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, base_font_size)
    except Exception:
        pass
    
    if font is None:
        # Use default font, but it won't scale well
        try:
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
    
    # Calculate text wrapping - estimate chars per line
    max_chars_per_line = int(width * 0.08)  # Rough estimate
    if max_chars_per_line < 20:
        max_chars_per_line = 20
    wrapped_lines = textwrap.wrap(caption, width=max_chars_per_line, break_long_words=False, break_on_hyphens=False)
    
    # Calculate text dimensions by actually measuring
    line_heights = []
    line_widths = []
    for line in wrapped_lines:
        try:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
        except:
            # Fallback if textbbox fails
            line_width = len(line) * (base_font_size // 2)
            line_height = base_font_size
        line_widths.append(line_width)
        line_heights.append(line_height)
    
    if not line_heights:
        return image
    
    total_text_height = sum(line_heights) + (len(wrapped_lines) - 1) * int(base_font_size * 0.3)
    max_line_width = max(line_widths) if line_widths else width * 0.8
    
    # Position: Center horizontally, lower third vertically
    text_x = int((width - max_line_width) // 2)
    text_y = int(height * 0.62)
    
    # Add semi-transparent background for readability
    padding = int(base_font_size * 0.6)
    bg_x1 = max(0, text_x - padding)
    bg_y1 = max(0, text_y - padding)
    bg_x2 = min(width, text_x + int(max_line_width) + padding)
    bg_y2 = min(height, text_y + total_text_height + padding)
    
    # Draw semi-transparent background
    overlay = Image.new('RGBA', (bg_x2 - bg_x1, bg_y2 - bg_y1), (0, 0, 0, 140))
    img_with_text.paste(overlay, (bg_x1, bg_y1), overlay)
    draw = ImageDraw.Draw(img_with_text)
    
    # Draw text (white color for contrast)
    current_y = text_y
    for i, line in enumerate(wrapped_lines):
        line_x = int((width - line_widths[i]) // 2)  # Center each line
        try:
            draw.text((line_x, current_y), line, fill=(255, 255, 255, 255), font=font)
        except:
            # Fallback for systems with font issues
            draw.text((line_x, current_y), line, fill=(255, 255, 255, 255))
        current_y += line_heights[i] + int(base_font_size * 0.25)
    
    # Convert back to RGB for saving
    return img_with_text.convert('RGB')


def generate_image(prompt: str, output_path: str, caption: str = None) -> str:
    """
    Generate an image using OpenAI image generation API and save it locally.
    DALL-E 3 doesn't support 1024x1280 directly, so we generate at 1024x1792
    and resize to the target dimensions. Optionally adds caption text overlay.
    
    Args:
        prompt: The image generation prompt
        output_path: Full path where the image should be saved
        caption: Optional caption text to overlay on the image
        
    Returns:
        The path where the image was saved
    """
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    # DALL-E 3 supports 1024x1792 (portrait), generate at that size
    response = client.images.generate(
        model=config.IMAGE_MODEL,
        prompt=prompt,
        size="1024x1792",
        quality="standard",
        n=1,
    )
    
    image_url = response.data[0].url
    
    # Download the image
    img_response = requests.get(image_url, timeout=30)
    img_response.raise_for_status()
    
    # Open image and resize to target dimensions (1024x1280)
    image = Image.open(io.BytesIO(img_response.content))
    image_resized = image.resize((config.IMAGE_WIDTH, config.IMAGE_HEIGHT), Image.Resampling.LANCZOS)
    
    # Add caption overlay if provided
    if caption:
        image_resized = add_text_overlay(image_resized, caption)
    
    # Save the final image
    image_resized.save(output_path, "PNG")
    
    return output_path

