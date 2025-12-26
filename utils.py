"""
Utility functions for directory management and logging.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

import config


def ensure_output_directories():
    """
    Ensure output directories exist, creating them if necessary.
    """
    os.makedirs(config.IMAGES_DIR, exist_ok=True)


def save_post_log(post_data: Dict[str, Any]):
    """
    Append a post entry to posts.json.
    
    Args:
        post_data: Dictionary containing theme, caption, image_path, and timestamp
    """
    # Ensure directories exist
    ensure_output_directories()
    
    # Load existing posts
    if os.path.exists(config.POSTS_JSON_PATH):
        with open(config.POSTS_JSON_PATH, "r", encoding="utf-8") as f:
            posts = json.load(f)
    else:
        posts = []
    
    # Add new post
    posts.append(post_data)
    
    # Save updated posts
    with open(config.POSTS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)


def generate_image_filename(theme: str) -> str:
    """
    Generate a filename for an image based on theme and timestamp.
    
    Args:
        theme: The content theme
        
    Returns:
        Filename string with .png extension
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_theme = "".join(c for c in theme if c.isalnum() or c in (" ", "-", "_")).strip()
    safe_theme = safe_theme.replace(" ", "_").lower()[:30]
    return f"{safe_theme}_{timestamp}.png"

