# Using another printer

The PDF this skill builds (single pages, bleed, embedded fonts, cover = first page, back = last page)
is the format most "upload your own PDF" printers accept. Before building for another printer, find
these on their file-specification / "aanleverspecificaties" / "file setup" page and set `page` in
book.json accordingly:

| Spec | Where it goes |
|---|---|
| Trim size (mm) | `page.width_mm`, `page.height_mm` |
| Bleed (usually 3 mm; some use 2 or 5) | `page.bleed_mm` |
| Safe zone / text margin | `page.outer_margin_mm` (keep ≥ their value + 5 mm) |
| Gutter / spine margin for glued books | `page.binding_margin_mm` |
| Page count rules (multiple of 2 or 4, min/max) | add blank/intro/closing pages; the build keeps an even count |
| Cover: first/last page of the PDF, or a separate cover spread? | if a spread is required, export the cover separately (width = 2 × page + spine) |
| Single pages or spreads? | this skill outputs single pages |
| Colour (RGB accepted? CMYK/Fogra required?) | most consumer printers accept RGB |

Tell the user honestly when a printer only works through its own online editor (many big consumer
photobook brands): then the deliverable is the graded photos + a page plan, not a PDF.

Hardcover and layflat books are offered by many printers but cost more and usually need a cover
spread with spine width from their calculator.
