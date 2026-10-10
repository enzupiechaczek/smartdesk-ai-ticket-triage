# Bug Log

| Title | Steps to reproduce | Expected | Actual | Severity (high, medium, low) | Evidence | Owner |
| --- | --- | --- | --- | --- | --- | --- |

No genuine bugs found.

## Reclassified findings from the earlier bug template

The bug template previously held four rows. None were API defects, so none are carried forward as
open bugs. They are listed here so the reclassification is visible rather than silently erased.

| Original title | Why it is not a bug | Where the real result now lives |
| --- | --- | --- |
| Unexpected category, TC-ValidAccess-001 | The stub predictor returned technical for every ticket. The API returned the subject unchanged and behaved correctly. The expectation of access was right; the stub was the cause. | `tests/test_cases.md`, current-model rerun: returns access with confidence 0.768 |
| Unexpected category, TC-ValidBilling-002 | Same stub cause. | `tests/test_cases.md`, current-model rerun: returns billing with confidence 0.642 |
| Wrong error message, TC-101CharacterSubject-006 | The test expected "Subject must not exceed 100 characters". The API returns "Subject is required (max 100 characters)", which matches the documented contract in README.md. The expectation was wrong, not the API. | `tests/test_cases.md`, Expected column now states the documented message |
| Wrong error message, TC-501CharacterDescription-007 | Same cause: the expected text did not match the documented message. | `tests/test_cases.md`, Expected column now states the documented message |

## Open observations, not API bugs

- The trained model scores about 0.625 in cross-validation and mislabels some tickets, for example
  TC-Priority-015 in the priority PR was classified billing for a printer problem. This is model
  quality for the A2 owners, not an API defect.
- TC-HTMLLikeText-009: this PR verified that the API stores and returns the `<b>` tags literally. It
  did not independently verify browser rendering. The Task 2934 rows in `tests/test_cases.md` cover
  rendering and reload with their own evidence.