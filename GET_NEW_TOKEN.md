# How to Get a New Access Token for Test Mode

## Quick Steps

### 1. Go to Graph API Explorer
Visit: https://developers.facebook.com/tools/explorer/

### 2. Select Your App
- In the top right, select your app: **724362370726318** (or your app name)

### 3. Add Required Permissions
Click "Add Permissions" button and add these:
- `instagram_basic`
- `instagram_content_publish` 
- `pages_read_engagement`
- `pages_manage_posts`

### 4. Generate Token
1. Click "Generate Access Token" button
2. A popup will appear - click "Continue as [Your Name]"
3. Review and approve all requested permissions
4. Copy the generated token

### 5. Exchange for Long-Lived Token (Optional but Recommended)
The token from step 4 expires in 1 hour. To make it last 60 days:

1. Use this URL (replace YOUR_TOKEN with the token from step 4):
```
https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=724362370726318&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_TOKEN
```

2. Or use the Access Token Debugger:
   - Go to: https://developers.facebook.com/tools/debug/accesstoken/
   - Paste your token
   - Click "Extend Access Token" button

### 6. Update .env File
Replace the `INSTAGRAM_ACCESS_TOKEN` value in your `.env` file with the new token.

### 7. Test
Run: `python main.py "test theme"`

## Important Notes
- Make sure your app is in **Development Mode** (not Live)
- You must be an Admin or Developer of the app
- The token will work for your own Facebook Page and Instagram account
- Short-lived tokens expire in 1 hour
- Long-lived tokens expire in 60 days

