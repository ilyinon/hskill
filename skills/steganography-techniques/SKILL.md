---
name: steganography-techniques
description: >-
  Steganography detection and extraction playbook. Use when analyzing images (LSB, PNG chunks, JPEG DCT, EXIF), audio (spectrogram, DTMF), files (polyglots, appended data, ADS), and text (whitespace, zero-width, homoglyphs) for hidden data.
---

# Steganography Techniques

## Working approach

- Preserve the original and identify the actual file/container format
- Inspect metadata, structure, appended data, and modality-specific channels
- Select bit-plane, coefficient, spectrogram, archive, or text analysis from observed evidence.

## Evidence and limits

Extracted bytes or an embedded object are reproducible with documented parameters and independently interpretable structure.

Random strings, tool guesses, or entropy alone are not hidden messages; distinguish compressed/encrypted content, false signatures, and malformed containers.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. IMAGE STEGANOGRAPHY; 2. AUDIO STEGANOGRAPHY | [Read](./references/01-image-steganography.md) |
| 3. FILE STEGANOGRAPHY; 4. TEXT STEGANOGRAPHY; 5. DECISION TREE | [Read](./references/02-file-steganography.md) |
| Advanced: STEGANOGRAPHY TOOLS GUIDE | [Read](./STEGO_TOOLS_GUIDE.md) |
