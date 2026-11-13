# Media search diagnostics

| Observation | Next check |
|---|---|
| The image has page chrome, subtitles, or a watermark | Save the original. Search a copy cropped to the scene and search readable overlay text separately when it may identify a publisher. |
| The engine returns photos of the same model or landmark | Compare several frame-specific details such as reflections, damage, edge alignment, and background geometry. |
| OCR returns an uncertain letter or number | Enlarge the source region, compare plausible readings, and search with an independent visible clue. |
| Visual search is unavailable or rate limited | Use local OCR, logo or model markings, distinctive text in its original language, and combinations of object details. Record the tool failure separately from a search with no matches. |
| A result shows an unexpectedly early date | Check the original page and an archived copy that actually contains the frame. A TinEye First Found date records when its crawler saw that version. [TinEye help](https://help.tineye.com/article/248-what-does-tineye-first-found-on-mean) |

A search result may point to a similar image, an object, or a page using the same image. Confirm the relevant match on the source page and record which crop led to it. [Google Lens help](https://support.google.com/websearch/answer/1325808)

## Video

Inspect title cards, visible text, and the beginning and end of the clip. Sample frames at scene changes and add a few time-spaced frames for long static shots. Deduplicate near-identical frames before searching. Keep each selected frame's playback time and extract the native frame where possible. Use the source timeline or frame timestamps for variable-frame-rate media. [FFprobe documentation](https://ffmpeg.org/ffprobe.html)

For a match, compare the scene before and after the frame when both clips are available. A clip can reuse footage from an earlier event. Cite the source and playback time for any observation that depends on a particular frame.

## Resolve an uncertain match

When OCR gives two readings, keep both until a separate clue resolves the text. For an object match, compare the marking with an independent catalog or other public source. For a same-frame match, compare several details tied to that shot, such as reflections and the alignment of foreground and background edges. Keep search-engine dates, page publication dates, and image capture dates in separate fields. If a provider is unavailable, record that outcome once and switch to the evidence already available.
