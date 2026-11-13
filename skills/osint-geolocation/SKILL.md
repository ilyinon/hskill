---
name: osint-geolocation
description: Verify where public or authorized imagery was taken using visible landmarks, maps, aerial images, and camera geometry. Use for photo or video geolocation and date-range clues.
---

# OSINT geolocation

1. Record what is visible before choosing a location. Separate legible text, layout, terrain, and skyline from interpretations. Verify apparent GPS and compass metadata against the scene. Check for mirroring or a rotated frame when text or orientation looks inconsistent.
2. Use high-information clues to find candidates. Search an unusual street or business name, a combination of landmarks, or a distinctive road, rail, or shoreline layout. Choose clues that can eliminate alternatives.
3. For each plausible candidate, place the camera and estimate its viewing direction. Compare left-to-right order, foreground and background, sightlines, angles, and fixed landmarks with a map, aerial image, or panorama. Test at least one discriminating feature when two candidates look alike.
4. Give the supported precision. Cite the camera position or bounded area, approximate viewing direction if relevant, matching evidence, and any remaining uncertainty. A landmark's map pin identifies the landmark. Give the camera coordinates only when its position is supported.
5. If time matters, use dated evidence to bound the scene. Compare lasting changes such as construction, signage, or road layouts. Treat shadows and seasonal clues as constraints and keep publication and capture dates separate.

## References

- [Diagnostics](./references/diagnostics.md) for testing camera geometry and estimating date intervals.
- [Worked case](./references/worked-cases.md) for choosing between two similar viewpoints.
- [Media search](../osint-media-search/SKILL.md) when the image needs a source or has appeared elsewhere.
