For other original section numbers, use the [entry index](../SKILL.md#references).

Verification status and limits: records `png-ihdr-layout` in the [verification registry](../../hack/verification.json).



# SKILL: Steganography Techniques — Expert Analysis Playbook

> **AI LOAD INSTRUCTION**: Expert steganography detection and extraction techniques. Covers image steganography (LSB, PNG chunk hiding, JPEG DCT, EXIF metadata, dimension tricks, palette manipulation), audio steganography (spectrogram, LSB, DTMF, morse), file steganography (polyglots, binwalk, NTFS ADS, steghide), and text steganography (whitespace, zero-width Unicode, homoglyphs). Base models miss the systematic file-type-based analysis approach and tool-specific extraction workflows.

## 0. RELATED ROUTING

Before going deep, consider loading:

- [traffic-analysis-pcap](../../traffic-analysis-pcap/SKILL.md) for extracting files from network captures before stego analysis
- [memory-forensics-volatility](../../memory-forensics-volatility/SKILL.md) for extracting files from memory dumps
- [classical-cipher-analysis](../../classical-cipher-analysis/SKILL.md) if extracted hidden data is further encrypted/encoded

### Tool Reference

Also load [STEGO_TOOLS_GUIDE.md](../STEGO_TOOLS_GUIDE.md) when you need:
- Tool installation instructions and dependencies
- Detailed command reference for each stego tool
- Workflow patterns for specific file types

---

## 1. IMAGE STEGANOGRAPHY

### LSB (Least Significant Bit)

LSB embeds data in the least significant bits of pixel color channels.

```bash
# zsteg — LSB analysis for PNG/BMP
zsteg image.png                       # auto-detect all LSB patterns
zsteg image.png -a                    # try all known methods
zsteg image.png -b 1                  # extract bit plane 1
zsteg image.png -E "b1,rgb,lsb,xy"   # specific extraction pattern

# StegSolve (Java GUI)
java -jar StegSolve.jar
# Navigate color planes: Red 0, Green 0, Blue 0 → look for hidden image/text
# Data Extractor: specify bit planes + byte order

# stegoveritas — comprehensive automated analysis
stegoveritas image.png
# Runs: exiftool, binwalk, zsteg, foremost, color plane extraction
```

### PNG Specific

```bash
# pngcheck — validate structure, find hidden chunks
pngcheck -v image.png

# Hidden chunks: tEXt, zTXt (compressed text), iTXt (international text)
# Custom/private chunks may contain hidden data

# CRC vs dimensions trick
# A CRC mismatch can mean corruption or altered dimensions; it does not prove cropping
# Fix: brute-force correct width/height → reveals hidden rows/columns
python3 -c "
import struct, zlib
with open('image.png','rb') as f:
    data = f.read()
# Check IHDR CRC at offset 29
ihdr = data[16:29]  # 13-byte IHDR payload, excluding the four-byte chunk type
for h in range(1,2000):
    for w in range(1,2000):
        new_ihdr = struct.pack('>II',w,h) + ihdr[8:]
        if zlib.crc32(b'IHDR'+new_ihdr) & 0xffffffff == struct.unpack('>I',data[29:33])[0]:
            print(f'Width: {w}, Height: {h}')
"

# APNG (animated PNG) — hidden frames
# Use apngdis to extract all frames: apngdis image.png
```

### JPEG Specific

```bash
# steghide — embed/extract from JPEG (DCT coefficient modification)
steghide extract -sf image.jpg                 # extract (no passphrase)
steghide extract -sf image.jpg -p PASSWORD     # extract with passphrase
steghide info image.jpg                        # check if data is embedded

# stegcracker — brute force steghide passphrase
stegcracker image.jpg wordlist.txt

# jsteg — JPEG LSB steganography
jsteg reveal image.jpg output.txt

# JPEG structure analysis
exiftool -v3 image.jpg       # verbose metadata + structure
jpegdump image.jpg           # raw JPEG marker analysis
```

### EXIF Metadata

```bash
# exiftool — comprehensive metadata extraction
exiftool image.jpg
exiftool -b -ThumbnailImage image.jpg > thumb.jpg   # extract thumbnail
exiftool -all= image.jpg                             # strip all metadata

# Hidden data in EXIF fields (comment, artist, copyright, etc.)
exiftool -Comment image.jpg
exiftool -UserComment image.jpg
strings image.jpg | grep -i "flag\|key\|secret"
```

### Palette-Based (GIF)

```bash
# GIF color table manipulation — data in color palette order
gifsicle -I image.gif                    # info
gifsicle --color-info image.gif          # palette details
# Check for animation frames: convert -coalesce image.gif frame_%d.png
```

---

## 2. AUDIO STEGANOGRAPHY

### Spectrogram Analysis

```bash
# Sonic Visualiser — best for spectrogram viewing
# Layer → Add Spectrogram → look for visual patterns (text/images)

# Audacity
# Analyze → Plot Spectrum
# Select audio → change view to Spectrogram

# sox for command-line spectrogram generation
sox audio.wav -n spectrogram -o spectro.png
```

### Audio LSB

```bash
# DeepSound — hide/extract files in audio (Windows)
# GUI tool: open audio file → extract hidden files

# WavSteg — LSB in WAV files
python3 WavSteg.py -r -i audio.wav -o output.txt -n 1   # extract 1 LSB
python3 WavSteg.py -r -i audio.wav -o output.txt -n 2   # extract 2 LSBs
```

### DTMF / Morse Code

```bash
# DTMF decoder (phone tones)
multimon-ng -t wav -a DTMF audio.wav

# Morse code
# Audacity → visual inspection of on/off pattern
# Online decoder or manual: .- = A, -... = B, etc.

# SSTV (Slow-Scan Television) — image in audio
qsstv                    # GUI decoder
# Or: RX-SSTV (Windows)
```

### WAV Header Manipulation

```bash
# Check for data appended after WAV audio data
# WAV data chunk size vs actual file size
python3 -c "
import wave
w = wave.open('audio.wav','rb')
print(f'Frames: {w.getnframes()}, Channels: {w.getnchannels()}, Width: {w.getsampwidth()}')
expected = w.getnframes() * w.getnchannels() * w.getsampwidth() + 44  # 44 = WAV header
import os
actual = os.path.getsize('audio.wav')
if actual > expected:
    print(f'Extra data: {actual - expected} bytes appended')
"
```

---
