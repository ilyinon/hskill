# Read a capacity from an archived catalog

Synthetic example. A task asks for the capacity printed on display card `B-017` in a store catalog captured on 18 September 2009.

1. Searching the page for `B-017` gives no matches. The image URL guessed from the card number has no index records. The saved gallery HTML contains `<img src="../media/display-blue.jpg">` and a neighboring `display-green.jpg`.
2. The exact URL for `display-blue.jpg` has a capture from 2010. The replay decodes as JPEG. In the image, the top left reads `B-017` and the bottom strip reads `CAPACITY 36/42`.
3. The neighboring image shows the same display style but is labeled `B-018` and has a different capacity. This checks that the value came from the requested card.
4. Report `36/42` as printed in the recovered JPEG. Cite the 2009 catalog for the link and the 2010 capture for the text. The exact text present on 18 September 2009 remains unverified unless a dated copy or other contemporary evidence confirms it.
