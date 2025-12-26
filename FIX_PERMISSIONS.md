# Fix Missing Permission Issue

## Current Status
Your token has these permissions ✅:
- `instagram_basic`
- `instagram_content_publish`  
- `pages_read_engagement`
- `instagram_manage_contents`

**Missing permission** ❌:
- `pages_manage_posts` (required to upload images to Facebook)

## Solution: Generate New Token with All Permissions

### Step 1: Go to Graph API Explorer
Visit: https://developers.facebook.com/tools/explorer/

### Step 2: Select Your App
Choose your app from the dropdown (App ID: 724362370726318)

### Step 3: Add ALL Required Permissions
Click "Add Permissions" and make sure these are ALL selected:
- ✅ `instagram_basic`
- ✅ `instagram_content_publish`
- ✅ `pages_read_engagement`
- ✅ `pages_manage_posts` ⚠️ **THIS IS MISSING - MUST ADD**
- ✅ `pages_show_list` (optional but helpful)

### Step 4: Generate New Token
1. Click "Generate Access Token"
2. Authorize all permissions
3. **Important**: Make sure `pages_manage_posts` is granted
4. Copy the token

### Step 5: Update .env File
Replace `INSTAGRAM_ACCESS_TOKEN` with the new token that includes `pages_manage_posts`

### Step 6: Test Again
Run: `python main.py "test theme"`

## Why This Permission is Needed
Instagram Graph API requires:
1. Upload image to Facebook (needs `pages_manage_posts`)
2. Get public URL from Facebook
3. Create Instagram media container with that URL
4. Publish to Instagram

Without `pages_manage_posts`, step 1 fails.

