# Quick Fix: Replace "helloWorld" Input with Proper Fields

## Problem

Your Apify actor is showing the default input:
```json
{
    "helloWorld": 123
}
```

Instead of the proper Flipkart URL input fields.

## Solution

Follow these steps to fix the input schema:

### Step 1: Upload INPUT_SCHEMA.json

1. **Go to your actor in Apify Console**
2. **Click on "Source" tab**
3. **Upload `INPUT_SCHEMA.json` to the ROOT directory** (not in any subdirectory)
4. Make sure it's at the same level as `main.py`

The file should contain:
```json
{
    "title": "Flipkart Review Scraper Input",
    "type": "object",
    "schemaVersion": 1,
    "properties": {
        "flipkart_url": {
            "title": "Flipkart Product URL",
            "type": "string",
            "description": "The Flipkart product URL to scrape reviews from (must contain /p/)",
            "editor": "textfield",
            "example": "https://www.flipkart.com/product-name/p/itm123?pid=ABC123",
            "pattern": "^https?://.*flipkart\\.com/.*"
        },
        "max_reviews": {
            "title": "Maximum Reviews",
            "type": "integer",
            "description": "Maximum number of reviews to scrape. Leave empty or set to 0 to scrape all reviews.",
            "editor": "number",
            "example": 100,
            "default": 0,
            "minimum": 0
        }
    },
    "required": ["flipkart_url"]
}
```

### Step 2: Create .actor Directory

1. **In the Source tab, create a new folder** called `.actor` (with the dot)
2. **Inside `.actor`, upload `actor.json`**

The `.actor/actor.json` should contain:
```json
{
    "actorSpecification": 1,
    "name": "flipkart-review-scraper",
    "title": "Flipkart Review Scraper",
    "description": "Extract authentic product reviews from Flipkart",
    "version": "1.0.0",
    "input": "./INPUT_SCHEMA.json",
    "dockerfile": "./Dockerfile.apify"
}
```

### Step 3: Rebuild the Actor

1. **Click "Build" button** in the top right
2. **Wait for build to complete** (usually 1-3 minutes)
3. **Refresh the page**

### Step 4: Verify

1. **Go to "Input" tab**
2. You should now see:
   - **Flipkart Product URL** (text field)
   - **Maximum Reviews** (number field)
3. No more "helloWorld"!

## File Structure

Your actor should have this structure:

```
Root directory:
├── main.py                    ← Entry point
├── flipkart_scraper_apify.py ← Scraper logic
├── requirements.txt           ← Dependencies
├── INPUT_SCHEMA.json          ← Input fields definition ⭐ IMPORTANT
├── Dockerfile.apify           ← Docker config
├── .actor/
│   └── actor.json             ← Actor metadata ⭐ IMPORTANT
└── README.md                  ← Documentation
```

## Test Input

After rebuilding, test with this input:

```json
{
    "flipkart_url": "https://www.flipkart.com/lg-8-kg-5-star-smart-inverter-technology-turbodrum-diagnosis-soft-closing-door-fully-automatic-top-load-washing-machine-black/product-reviews/itma69f01a7f0c0a?pid=WMNGA3HKGRHDEDME",
    "max_reviews": 10
}
```

## Still Not Working?

### Checklist:
- ✅ `INPUT_SCHEMA.json` is in ROOT directory (not in a subfolder)
- ✅ `.actor/actor.json` exists with correct reference
- ✅ Actor has been rebuilt after uploading files
- ✅ Page has been refreshed

### Common Mistakes:
❌ Placing `INPUT_SCHEMA.json` inside a folder
❌ Not creating `.actor` directory
❌ Not rebuilding after changes
❌ Using old cached version

### Force Refresh:
1. Delete the actor
2. Create a new actor
3. Upload all files fresh
4. Build

## Expected Result

After fixing, your input form should look like:

```
┌─────────────────────────────────────┐
│ Flipkart Product URL *              │
│ ┌─────────────────────────────────┐ │
│ │ https://www.flipkart.com/...    │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Maximum Reviews                     │
│ ┌─────────────────────────────────┐ │
│ │ 100                             │ │
│ └─────────────────────────────────┘ │
│                                     │
│            [▶ Start]                │
└─────────────────────────────────────┘
```

## Need More Help?

Check the full guide: [APIFY_DEPLOYMENT.md](APIFY_DEPLOYMENT.md)
