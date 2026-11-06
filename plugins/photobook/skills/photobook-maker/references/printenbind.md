# Print&Bind (printenbind.nl) — recommended printer

Dutch online printer, ships across NL/BE/EU, fast (standard production is 1 working day), cheap for
one-off books, accepts your own PDF (no forced editor), and has an English site. This is the printer
the skill was built and tested against. Facts below were read from the live order form on
**6 November 2026**; re-check anything price- or stock-related on the site before promising it.

Contents: product & order URL · options and recommended picks · file specs · cover/spine · prices ·
pre-filled order URL · business API

## Product and order form

- Product: **Photobook** (glued "perfect binding" softcover, or Wire-O spiral).
- Order form: `https://www.printenbind.nl/en/bestel/article?product=fotoboek`
- Sizes: **A5** (148×210), **A4** (210×297), **A3** (297×420), or **Custom**: width 120–300 mm,
  height 145–300 mm (so square 210×210, 250×250 and 300×300 all work, and A4 landscape 297×210).
- There is no hardcover or layflat option on this product. If the user insists on hardcover, see
  `other-printers.md`.

## Options, and what to recommend

| Section | Options on the site | Recommend | Why |
|---|---|---|---|
| Quantity | number of copies | 1 (+ extra copies for parents are cheap) | |
| Pages | page count of the PDF | exactly the PDF's page count | Page 1 and the last page become the cover (check preview) |
| Color | Color / B&W | Color | |
| Size | A5, A4, A3, Custom | Custom 300×300 for a "real" album; 210×210 or A4 for smaller budgets | Phone photos (often 1200×1600 px) print sharp up to ~18 cm, so larger books use 1–2 photos per page |
| Printing method | One-sided / Double sided | **Double sided** | Photobooks are read as spreads |
| Title page | Front/title page double-sided, or single-sided | default | |
| Dividing sheet | none / insert | none | |
| Paper type | Standard 80 g, Roman Biotop cream 90, Firm 100, Rustic off-white 120, **Extra firm white 160**, Glossy off-white 170 | **Extra firm 160 g** | Thick enough that photos don't show through; bright white keeps colours and B&W crisp. **Glossy 170 g cannot be perfect bound** (the glue doesn't hold) — the site greys it out. Thin papers show through when printed double-sided. Rustic is off-white and dulls photos |
| Round corners | none / round | none | |
| Finishing | **Perfect binding** / Wire-O | Perfect binding | Looks like a book; Wire-O only if they want it to lie flat |
| Spine (perfect binding) | Unprinted (white) / Printed via your own file / Printed via spine editor | **Printed via spine editor** | Lets the user type a title on the spine without rebuilding the cover as a spread. Suggest text like `Title · Subtitle`, background = the book's paper colour, text = ink colour |
| Short side binding | checkbox | off | |
| Cover | Natural card white 300, **Card off-white 350**, Old Dutch off-white 300, Linen pressing white 300, Pearl luxury white 300, Ecofibre beige 320, Tulip bulbs 300 | **Card (off-white 350)** | Thickest; off-white matches the default warm page tone. Ecofibre beige yellows the photo; Pearl adds shimmer; Tulip bulbs is seed paper |
| Cover finishing | No finishing, **Glossy laminated**, **Matt laminated**, Provided with a glossy coating | **Matt laminated** if in stock, else **Glossy laminated** | Lamination is a protective film. "Glossy coating" is only a varnish that scuffs. Matt was out of stock until 10 Nov 2026 when checked |
| Backside cover | Unprinted / Printed | Printed | The last PDF page is the back cover |
| Extra document check | +€7.63 | optional | A human checks the file; worth it for a first order if the user is nervous |
| Borderless printing | checkbox | on (default) | The PDF already has 3 mm bleed |
| Delivery | Pick up (Groningen) / Post | Post | |
| Production | Urgent / Standard (1 day) / Budget (4 days, cheaper) | Budget if there is time | |

## File specifications (from their "Submission conditions")

- **PDF**, all pages the same size, **single pages, not spreads** (their system orders pages itself).
- **Bleed 3 mm** recommended (without bleed they enlarge by 1 mm themselves).
- **Text margin**: keep text and important content ≥ 5 mm from the trim edge.
- **Spine margin**: ≥ **15 mm** on the binding side; glued books don't open flat. The skill uses 22 mm.
- **Frames**: if you draw borders, make them ≥ 4 mm (machine deviation up to 1 mm).
- **Resolution**: they ask for 300 dpi. Pages are rendered at 300 dpi; individual phone photos inside
  may be lower (170+ dpi is fine in practice). Their automatic check may show a resolution warning
  for those — it does not block the order.
- **Colour**: experts are asked for PDF/X-1a:2001, Fogra39L CMYK. RGB PDFs are accepted and converted;
  very saturated colours (neon/club light, turquoise water) may print slightly more muted.
