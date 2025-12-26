"""
Configuration module for API keys and constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Instagram Graph API Configuration (for business accounts)
# Required credentials for Instagram Graph API:
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")  # Long-lived Page Access Token
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")  # Facebook Page ID linked to Instagram Business Account
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")  # Optional: Will be fetched if not provided

# GitHub Configuration (for image hosting - alternative to Facebook upload)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub Personal Access Token
GITHUB_REPO = os.getenv("GITHUB_REPO", "instagram-images")  # Repository name for storing images
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")  # GitHub username/org name

# Output directories
OUTPUT_DIR = "outputs"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
POSTS_JSON_PATH = os.path.join(OUTPUT_DIR, "posts.json")

# Image generation settings
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1280
IMAGE_SIZE = f"{IMAGE_WIDTH}x{IMAGE_HEIGHT}"

# Model settings
CAPTION_MODEL = "gpt-4o-mini"
IMAGE_MODEL = "dall-e-3"  # Generate at 1024x1792, then resize to 1024x1280

