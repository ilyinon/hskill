# Archive image diagnostics

## Recover the original URL

- If you have a title or a distinctive phrase, look for quoted text, alternate spellings, and links from dated directories, calendars, or neighboring captures. Use archived navigation and recorded redirects to recover the old path and host. Record where each candidate URL came from.
- Keep query parameters that select content. Check observed host, protocol, and path variants when a migration or redirect supports them. Inspect CDX's original URL and redirect captures to follow the historical trail.
- Keep a small record of exact URLs, date windows, and outcomes. Before guessing new filenames, collect and deduplicate the assets in any gallery HTML you already have. Check the likely thumbnails and full images from that list.

## Find the file

- If replay shows blank tiles, inspect the page source for original asset URLs. A script that opens a larger view may contain a literal filename or map a thumbnail to a different URL.
- If one variant is missing, try the thumbnail or larger view referenced by the page and widen the date range for the exact URL. Reuse the result of each lookup. Keep an empty index response distinct from a timeout or HTTP 429, and follow the archive's retry guidance.
- If replay returns HTTP 200, check the final URL and decode the bytes before treating the result as an image. Save the raw file and use a separate crop for inspection. [Wayback help](https://archivesupport.zendesk.com/hc/en-us/articles/360004651732-Using-The-Wayback-Machine)

To list captures for one observed asset, substitute its absolute original URL and set a date window around the page capture. Widen the window if needed. CDX `statuscode` describes the archived origin response. Verify the replay separately. [Wayback CDX documentation](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server)

```sh
curl --get --compressed --max-time 20 'https://web.archive.org/cdx/search/cdx' \
  --data-urlencode "url=$asset_url" \
  --data-urlencode 'from=2008' --data-urlencode 'to=2010' \
  --data-urlencode 'output=json' \
  --data-urlencode 'fl=timestamp,original,statuscode,mimetype,digest'
```

## Try a second public index

If Wayback lacks a capture of the observed URL, check the exact URL in a suitable [Common Crawl collection](https://index.commoncrawl.org/). Choose collections by date and note their coverage. When an index hit has a WARC filename, offset, and length, use the record's bytes to confirm its target URL, capture time, and contents. The index hit identifies a candidate record. [Common Crawl retrieval guide](https://www.commoncrawl.org/get-started)

## Read the label

- Scan the edges of the image as well as the subject. Catalog numbers and values may sit in separate strips. Inspect an enlarged crop for characters that change the answer, such as a slash, hyphen, or digit.
- If the current model accepts text only, crop the label locally and use OCR. For one line, `tesseract label.png stdout --psm 7` is a starting point. Try another crop or a larger archived copy if the output is ambiguous. [Tesseract quality guide](https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html)
- If several files show similar subjects, match the printed identifier before extracting the value. If neither the image nor an independent dated copy is legible, report the unresolved field with the strongest available evidence.

## Keep the dates separate

For each relevant asset, record the original URL, the requested replay date, the effective capture date after redirects, and whether the saved body decodes. Record any printed publication date separately. A later image capture establishes when the archive captured those bytes. To link it to an earlier gallery, check the gallery's actual asset reference and corroborate the printed identifier or compare with a dated copy. When a filename could have been reused, say what the earlier HTML establishes and what the later image establishes. Cite the replay that supplied the evidence.