- Fonts embedded (the skill's PDF embeds them as vector text).
- Size 300×300 trim with bleed = 306×306 mm (3543×3543 px at 300 dpi is the no-bleed equivalent).

## Cover and spine

- With a printed cover, **page 1 of the PDF is the front cover** and **the last page is the back
  cover**; page 2 and the second-to-last page are left blank on purpose (inside covers). The site's
  live preview confirms this — always check it before ordering.
- "Printed via your own file" needs a single cover **spread** (back | spine | front) whose width is
  2 × page width + spine width; the site shows the exact spine width. Avoid unless the user wants a
  wrap-around cover photo; the spine editor is simpler.
- Spine width is roughly pages ÷ 2 × 0.18 mm for 160 g paper (~6–7 mm for 70 pages), enough for one
  small line of text.

## Indicative prices (6 Nov 2026, incl. VAT and postage, 1 copy, 160 g, perfect binding, glossy laminated, printed back)

| Size | Pages | Price |
|---|---|---|
| 210×210 | 60 | ~€31 |
| 210×210 | 80 | ~€34 |
| 297×210 (A4 landscape) | 60 | ~€31 |
| 300×300 | 60 | ~€43 |
| 300×300 | 70 | ~€45 |

## Pre-filled order URL

The form reads its state from query parameters, so you can open it already configured and only
let the user (or the browser agent) check and upload. Parameter names seen on the form:

```
https://www.printenbind.nl/en/bestel/article?product=fotoboek&type=boekvorm
  &number=1                  # copies
  &copies=70                 # PAGES (yes, the parameter is called copies)
  &color=all
  &size=custom&size_custom_width=300&size_custom_height=300   # or size=a5|a4|a3
  &printside=double
  &add_inserts=0
  &papertype=160             # 80 | roman_90 | 100 | rustic_120 | 160 | mc_170 (glossy, not with perfect binding)
  &finishing_extra=none      # none | round_corner
  &finishing=garenloos+inbinden   # perfect binding | wire-o+inbinden
  &spine=custom              # blanco = unprinted, printed = via your own file, custom = via spine editor
  &spine_editor_text=Anna+%C2%B7+30      # URL-encoded spine text
  &spine_editor_font=Alegreya-Regular             # font chosen in the spine editor
  &spine_editor_text_align=center
  &spine_editor_bg_color=%23fcfaf6                # book paper colour (# encoded as %23)
  &spine_editor_text_color=%23282624              # ink colour
  &spine_edge=none
  &papertype_cover=card      # Card off-white 350
  &finishing_cover=laminating_glossy   # none | laminating_glossy | laminating_matt | coating
  &finishing2=laminating_glossy        # mirrors finishing_cover; keep both the same
  &printside_front=none      # title page: default (front/title page double-sided)
  &printside_back=1          # back cover printed (0 = unprinted: then don't put a back-cover page in the PDF)
  &borderless=1&check_doc=standard
  &delivery_method=post      # post | pickup
  &production_method=standard     # fast | standard | budget
  &comment=...               # optional note to the printer, URL-encoded (shown as "Add comment")
```

This parameter set was confirmed against a real order URL created on the site (Nov 2026).

### Worked example

300×300 mm, 70 pages, Extra firm 160 g, double sided, perfect binding, off-white 350 g card cover,
glossy laminated, back cover printed, spine text via the spine editor, post, standard production,
with a short note to the printer:

```
https://www.printenbind.nl/en/bestel/article?product=fotoboek&type=boekvorm&add_inserts=0&borderless=1&check_doc=standard&color=all&comment=Hello%2C+the+PDF+has+3+mm+bleed%3B+page+1+is+the+front+cover+and+the+last+page+is+the+back+cover.+Thank+you%21&copies=70&delivery_method=post&finishing=garenloos+inbinden&finishing2=laminating_glossy&finishing_cover=laminating_glossy&finishing_extra=none&number=1&papertype=160&papertype_cover=card&printside=double&printside_back=1&printside_front=none&production_method=standard&size=custom&size_custom_height=300&size_custom_width=300&spine=custom&spine_edge=none&spine_editor_bg_color=%23fcfaf6&spine_editor_font=Alegreya-Regular&spine_editor_text=Anna+%C2%B7+30&spine_editor_text_align=center&spine_editor_text_color=%23282624
```

Build it from the agreed settings, for example:

```python
from urllib.parse import urlencode
params = dict(product='fotoboek', type='boekvorm', number=1, copies=70, color='all',
              size='custom', size_custom_width=300, size_custom_height=300, printside='double',
              printside_front='none', add_inserts=0, papertype='160', finishing_extra='none',
              finishing='garenloos inbinden', spine='custom', spine_edge='none',
              spine_editor_text='Anna · 30', spine_editor_font='Alegreya-Regular',
              spine_editor_text_align='center', spine_editor_bg_color='#fcfaf6',
              spine_editor_text_color='#282624', papertype_cover='card',
              finishing_cover='laminating_glossy', finishing2='laminating_glossy', printside_back=1,
              borderless=1, check_doc='standard', delivery_method='post',
              production_method='standard', comment='Optional note to the printer')
print('https://www.printenbind.nl/en/bestel/article?' + urlencode(params))
```

Mistakes seen in real orders: `finishing_cover=coating` (varnish, not lamination) and
`printside_back=0` while the PDF contains a back-cover page — check both before uploading.
Build the URL with proper URL-encoding (e.g. Python `urllib.parse.urlencode`), never by hand.

Parameter names can change; after opening the URL, read the page and confirm every section shows
the intended value. The form shows "Price & delivery date are not shown due to error messages" when
a combination is invalid (for example glossy paper + perfect binding) — read the message in the
Configuration section and fix it.

## Business angle: Order API

Print&Bind has a REST **Order API** for webshops (token from the profile page, ~10 requests/second):
create an order, add articles (Photobook is one), attach files, set delivery, finish.
Docs: https://www.printenbind.nl/api/documentation and https://www.printenbind.nl/en/order-api.
Ordering through the API needs the user's own API token and still costs money — only use it if the
user explicitly asks and supplies the token; the website flow is the default.
