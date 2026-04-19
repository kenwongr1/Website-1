# Amerigroup International — Elementor Template Kit

Import-ready Elementor templates for all 6 pages. Works with WordPress 6+ and Elementor Free (v3.18+). Pro not required.

## Files in this folder

| File | Purpose |
|---|---|
| `01-home.json` | Home page |
| `02-about.json` | About Us |
| `03-technology.json` | Technology Solutions |
| `04-projects.json` | Projects portfolio |
| `05-team.json` | Our Team |
| `06-partners.json` | Our Partners |
| `custom.css` | Global styling (paste once into Elementor Custom CSS) |
| `generate.py` | Regenerator — edit content then re-run |

## Step-by-step import

### 1. Prep WordPress
- Install **Elementor** (free) from Plugins → Add New
- Activate any Elementor-compatible theme (Hello Elementor is recommended for a clean canvas)

### 2. Add the global CSS (once)
- Go to **Elementor → Custom CSS** (or Site Settings → Custom CSS in the editor)
- Paste the contents of `custom.css`
- Save

### 3. Import each page template
For each of the 6 `.json` files:

1. In WordPress admin, go to **Templates → Saved Templates**
2. Click **Import Templates** (top bar)
3. Upload the `.json` file
4. The template appears in your saved templates list

### 4. Create pages from templates
For each imported template:

1. Go to **Pages → Add New**
2. Set the title (e.g. "Home", "About Us", etc.)
3. Click **Edit with Elementor**
4. Click the **folder icon** (My Templates) in the widget panel
5. Find the imported template → click **Insert**
6. Set the **Page Layout** to **Elementor Canvas** (under Page Settings gear icon) for a full-width layout without theme header/footer
7. Publish

### 5. Set the Home page
- Settings → Reading → "Your homepage displays" → **A static page** → select your Home page

### 6. Configure menu (optional, nav is inline)
The nav bar is embedded in every page via HTML widget. If you'd prefer a WordPress menu:
- Delete the nav HTML widget at the top of each page
- Add an Elementor Nav Menu widget and link to your 6 pages

## Editing content

**Everything is editable in Elementor:**
- Headings → click the heading widget → change text in left panel
- Paragraphs → click the text editor widget → rich text editor
- Images → click the image widget → Replace with media library
- Buttons → click the button widget → text, link, color
- Dense blocks (grids, cards) are in HTML widgets — click the widget and edit HTML directly

## Regenerating after content changes

If you want to regenerate the JSON after bulk edits:
```bash
cd elementor-templates
python3 generate.py
```
Then re-import in WordPress (or delete the old template first).

## Notes
- Images use Unsplash URLs. Replace with your own via the image widget in Elementor.
- Emoji icons (☀️ ⚡ 💧) render natively. Swap for Elementor Icon widget if you prefer Font Awesome.
- The contact form is static HTML. For a working form, delete the form HTML widget and drop in the **Form** widget (Elementor Pro) or a plugin like Contact Form 7 / WPForms.
