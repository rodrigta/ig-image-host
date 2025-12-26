# Setting Up Facebook App for Test Mode

## Current Status
- App ID: 724362370726318
- Page ID: 985617281290628
- Instagram Business Account ID: 24947725968239405

## Steps to Enable Test Mode

### Step 1: Verify App is in Development Mode
1. Go to: https://developers.facebook.com/apps/
2. Select your app (ID: 724362370726318)
3. Check the top banner - it should say "Development" mode
4. If it says "Live" or "In Review", click "Development" to switch

### Step 2: Add Required Permissions
1. In your app dashboard, go to **App Review** → **Permissions and Features**
2. Find these permissions and add them (if not already added):
   - `instagram_basic` 
   - `instagram_content_publish`
   - `pages_read_engagement`
   - `pages_manage_posts` (for uploading images to Facebook)

### Step 3: Add Your Account as Test User/Admin
1. Go to **Roles** → **Roles** in your app dashboard
2. Make sure your Facebook account is listed as:
   - **Admin** (has all permissions), OR
   - **Developer** (can test permissions)

### Step 4: Generate New Access Token with Permissions
1. Go to: https://developers.facebook.com/tools/explorer/
2. Select your app from the dropdown
3. Click "Add Permissions" and add:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement`
   - `pages_manage_posts`
4. Click "Generate Access Token"
5. Authorize all permissions
6. Copy the new access token
7. Update `.env` file with the new token

### Step 5: Test the Application
Run: `python main.py "your theme here"`

## Notes
- In Development mode, permissions work for app admins/developers automatically
- No App Review needed for Development mode
- Make sure you're testing with your own Facebook Page and Instagram account

