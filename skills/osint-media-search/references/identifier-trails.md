# Follow an object identifier to a photo

Use this workflow when visible markings identify an object and a public record
is expected to lead from that object to a photo. Start with the identifier.

## Recover the marking locally

Preserve the input archive and verify a supplied SHA-256. Inspect the contents
before choosing a method. For an exact rectangular scan in 2–40 PNG pieces with
binary transparency, irregular matching edges, and quarter-turn rotations, run
the [local reassembly helper](../scripts/reassemble_png.py) from the skill folder.
It requires Python with Pillow and NumPy. Each piece may be up to 512 pixels per
side. It reads PNGs inside the ZIP and writes one verified rectangle.

```sh
python3 scripts/reassemble_png.py fragments.zip assembled.png --sha256 EXPECTED_HEX
```

Omit `--sha256` if no expected digest was supplied. Check the result's orientation
and use `--rotate 90`, `180`, or `270` with a new output path if needed. An incomplete
assembly call produces an error. For straight cuts, arbitrary rotations, or
missing pixels, inspect the visible regions and recover only the fields you
can verify.

Crop and enlarge each copy of the marking. For a text-only model, run local
OCR, for example `tesseract stdin stdout --psm 7 < serial-crop.png`. If print
is small or ambiguous, try a tighter crop or a different threshold, and compare
independent copies or a second reading. Record the identifier, series or version,
and any unresolved characters. Preserve the original form for citation and
normalize spacing only as appropriate for the record service.

## Prove the joins in order

1. **Object → report.** Search the exact identifier and open the source.
   Compare the identifier, series, and object type wherever the source exposes
   them. A public report with a masked number needs independent corroboration
   before it can establish an exact match.
2. **Report → entry → photo.** Record which entry is last, its timestamp and
   public URL, and what connects it to a contributor or photo. Useful links
   include a direct photo URL, a persistent public profile ID paired with the
   specific post, or an entry note that uniquely identifies the photo. Similar
   placenames, the same ZIP, and coincident latitude can help find candidates
   but cannot establish this join. Keep a search snippet separate from the
   opened source, and keep sighting, posting, and capture dates distinct.
3. **Photo → requested coordinate.** Keep the frame and its source. Read the
   camera position, direction and subject position separately, then use
   [geolocation](../../osint-geolocation/SKILL.md) to verify the requested point.
   Check a supplied latitude against that point and preserve the longitude's
   sign and supported precision.

If a search is blocked or requires recording a new sighting, look for an
existing public report link, an official read-only index, or a supplied capture.
Use truthful inputs and retrieve existing records through read-only views. Record
blocked lookup, no match in a searched index, and a matching entry with missing
attribution as distinct outcomes. For a fully offline run, use saved reports and
photo records. If the answer is rejected, retain verified observations, record
the rejected value, and revisit the earliest unproven join. Try another value
only if new evidence identifies a different interpretation or point. If the
needed source is unavailable, report the missing evidence and any verified
partial result.
