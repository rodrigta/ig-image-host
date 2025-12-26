"""
Caption generation using OpenAI LLM.
"""

from openai import OpenAI
import config


def generate_caption(theme: str, prompt_template: str) -> str:
    """
    Generate an Instagram caption using OpenAI Chat Completions API.
    
    Args:
        theme: The content theme
        prompt_template: The prompt template to use
        
    Returns:
        Generated caption as plain text string
    """
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model=config.CAPTION_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a thoughtful content writer who creates calm, confident, grounded captions with emotional maturity. You avoid hype, hustle culture, and excessive punctuation."
            },
            {
                "role": "user",
                "content": prompt_template
            }
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    caption = response.choices[0].message.content.strip()
    
    # Clean up any unwanted characters or formatting
    caption = caption.replace('"', '').replace('"', '').replace("'", "").replace("'", "")
    caption = caption.replace("!", ".").replace("?", ".")
    
    return caption


def generate_hashtags(theme: str, caption: str, prompt_template: str) -> str:
    """
    Generate Instagram hashtags using OpenAI Chat Completions API.
    
    Args:
        theme: The content theme
        caption: The generated caption
        prompt_template: The prompt template to use
        
    Returns:
        Generated hashtags as a string (space-separated)
    """
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model=config.CAPTION_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a social media expert who generates relevant, effective Instagram hashtags. Return only hashtags separated by spaces, no additional text."
            },
            {
                "role": "user",
                "content": prompt_template
            }
        ],
        temperature=0.8,
        max_tokens=100
    )
    
    hashtags = response.choices[0].message.content.strip()
    
    # Clean up the hashtags - ensure they all start with #
    hashtag_list = []
    for tag in hashtags.split():
        tag = tag.strip()
        if tag and not tag.startswith('#'):
            tag = '#' + tag
        if tag.startswith('#'):
            # Remove any special characters except alphanumeric and underscore
            clean_tag = '#' + ''.join(c for c in tag[1:] if c.isalnum() or c == '_')
            if len(clean_tag) > 1:  # Has to be more than just '#'
                hashtag_list.append(clean_tag)
        elif tag:
            hashtag_list.append('#' + tag)
    
    # Limit to 15 hashtags max
    hashtag_list = hashtag_list[:15]
    
    return ' '.join(hashtag_list)

