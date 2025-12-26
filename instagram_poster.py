"""
Instagram posting functionality using Instagram Graph API (Meta's official API).
"""

import os
import requests
import json
import base64
from typing import Optional
from datetime import datetime
import config


def upload_image_to_facebook(image_path: str, access_token: str, page_id: str) -> Optional[str]:
    """
    Upload image to Facebook to get a URL for Instagram Graph API.
    
    Args:
        image_path: Path to the image file
        access_token: Facebook Page Access Token
        page_id: Facebook Page ID
        
    Returns:
        Published photo ID or None if failed
    """
    url = f"https://graph.facebook.com/v18.0/{page_id}/photos"
    
    with open(image_path, 'rb') as image_file:
        files = {'file': image_file}
        data = {
            'published': 'false',  # Don't publish to Facebook, just upload
            'access_token': access_token
        }
        response = requests.post(url, files=files, data=data)
        
    if response.status_code == 200:
        result = response.json()
        return result.get('id')  # This is the photo ID on Facebook
    else:
        raise Exception(f"Failed to upload image to Facebook: {response.text}")


def create_instagram_media_container(instagram_account_id: str, image_url: str, caption: str, access_token: str) -> str:
    """
    Create an Instagram media container using Facebook Graph API.
    
    Args:
        instagram_account_id: Instagram Business Account ID
        image_url: URL of the image (from GitHub or Facebook upload)
        caption: Caption text for the post
        access_token: Page Access Token with Instagram permissions
        
    Returns:
        Creation ID for publishing
    """
    # Use Facebook Graph API endpoint for Instagram (more reliable)
    url = f"https://graph.facebook.com/v18.0/{instagram_account_id}/media"
    
    params = {
        'image_url': image_url,
        'caption': caption,
        'access_token': access_token
    }
    
    response = requests.post(url, params=params)
    
    if response.status_code == 200:
        result = response.json()
        return result.get('id')  # Creation ID
    else:
        raise Exception(f"Failed to create media container: {response.text}")


