---
name: osint-web-archives
description: Find and verify historical facts in public web archives. Use for Wayback captures, missing gallery images, and visible text printed on archived photos, catalog cards, or posters.
---

# OSINT web archives

1. Find the relevant archived page near the requested date. If its address is unknown, follow dated links and redirects to recover the original URL. Keep that URL and the timestamp of the capture actually opened.
2. If the page is a gallery or catalog and the requested label is absent from its text, inspect the saved HTML for `<img src>`, `srcset`, lazy-load attributes, and links to larger images. Resolve relative paths against the original page URL and its `<base href>` when present. Keep the filenames observed in the markup. A card number printed on an image may bear no relation to its filename.
3. Look up each relevant image URL separately in the public archive index. If the page's date has no image capture, check nearby captures of that exact URL. Verify the effective capture timestamp and that the response contains a decodable image. Start with the relevant section of the gallery and reuse saved results. If the exact URL is missing in Wayback, check another public archive when it covers the period.
4. Open the image with `view_image` when image input is available, or run local OCR. Crop and enlarge small labels as needed. Verify the identifier and requested value on the same card. Preserve punctuation and ranges as printed.
5. Cite the archived page and the actual image capture separately. The page establishes that it referenced the image at the page's capture time. The image establishes what was visible at its own capture time. If the dates differ, state the gap and look for a dated copy when the answer requires proof for the exact date.

## References

- [Diagnostics](./references/diagnostics.md) for exact URL lookup, missing captures, and small or ambiguous text.
- [Worked case](./references/worked-cases.md) for a catalog card whose printed identifier differs from its filename.
