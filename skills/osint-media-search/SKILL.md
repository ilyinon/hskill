---
name: osint-media-search
description: Find the source of a public photo or video, identify an object shown in it, or trace a repost using visible clues, OCR, reverse image search, and video frames.
---

# OSINT media search

1. Identify what the task asks for. Finding an object, matching the exact frame, and establishing the earliest confirmed publication require different evidence.
2. Preserve the best available original. Note distinctive details such as a sign, logo, markings, damage, reflections, or the arrangement of objects. Use local OCR for legible text and check ambiguous characters against the image. Treat metadata as a clue to verify.
3. Search the full frame or a targeted crop according to the question. A crop of a logo can identify an object, while a crop retaining the surrounding scene helps match the same frame. When image search is unavailable, search readable text, spelling variants, and combinations of distinctive details. Use public or authorized inputs for external image searches.
4. Open the underlying result pages and compare the actual images. Label each result as the same frame, a different photo of the same object, or a visually similar candidate. Account for cropping, resizing, mirroring, and overlays before rejecting a possible match.
5. For an object or event, verify the requested fact in a source that identifies the same entity. For publication history, record the page URL, media URL, stated date, and earliest capture that shows the media. Keep the date of indexing, capture, publication, and recording distinct.

## References

- [Diagnostics](./references/diagnostics.md) for search choices, fallback, and video frames.
- [Worked case](./references/worked-cases.md) for distinguishing a repost from a similar photo.
- [Web archives](../osint-web-archives/SKILL.md) when a page or image needs dated archival evidence.
