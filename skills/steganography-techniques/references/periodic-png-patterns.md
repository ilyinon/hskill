# Periodic patterns in PNGs

Use this workflow for repeated tiles, bands, checkerboards, and woven-looking images supplied for offline analysis.

## Preserve coordinates and samples

- Keep the original file. Record the frame, image dimensions, sample depth, mode, and coordinates of each crop. Use decoded samples at their original resolution. Magnified previews are useful for choosing a crop. Use nearest-neighbor scaling for previews and keep the original sample grid for measurements.
- For indexed PNGs, inspect palette indices, RGB entries, and transparency when they carry distinct information. Two indices can render as the same color. A composite preview can also hide differences between transparent samples. For animated PNGs, record which frame or composited view you measured. [PNG specification](https://www.w3.org/TR/png-3/#11PLTE) · [Transparency](https://www.w3.org/TR/png-3/#11tRNS) · [Animation](https://www.w3.org/TR/png-3/#11fcTL)
- Check borders, annotations, and partial tiles in a separate view. If you exclude them from a comparison, save the crop or mask and report its coverage. Keep unexplained mismatches visible.

## Find a repeat and reconstruct it

1. Compare the original samples with horizontally and vertically shifted copies over their overlapping regions. Record the number of compared samples and mismatches for each candidate shift. If the image uses enlarged blocks, check the block grid before interpreting the tile coordinates.
2. Inspect smaller shifts as well as obvious multiples. Repeating stripes, flat patches, reflections, and half-tile phases can produce several plausible alignments. A common shift in a flat crop carries little information. Use a crop with variation on both axes.
3. Write a forward model for the image. For two interleaved sequences, record the crop origin, orientation, polarity, the order of each sequence, and the rule that selects one value at each crossing. Reconstruct the crop from those parameters and count pixel mismatches. For exact sample comparisons, list any systematic mismatches or clusters at seams.
4. Apply the same parameters to a second complete repeat when available. Keep that repeat out of the fit. Report both mismatch counts and their denominators. With only one repeat, record the available evidence and the validation that remains open.
5. When reconstruction is exact and the available held-out check agrees, save the artifact hash, crop origin, grid, crossing rule, axis order, extracted sequences, and mismatch counts. Continue with decoding and reuse that record after resuming. Reopen extraction only when a mismatch, a changed artifact, or a new clue affects it.

## Decode the extracted sequences

- Inspect the RGB samples in the reconstructed region. If the channels agree and their values are multiples of `0x11`, divide any channel by `0x11` to recover one hex digit per established grid position. Preserve axis order and repeated digits, including adjacent positions with the same shade.
- If the clue identifies two equal-length hex strings as key and ciphertext and leaves the transform open, try XOR on corresponding digits first. Retain the input width and leading zeros. For example, `a53c` XOR `a14f` gives `0473`. A nonce can be valid without readable text.
- For other readings, use the clue to select a transform and state the expected bit order, grouping, or independent check. Keep decoding local.
- If the puzzle advertises a raw nonce, use the exact raw string for the first authorized normal check. Record the exact input, whether it was raw or wrapped, and the observed verdict. Keep the reconstruction, candidate derivation, and verdict as separate observations.

## Worked local check

Warp `1011` and weft `01` define a four-column, two-row tile. Use the warp value at column `x` when `(x + y) % 2 == 0` and the weft value at row `y` otherwise. The observed tile rows are `1010` and `1011`. Reconstruct both rows and compare all eight samples. Flipping the first observed sample produces one mismatch and verifies that the comparison detects a local error.
