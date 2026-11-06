# book.json reference

The whole book is described by one JSON file in the work directory. Everything is optional except
`title` and `chapters`. Photo references are **name prefixes** as shown on the contact sheets
(slugified: lowercase, spaces → `-`; e.g. `img_1234`, `whatsapp-image-2025-05-01-at-10-00-00-1`).
Group names are the slugified folder names (`Us two (2024)` → `us-two`).

```json
{
  "title": "Anna",
  "subtitle": "thirty years",
  "output": "anna-30_print.pdf",

  "page":  {"width_mm": 300, "height_mm": 300, "bleed_mm": 3,
            "binding_margin_mm": 22, "outer_margin_mm": 20, "gap_mm": 6},
  "print": {"min_dpi": 170, "hero_min_dpi": 125},
  "style": {"paper": "#FCFAF6", "ink": "#282624", "muted": "#78726A", "accent": "#C4807C"},

  "cover": {"photo": "childhood/img_0001", "photo_width": 0.7, "back_text": "2025",
            "repeat_inside": false},
  "intro_pages": [
    {"type": "title"},
    {"type": "stats", "rows": [["30", "years"], ["12", "countries"], ["1 000+", "photos"]]}
  ],
  "closing": {"text": "to be continued…"},

  "grade": {
    "rotate": {"img_0012": 90},
    "crop":   {"scan-03": [0, 0.16, 0.99, 0.905]},
    "bw":     ["img_0420", "club-night-2"],
    "old_photos": ["childhood"],
    "warmth": 1.0
  },

  "chapters": [
    {"folder": "childhood", "title": "Roots",   "subtitle": "where it all began", "hero": "scan-01"},
    {"folder": "parents",   "title": "Parents", "subtitle": "Maria & John",       "hero": "img_0100"},
    {"folder": "us-two",    "title": "Us",      "subtitle": "the two of us",      "hero": "img_0900", "last": true}
  ],
  "order":     {"us-two": ["img_0850", "img_0700"]},
  "moves":     {"scan-05": "parents"},
  "exclude":   ["img_0311", "img_0950"],
  "feature":   ["img_0420", "img_0990"],
  "nofull":    ["img_0870"],
  "secondary": ["img_0012"],
  "auto_full": true,

  "messages": [
    {"after": "parents", "author": "Mom & Dad", "text": "Paragraph one.\nParagraph two."},
    {"after": "friends", "pos": 1, "author": "Eva", "relation": "friend", "text": "..."},
    {"author": "Me", "text": "Closing message, goes at the end when 'after' is missing."}
  ]
}
```

| Key | Meaning |
|---|---|
| `page` | Trim size and margins in mm. 300×300 default; A4 portrait = 210×297, landscape = 297×210. Type scales with the short side |
| `print.min_dpi` | Photos are never enlarged beyond this (170 is a good compromise for phone photos); `hero_min_dpi` applies to chapter-opener and cover photos |
| `cover.photo` | `group/prefix` of the cover photo; it is not repeated inside unless `repeat_inside` |
| `intro_pages` | Pages after the inside cover: `title`, `stats` (big numbers + small labels), `text` |
| `closing` | Optional last text page ("to be continued…") |
| `grade.*` | Read by grade.py; changing it regrades everything automatically |
| `chapters[].hero` | Photo on the chapter title page (default: first photo) |
| `chapters[].last` | Keeps this chapter last when new folders appear |
| `order` | Explicit photo order per group (unlisted photos follow by date) |
| `moves` | Show a photo in another chapter without moving files |
| `exclude` | Leave photos out |
| `feature` | Force a full-bleed page (only sharp, high-res photos) |
| `nofull` | Never full-bleed (pairs instead) |
| `secondary` | Alone on a page but small (60 %) |
| `auto_full` | Let high-res photos get full pages automatically for rhythm |
| `messages[].after` | Group the message follows; `pos` = after N photo pages of that chapter instead of at the end |

Page order: front cover · blank inside cover · intro pages · chapters (opener, photo pages, messages) ·
closing · blank inside back cover (if needed for an even count) · back cover.
