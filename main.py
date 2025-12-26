"""
CLI entry point for Instagram content generation pipeline.
"""

import os
import sys
from datetime import datetime

# Set UTF-8 encoding for stdout to handle emojis and special characters
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import config
import prompts
import caption_generator
import image_generator
import instagram_poster
import utils


def main():
    """Main CLI entry point."""
    # Ensure output directories exist
    utils.ensure_output_directories()
    
    # Get theme from command line argument or prompt user
    if len(sys.argv) > 1:
        theme = " ".join(sys.argv[1:]).strip()
    else:
        print("\n=== Instagram Content Generator ===")
        theme = input("Enter a theme (e.g., 'life motivation', 'sunset travel'): ").strip()
    
    if not theme:
        print("Error: Theme cannot be empty.")
        return
    
    print(f"\nGenerating content for theme: {theme}")
    print("Generating caption...")
    
    # Generate caption
    caption_prompt_text = prompts.caption_prompt(theme)
    caption = caption_generator.generate_caption(theme, caption_prompt_text)
    
    print("Generating hashtags...")
    
    # Generate hashtags
    hashtag_prompt_text = prompts.hashtag_prompt(theme, caption)
    hashtags = caption_generator.generate_hashtags(theme, caption, hashtag_prompt_text)
    
    print("Generating image...")
    
    # Generate image with caption overlay
    image_prompt_text = prompts.image_prompt(theme)
    image_filename = utils.generate_image_filename(theme)
    image_path = os.path.join(config.IMAGES_DIR, image_filename)
    image_generator.generate_image(image_prompt_text, image_path, caption=caption)
    
    # Upload to Instagram if credentials are available
    instagram_result = None
    if config.INSTAGRAM_ACCESS_TOKEN:
        print("Uploading to Instagram...")
        try:
            instagram_result = instagram_poster.upload_to_instagram(image_path, caption, hashtags)
            if instagram_result["success"]:
                print(f"[SUCCESS] Uploaded to Instagram: {instagram_result['message']}")
            else:
                print(f"[WARNING] Instagram upload failed: {instagram_result['message']}")
        except Exception as e:
            print(f"[WARNING] Instagram upload error: {str(e)}")
            instagram_result = {"success": False, "error": str(e)}
    else:
        print("[INFO] Instagram credentials not set - skipping upload")
    
    # Log post data
    post_data = {
        "theme": theme,
        "caption": caption,
        "hashtags": hashtags,
        "image_path": image_path,
        "timestamp": datetime.now().isoformat(),
        "instagram_uploaded": instagram_result["success"] if instagram_result else False,
        "instagram_media_id": instagram_result.get("media_id") if instagram_result and instagram_result.get("success") else None
    }
    utils.save_post_log(post_data)
    
    # Print success summary
    print("\n" + "="*50)
    print("[SUCCESS] Content generated successfully!")
    print(f"Theme: {theme}")
    print(f"Caption: {caption}")
    print(f"Hashtags: {hashtags}")
    print(f"Image saved to: {image_path}")
    if instagram_result and instagram_result.get("success"):
        print(f"Instagram: Uploaded successfully (Media ID: {instagram_result.get('media_id')})")
    print(f"Post logged to: {config.POSTS_JSON_PATH}")
    print("="*50 + "\n")


if __name__ == "__main__":
    main()

