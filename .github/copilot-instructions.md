# Food-Picker Project: AI Coding Guidelines

## Project Overview
Food-Picker is a web application for randomly selecting recipes and managing favorites. It's a multi-page HTML/CSS application with a main recipe picker interface and navigation to favorites, personal recipes, and shared recipes.

## Architecture & File Structure

### Core Pages
- **Untitled-1.html** - Main entry point; contains the "Randomise Food" button, navigation to recipes/favorites
- **My_recipies.html** - Personal recipes page (structure incomplete, needs expansion)
- **HTML_Favorites** - Favorites page (incomplete template)

### Styling
- **CSS-Foodpicker.css** - Global stylesheet with:
  - CSS Variables (--accent: #1e88e5, --text, --bg)
  - Button styling (.randomise-btn with hover transform effect)
  - Layout utilities (.main flexbox container)

## Critical Issues to Fix (Priority)
1. **CSS Syntax Errors in CSS-Foodpicker.css**:
   - Line 2: `--bg: ##fffff;` → should be `#ffffff` (double hash)
   - Line 27: `box-shadow: rgba(red, green, blue, alpha)` → invalid values, use hex/rgb
   - Line 29: `transofrm` → typo, should be `transform`; `box-shdow` → `box-shadow`
   - Line 35: `font-size: px1000;` → invalid unit, should be `1000px`

2. **HTML Markup Issues**:
   - Untitled-1.html: `<style href="...">` is invalid; use `<link rel="stylesheet">`
   - My_recipies.html: `<title>` contains only `<p>` tags, no actual content
   - Navigation link syntax is malformed (`.html.</a.>` instead of `</a>`)
   - Semantic issues: `<h1>` nesting inside `<h3>` and `<title>` tags

## Development Patterns

### HTML Structure Convention
- Single-page HTML files for each feature (recipes, favorites, etc.)
- Use semantic HTML5 (`<header>`, `<main>`, `<nav>`)
- Include Google Fonts preconnect (DM Serif Text font currently used)
- Viewport meta tag for responsive design

### CSS Organization
- Use CSS Custom Properties at `:root` level for theming
- Primary accent color: **#1e88e5** (Material Blue)
- Apply flex layout for main content centering
- Button interactions use `transform` and `box-shadow` for depth

### Common Navigation Pattern
```html
<a class="My_recipies" href="/path/to/page.html"><h3>Page Title</h3></a>
```
*Note*: Update to use proper button semantics or `<nav>` elements as scope expands.

## Integration Points
- **Google Fonts API** - DM Serif Text loaded from googleapis.com
- No backend/database yet - data structure TBD
- No JavaScript framework - vanilla HTML/CSS (add JS when randomization logic needed)

## Key Conventions & Gotchas
- File names use underscores (`My_recipies.html`) - maintain consistency
- CSS variables must be defined in `:root` for global access
- Button interactions require both `transform` and `box-shadow` for Material Design feel
- Links in navigation use relative paths with leading `/` (e.g., `/My_recipies.html`)

## Next Steps for Expansion
1. Fix all CSS syntax errors (see Critical Issues)
2. Add JavaScript for "Randomise Food" button functionality
3. Implement responsive grid for recipe display
4. Create data structure for storing recipes (local storage or backend)
5. Complete HTML templates for My_recipies.html and Favorites page

## Testing & Validation
- No build system currently - work directly with HTML/CSS
- Manually test in browser after changes
- Validate HTML at https://validator.w3.org/
- Check CSS at https://jigsaw.w3.org/css-validator/
