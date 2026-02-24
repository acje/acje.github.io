# Favicon Setup Instructions

## Current Status
A placeholder SVG favicon has been created with your initials "AJ".

## To Create Professional Favicons

### Option 1: Use Favicon Generator (Recommended)
1. Visit https://realfavicongenerator.net/
2. Upload a square image (at least 512x512px) with your logo or branding
3. Download the generated favicon package
4. Replace files in this `static/` directory with:
   - `favicon.ico`
   - `favicon-16x16.png`
   - `favicon-32x32.png`
   - `apple-touch-icon.png`
   - `android-chrome-192x192.png`
   - `android-chrome-512x512.png`
   - `site.webmanifest`

### Option 2: Use Favicon.io
1. Visit https://favicon.io/
2. Choose from:
   - Text to favicon (use initials "AJ")
   - Image to favicon (upload logo)
   - Emoji to favicon
3. Download and extract to this directory

### Option 3: Keep SVG (Modern browsers only)
The current `favicon.svg` works for modern browsers but not older ones or all platforms.

## Files to Replace
- Replace `favicon.svg` with your custom design
- Add `favicon.ico` for legacy browser support
- Add PNG versions for various devices

## Hugo Book Theme Integration
The theme automatically includes favicons from the static folder via the `html-head-favicon` partial.
