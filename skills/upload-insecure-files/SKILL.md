---
name: upload-insecure-files
description: >-
  Insecure file upload playbook. Use when testing upload validation, storage paths, processing pipelines, preview behavior, overwrite risks, and upload-to-RCE chains.
---

# Upload Insecure Files

## Working approach

- Map accept, store, process, and serve stages with one benign owned marker
- Identify validation, renaming, handlers, processors, access policy, and tenant ownership
- Choose only the processing or retrieval chain the evidence supports.

## Evidence and limits

The unchanged principal crosses a defined execution, path, ownership, rendering, or network boundary after upload.

Upload success or a stored dangerous extension alone is insufficient; handlers, MIME policy, processing, serving origin, and final permissions determine impact.

## References

Choose the reference matching the current step; do not preload the catalog. Original section numbers are retained below. Select engine, version, and prerequisites before using examples; version/vendor tables are candidates to verify.

| Current need / original sections | Read selectively |
|---|---|
| 1. CORE MODEL; 2. RECON QUESTIONS FIRST; 3. VALIDATION BYPASS MATRIX; 4. STORAGE AND RETRIEVAL ABUSE; 5. PROCESSING-CHAIN ATTACKS; 6. HIGH-VALUE EXPLOITATION PATHS; 7. AUTHORIZATION AND BUSINESS LOGIC CHECKS | [Read](./references/01-core-model.md) |
| 8. TEST SEQUENCE; 9. CHAINING MAP; 10. OPERATOR CHECKLIST; 11. UPLOAD SUCCESS RATE MODEL & ADVANCED METHODOLOGY; 12. POLYGLOT FILE TECHNIQUES | [Read](./references/02-test-sequence.md) |
| 13. IMAGEMAGICK EXPLOITATION CHAIN; 14. FFMPEG SSRF & LOCAL FILE READ; 15. CLOUD STORAGE UPLOAD CONSIDERATIONS; 16. CONTENT-TYPE VALIDATION BYPASS | [Read](./references/03-imagemagick-exploitation-chain.md) |
| Advanced: Upload Insecure Files — Extended Scenarios & Real-World Cases | [Read](./SCENARIOS.md) |
