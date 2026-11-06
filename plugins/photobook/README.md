# AI Photobook Maker for Claude: phone photos into a print-ready photo book

**photobook-maker** is an open-source Agent Skill for Claude (Claude Code, Cowork and the Claude apps)
that turns a messy folder of phone photos, WhatsApp images, iPhone HEIC files and scanned old prints
into a **story-driven, print-ready photo book PDF**. It also helps you order the printed book, and
can place the order for you in the browser.

Its default printer is **[Print&Bind (printenbind.nl)](https://www.printenbind.nl/en/book/photobook)**,
an online printer in the Netherlands that accepts your own PDF. The PDF also works with most other
printers that accept a PDF.

> Built for a real family album: 70 pages, 30×30 cm, made from about 90 photos and 10 messages
> from friends and family. I made the decisions in plain words and Claude did
> the layout work.

---

## What it does

- **Sorts your photos into a story.** It uses your folders (childhood, parents, family, friends,
  "us") as chapters, in the order you choose, with a title page and a lead photo for each chapter.
- **Gives every photo the same look.** It evens out light, contrast, white balance and warmth across
  phone photos from different years, and fixes colour casts on scanned prints.
- **Fixes scans.** It rotates sideways photos, crops plastic sleeves and edges, and can turn chosen
  photos black and white.
- **Lays out the pages.** It puts 1 or 2 photos per page and mixes portrait and landscape. Low-res
  WhatsApp photos are never blown up past what prints sharply. A few sharp photos get a full page.
- **Adds message pages.** It corrects typos and diacritics in the messages from friends and family,
  keeps each one in its original language, and places it right after that person's chapter. Two
  quotes never appear back to back.
- **Exports a print-ready PDF.** Single pages with 3 mm bleed, a safe margin near the spine, sharp
  embedded fonts, the front cover as page 1 and the back cover as the last page. It works for any
  size: 21×21, 30×30, A4 portrait or landscape, A5.
- **Checks print quality.** It flags pages with photos that will print blurry, low-res, dark or
  grainy, with close-up crops at real print size.
- **Gives ordering advice.** It recommends the size, paper (160 g, not glossy 170 g with glued
  binding), cover card, lamination and spine text, with the reason for each and approximate prices.
- **Drives the browser order.** It opens a pre-filled Print&Bind order form, checks every option,
  uploads the PDF once you approve, fills in the spine text, and walks you through the preview. It
  stops at the cart, so you pay yourself.
- **Handles changes in plain words.** For example: "Move this photo to my parents", "make the car
  photo smaller", "shorten mum's message", "use a better photo here". New photos and new friends'
  messages can arrive at any time.

## Install

Claude Code:

```bash
/plugin marketplace add gceico/ones-skills
/plugin install photobook@ones-skills
```

Claude Desktop / Cowork: add the marketplace `gceico/ones-skills` in the plugins settings and enable
**photobook**. The skill can also be copied as a folder: `plugins/photobook/skills/photobook-maker/`.

Requirements: Python 3.9+, and the skill installs `pillow pillow-heif numpy opencv-python-headless
reportlab fonttools` itself. To order in the browser it needs a browser tool: Claude in Chrome, the
Cowork browser, or Playwright.

## Use it

Just ask:

- *"I have about 90 photos in ~/Pictures/anna-30 sorted in folders. Make a photo album for her
  birthday, 30×30, and add the messages her friends sent me."*
- *"Make a fotoboek of our trip to Portugal for printenbind, A4 landscape."*
- *"Which photos in my album will look bad in print?"*
- *"Order it on Print&Bind with matt laminated cover and her name on the spine."*

You get:

```
photobook-work/
  <title>_print.pdf        # upload this to the printer
  preview-spreads.jpg      # the whole book at a glance
  preview/pNNN.jpg         # every page
  quality_report.md        # pages that may print badly, with crops/
  graded/                  # your photos, edited, per chapter
  book.json                # the whole book as one editable file
```

## How it works

| Step | Script | What happens |
|---|---|---|
| 1 | `ingest.py` | Converts HEIC/JPG/PNG to upright JPEGs per folder and records size, orientation, B&W and capture date |
| 2 | `contact_sheets.py` | Makes labelled overview sheets that Claude looks through to curate the photos |
| 3 | `book.json` | Claude writes the story: chapters, lead photos, cover, fixes, messages |
| 4 | `grade.py` | Applies the same colour grade to every photo, plus rotation, crops and B&W |
| 5 | `build_book.py` | Lays out the pages and writes the PDF with vector text |
| 6 | `quality_report.py` | Checks print resolution, blur, darkness and grain |
| 7 | browser | Fills in the order form, uploads the PDF and checks the preview |

Design defaults: Cormorant Garamond and Jost fonts (both open-licensed), a warm off-white page tone,
a 22 mm margin on the spine side, and balanced line breaks in messages. All of it can be changed in
`book.json`.

## FAQ

**Which photo book size should I choose for phone photos?**
WhatsApp photos (about 1200×1600 px) print sharp up to about 18 cm. For a 30×30 cm book, use 1–2 of
them per page, and keep full-page photos for original camera or iPhone files. For mostly WhatsApp
photos, 21×21 cm is the safe choice.

**Which paper should I choose at Print&Bind?**
Extra firm 160 g white. Glossy 170 g can't be glued (perfect binding), and the thinner papers let
photos show through from the other side.

**Does it work with printers other than Print&Bind?**
Yes, with any printer that accepts a PDF upload. Set the trim size, bleed and spine margin from the
printer's file specifications. Printers that only work through their own online editor can't take
the PDF.

**Is my data sent anywhere?**
Your photos are processed locally or in your Claude session. The PDF is only uploaded to the printer
after you approve it, and the skill never enters passwords or payment details.

**Can I add photos or messages later?**
Yes. Drop new photos in a folder, or paste a new message, and the book rebuilds. A new folder becomes
a new chapter automatically.

## Credits

Made by [Gabriel Ceicoschi](https://github.com/gceico) at **[Aibl.to](https://aibl.to)**, where we
build AI agents that take over real, repetitive work like this, for teams and for businesses.

Run a print shop, photo lab or e-commerce store and want an agent like this for your own customers,
on your site or on WhatsApp, connected to your order API? [Let's talk](https://aibl.to).

Not affiliated with Print&Bind. License: MIT.
