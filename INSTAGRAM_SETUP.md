# Instagram Graph API Setup Guide

This application uses Instagram Graph API (Meta's official API) to post content to Instagram Business accounts.

## Required Credentials

You'll need the following credentials in your `.env` file:

### 1. INSTAGRAM_ACCESS_TOKEN
- A **long-lived Page Access Token** with the following permissions:
  - `instagram_basic`
  - `instagram_content_publish`
  - `pages_read_engagement`
  - `pages_manage_posts`

### 2. FACEBOOK_PAGE_ID
- The ID of your Facebook Page that is linked to your Instagram Business Account

### 3. INSTAGRAM_BUSINESS_ACCOUNT_ID (Optional)
- Your Instagram Business Account ID
- If not provided, the system will automatically fetch it from your Facebook Page

## Setup Steps

### Step 1: Convert Instagram Account to Business Account
1. Go to Instagram app settings
2. Switch to Business Account (if not already)

### Step 2: Link Instagram to Facebook Page
1. In Instagram app: Settings → Business → Facebook Page
2. Link your Instagram Business Account to a Facebook Page
3. Note your Facebook Page ID (found in Page Settings → About → Page ID)

### Step 3: Create Facebook App
1. Go to https://developers.facebook.com/
2. Create a new app or use existing one
3. Add "Instagram Graph API" product to your app

### Step 4: Get Access Token

#### Option A: Using Graph API Explorer (Quick Test)
1. Go to https://developers.facebook.com/tools/explorer/
2. Select your app
3. Generate token with permissions: `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`, `pages_manage_posts`
4. Exchange for long-lived token (valid 60 days)

#### Option B: Using Access Token Tool
1. Go to https://developers.facebook.com/tools/accesstoken/
2. Select your app
3. Get Page Access Token for your Facebook Page
4. This token should have Instagram permissions

#### Option C: Generate Long-Lived Token Programmatically
```python
# Exchange short-lived token for long-lived token
import requests

SHORT_LIVED_TOKEN = "your_short_lived_token"
APP_ID = "your_app_id"
APP_SECRET = "your_app_secret"

url = f"https://graph.facebook.com/v18.0/oauth/access_token"
params = {
    'grant_type': 'fb_exchange_token',
    'client_id': APP_ID,
    'client_secret': APP_SECRET,
    'fb_exchange_token': SHORT_LIVED_TOKEN
}

response = requests.get(url, params=params)
long_lived_token = response.json()['access_token']
```

### Step 5: Get Instagram Business Account ID
The system will automatically fetch this, but you can also get it manually:

```python
import requests

PAGE_ID = "your_page_id"
ACCESS_TOKEN = "your_access_token"

url = f"https://graph.facebook.com/v18.0/{PAGE_ID}"
params = {
    'fields': 'instagram_business_account',
    'access_token': ACCESS_TOKEN
}

response = requests.get(url, params=params)
instagram_account_id = response.json()['instagram_business_account']['id']
```

### Step 6: Update .env File
Add these lines to your `.env` file:

```
INSTAGRAM_ACCESS_TOKEN=your_long_lived_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_instagram_business_account_id  # Optional
```

## Important Notes

- **Long-lived tokens expire after 60 days**. You may need to refresh them periodically.
- **Rate Limits**: Instagram Graph API allows up to 25 posts per 24 hours per business account.
- **Image Requirements**: 
  - Minimum 320px width
  - Maximum 1440px width
  - Aspect ratio between 4:5 and 1.91:1 (recommended: 4:5 for portrait)
  - File size less than 30MB
- **App Review**: For production use, your app may need to go through Meta's App Review process.

## Testing

After setting up credentials, test with:
```bash
python main.py "your theme here"
```

