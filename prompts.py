"""
Prompt definitions for caption and image generation.
"""


def image_prompt(theme: str) -> str:
    """
    Generate a prompt for image generation based on a theme.
    
    Style emphasizes: cinematic, minimalist, premium photography,
    soft golden hour lighting. Conveys calm confidence and quiet ambition.
    
    Args:
        theme: The content theme (e.g., "life motivation", "sunset travel")
        
    Returns:
        Formatted prompt string for image generation
    """
    return f"""Create a cinematic, minimalist, premium professional photography image inspired by the theme: {theme}.

Style requirements:
- Cinematic composition with soft golden hour lighting
- Minimalist aesthetic, clean and uncluttered
- Premium professional photography look
- Convey calm confidence, quiet ambition, and peaceful abundance
- Natural, grounded atmosphere
- No text, no logos, no watermarks
- No surreal or fantastical elements
- Realistic, tasteful imagery"""


def caption_prompt(theme: str) -> str:
    """
    Generate a prompt for caption generation based on a theme.
    
    Style emphasizes: calm, confident, grounded, emotionally mature tone.
    Non-hype, non-hustle approach with quiet ambition.
    
    Args:
        theme: The content theme (e.g., "life motivation", "sunset travel")
        
    Returns:
        Formatted prompt string for caption generation
    """
    return f"""Write a short Instagram caption (1-2 lines maximum) inspired by the theme: {theme}.

Tone requirements:
- Calm and confident
- Grounded and emotionally mature
- Quiet ambition, peaceful abundance
- Non-hype, non-hustle energy
- No hashtags
- No emojis, or maximum one subtle emoji
- No quotation marks
- No exclamation marks
- Plain text only

Write the caption now:"""


def hashtag_prompt(theme: str, caption: str) -> str:
    """
    Generate a prompt for hashtag generation based on theme and caption.
    
    Args:
        theme: The content theme (e.g., "life motivation", "sunset travel")
        caption: The generated caption text
        
    Returns:
        Formatted prompt string for hashtag generation
    """
    return f"""Generate 10-15 relevant Instagram hashtags for a post with the following theme and caption:

Theme: {theme}
Caption: {caption}

Requirements:
- Generate 10-15 hashtags maximum
- Mix of popular and niche hashtags
- Relevant to the theme and caption
- Include motivational, inspirational, lifestyle, or photography-related tags as appropriate
- Return ONLY the hashtags separated by spaces, no other text
- Format: #hashtag1 #hashtag2 #hashtag3 etc.

Generate the hashtags now:"""