def publish_instagram_media(instagram_account_id: str, creation_id: str, access_token: str) -> dict:
    """
    Publish the Instagram media container using Facebook Graph API.
    
    Args:
        instagram_account_id: Instagram Business Account ID
        creation_id: Creation ID from create_instagram_media_container
        access_token: Page Access Token with Instagram permissions
        
    Returns:
        Published media information
    """
    # Use Facebook Graph API endpoint for Instagram (more reliable)
    url = f"https://graph.facebook.com/v18.0/{instagram_account_id}/media_publish"
    
    params = {
        'creation_id': creation_id,
        'access_token': access_token
    }
    
    response = requests.post(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to publish media: {response.text}")


def get_instagram_business_account_id(page_id: str, access_token: str) -> str:
    """
    Get Instagram Business Account ID from Facebook Page ID.
    
    Args:
        page_id: Facebook Page ID
        access_token: Facebook Page Access Token
        
    Returns:
        Instagram Business Account ID
    """
    url = f"https://graph.facebook.com/v18.0/{page_id}"
    
    params = {
        'fields': 'instagram_business_account',
        'access_token': access_token
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        result = response.json()
        instagram_account = result.get('instagram_business_account')
        if instagram_account:
            return instagram_account.get('id')
        else:
            raise Exception("No Instagram Business Account linked to this Facebook Page")
    else:
        raise Exception(f"Failed to get Instagram account: {response.text}")


def get_image_url_from_facebook_photo(photo_id: str, access_token: str) -> str:
    """
    Get the image URL from a Facebook photo ID.
    
    Args:
        photo_id: Facebook Photo ID
        access_token: Facebook Page Access Token
        
    Returns:
        Image URL
    """
    url = f"https://graph.facebook.com/v18.0/{photo_id}"
    
    params = {
        'fields': 'images',
        'access_token': access_token
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        result = response.json()
        images = result.get('images', [])
        if images:
            # Get the largest image
            return max(images, key=lambda x: x.get('width', 0) * x.get('height', 0)).get('source')
        else:
            raise Exception("No images found for photo ID")
    else:
        raise Exception(f"Failed to get image URL: {response.text}")


def get_github_default_branch(username: str, repo: str) -> str:
    """
    Get the default branch name for a GitHub repository.
    
    Args:
        username: GitHub username
        repo: Repository name
        
    Returns:
        Default branch name (usually "main" or "master")
    """
    headers = {
        "Authorization": f"token {config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{username}/{repo}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repo_info = response.json()
        return repo_info.get("default_branch", "main")
    else:
        # Default to "main" if can't determine
        return "main"


def upload_image_to_github(image_path: str, filename: str) -> str:
    """
    Upload image to GitHub repository and return raw URL.
    
    Args:
        image_path: Local path to the image file
        filename: Filename to use in GitHub (will be stored in images/ directory)
        
    Returns:
        Raw GitHub URL of the uploaded image
    """
    if not config.GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN not set in .env file")
    if not config.GITHUB_USERNAME:
        raise ValueError("GITHUB_USERNAME not set in .env file")
    
    repo = config.GITHUB_REPO
    username = config.GITHUB_USERNAME
    
    # Get default branch
    default_branch = get_github_default_branch(username, repo)
    
    # Read image file and encode to base64
    with open(image_path, 'rb') as f:
        image_content = f.read()
        image_base64 = base64.b64encode(image_content).decode('utf-8')
    
    # GitHub API endpoint to create/update file
    # Store images in images/ directory in the repo
    github_path = f"images/{filename}"
    url = f"https://api.github.com/repos/{username}/{repo}/contents/{github_path}"
    
    headers = {
        "Authorization": f"token {config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Commit message
    commit_message = f"Upload image: {filename}"
    
    data = {
        "message": commit_message,
        "content": image_base64,
        "branch": default_branch
    }
    
    # Check if file already exists (to get sha for update)
    response = requests.get(url, headers=headers, params={"ref": default_branch})
    if response.status_code == 200:
        existing_file = response.json()
        data["sha"] = existing_file["sha"]  # Include SHA to update existing file
    
    # Upload file
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code in [200, 201]:
        # Return raw GitHub URL
        raw_url = f"https://raw.githubusercontent.com/{username}/{repo}/{default_branch}/{github_path}"
        return raw_url
    else:
        error_msg = response.text
        if response.status_code == 404:
            raise Exception(f"Repository {username}/{repo} not found. Please create it first or check the repository name.")
        else:
            raise Exception(f"Failed to upload to GitHub: {response.status_code} - {error_msg}")


def get_page_access_token(page_id: str, user_access_token: str) -> str:
    """
    Get Page Access Token from User Access Token.
    
    Args:
        page_id: Facebook Page ID
        user_access_token: User Access Token with pages permissions
        
    Returns:
        Page Access Token
    """
    url = f"https://graph.facebook.com/v18.0/{page_id}"
    params = {
        'fields': 'access_token',
        'access_token': user_access_token
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        result = response.json()
        return result.get('access_token')
    else:
        raise Exception(f"Failed to get page access token: {response.text}")


def upload_to_instagram(image_path: str, caption: str, hashtags: str = "") -> dict:
    """
    Upload an image to Instagram using Instagram Graph API.
    
    Args:
        image_path: Path to the image file
        caption: Caption text for the post
        hashtags: Optional hashtags to append to the caption
        
    Returns:
        Dictionary with upload result information
    """
    if not os.path.exists(image_path):
        raise ValueError(f"Image file not found: {image_path}")
    
    # Check for required credentials
    if not config.INSTAGRAM_ACCESS_TOKEN:
        raise ValueError("INSTAGRAM_ACCESS_TOKEN not set in .env file")
    
    try:
        user_access_token = config.INSTAGRAM_ACCESS_TOKEN
        
        # Get Page Access Token from User Access Token
        if config.FACEBOOK_PAGE_ID:
            print("Getting Page Access Token...")
            page_access_token = get_page_access_token(config.FACEBOOK_PAGE_ID, user_access_token)
            print("✓ Page Access Token obtained")
            
            # Get Instagram Business Account ID from Page (more reliable than hardcoded)
            print("Getting Instagram Business Account ID...")
            instagram_account_id = get_instagram_business_account_id(config.FACEBOOK_PAGE_ID, page_access_token)
            print(f"✓ Instagram Account ID: {instagram_account_id}")
        else:
            raise ValueError("FACEBOOK_PAGE_ID not set in .env file")
        
        # Fallback to configured ID if fetching fails
        if not instagram_account_id:
            instagram_account_id = config.INSTAGRAM_BUSINESS_ACCOUNT_ID or "24947725968239405"
        
        # Combine caption and hashtags
        instagram_caption = caption
        if hashtags:
            instagram_caption = f"{caption}\n\n{hashtags}"
        
        # Get image URL - Try GitHub upload first (doesn't require pages_manage_posts)
        # Fallback to Facebook upload if GitHub not configured
        image_url = None
        
        # Try GitHub upload first (works without pages_manage_posts permission)
        if config.GITHUB_TOKEN and config.GITHUB_USERNAME:
            try:
                print("Uploading image to GitHub...")
                filename = os.path.basename(image_path)
                image_url = upload_image_to_github(image_path, filename)
                print(f"✓ Image uploaded to GitHub: {image_url}")
            except Exception as e:
                print(f"Warning: GitHub upload failed: {str(e)}")
                image_url = None
        
        # Fallback to Facebook upload if GitHub failed or not configured
        if not image_url:
            try:
                print("Uploading image to Facebook...")
                photo_id = upload_image_to_facebook(image_path, page_access_token, config.FACEBOOK_PAGE_ID)
                
                print("Getting image URL...")
                image_url = get_image_url_from_facebook_photo(photo_id, page_access_token)
                print("✓ Image uploaded and URL obtained")
            except Exception as e:
                raise Exception(f"Failed to upload image: {str(e)}")
        
        # Step 3: Create Instagram media container
        # Use Page Access Token for Instagram API (it should work for both Facebook and Instagram)
        print("Creating Instagram media container...")
        creation_id = create_instagram_media_container(
            instagram_account_id, 
            image_url, 
            instagram_caption, 
            page_access_token
        )
        
        # Step 4: Publish the media
        print("Publishing to Instagram...")
        published_media = publish_instagram_media(instagram_account_id, creation_id, page_access_token)
        
        return {
            "success": True,
            "media_id": published_media.get('id'),
            "message": "Image uploaded successfully to Instagram"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to upload to Instagram: {str(e)}"
        }
