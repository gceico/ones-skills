# Design guide: story, curation, messages, typography

What separates a nice photobook from a folder dump. Read this before writing book.json.

## Story first

- Ask what the book is for (birthday, anniversary, wedding, baby's first year, memorial, trip) and who
  it is for. The occasion becomes the title/subtitle and often an intro "stats" page
  (e.g. "30 years · 12 countries · 1 000+ photos").
- Chapters follow a life or a trip: **past → people → present**. A common arc for a person:
  roots/childhood → parents → family → friends → studies/work → partner's family → "us" last.
  For a trip: arrival → places in order → people → last evening. The last chapter is the emotional
  peak; mark it `"last": true` so new folders slot in before it.
- The user's folders are usually already the best grouping (they know who is who). Use them. If they
  dumped everything in one folder, propose groups from the contact sheets (faces, places, dates) and
  confirm. Face recognition is rarely needed; asking "who is in folder X?" is faster and more accurate.
- Chapter titles: short, warm, in the book's main language; a subtitle can name the people
  ("Tom, Lisa & the little ones"). Use the names the user gives — never guess names.

## Curation

- Drop near-duplicates (keep the sharper / better expression), screenshots, and photos where the
  main person is tiny or blurred. Use `exclude` rather than deleting files.
- Fix: sideways scans (`grade.rotate`), plastic-sleeve/edge borders on scanned prints (`grade.crop`),
  colour casts on old prints (`grade.old_photos`).
- Variety keeps pages alive: mix portrait and landscape; turn a few photos black & white — good
  candidates are near-monochrome photos, photos with ugly coloured light (club purple, sodium orange),
  and quiet emotional portraits. 5–10 % B&W is plenty.
- Hero photo per chapter (`hero`) = the photo that sums the chapter up, ideally sharp and bright.
  Full-page photos (`feature`) only for high-resolution, strong images; never for blurry ones.
  `secondary` makes a photo small on its own page ("a bit secondary"); `nofull` keeps it out of full pages.
- The cover photo should be the sharpest, most "her/him/us" image. Low-res cover photos look soft
  because people inspect covers closely.

## Resolution rules of thumb (300 × 300 mm book)

| Photo | Prints sharp up to | Use as |
|---|---|---|
| WhatsApp 1200×1600 | ~18 × 24 cm | half page / pair |
| WhatsApp 960×540 / 1024×768 | ~14 cm wide | small, pair, or skip |
| iPhone 3024×4032 | full page | full bleed, hero |
| Phone photo of a print | depends on focus | pair; B&W hides colour cast |

`quality_report.py` flags what will look bad. Look at its crops yourself before reporting.

## Messages from friends and family

- Correct, don't rewrite: fix typos, punctuation and missing diacritics (ș ț ă î â in Romanian,
  umlauts etc.), keep the original language (mixing languages in one book is fine and charming),
  keep their voice and inside jokes.
- Emojis: the fonts don't contain them; remove them (the layout adds a small heart under each message).
- Sign-off: the name(s) as the family uses them ("Mom & Dad", "Uncle Tom & Lisa"). If a message
  is from two people but written in singular, offer to switch it to plural.
- Long messages (> ~600 characters) get small type; offer to shorten, show the shortened text, and
  let the user approve.
- If a message looks duplicated (copy-paste error), flag it instead of printing it twice.
- Place each message right after the chapter of the people who wrote it. Never two message pages in a
  row (the build script enforces this). The user's own message usually closes the book.
- When the user asks you to write a message on someone's behalf, write a draft, label it clearly as
  your draft, and keep it short and warm. Don't print it until the user approves.

## Typography and style (defaults in build_book.py)

- Cormorant Garamond for titles and messages, Jost for small labels; warm off-white paper `#FCFAF6`,
  dark warm grey ink `#282624`. Change via `style` in book.json.
- Messages: balanced line lengths, ~1.5 line height, extra space between paragraphs, no lonely last
  word, numbers like "1 000" never break. All text is embedded vector text (sharp in print).
- Margins: 20 mm outer, 22 mm on the spine side, 6 mm between photos. Don't put faces or text in the
  spine area of full-bleed photos.
