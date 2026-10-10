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

- Model quality, not an API defect. docs/model_evaluation.md reports 0.625 for the 20% test split,
  which holds only 8 tickets, and 0.632 (+/- 0.198) for the 5-fold cross-validation mean, which that
  report calls the more reliable figure. The model also mislabels some tickets, for example
  TC-Priority-015 in the priority PR was classified billing for a printer problem. This is a quality
  observation for the A2 owners.
- TC-HTMLLikeText-009: the API stores and returns the `<b>` tags literally, which is evidenced in
  tests/evidences/API-current-model-evidence.md. Browser rendering was observed separately in Chrome
  and has its own screenshot, tests/evidences/TC-HTMLLikeText-009-rendering.png. Script and image
  behaviour are not claimed here; the Task 2934 rows cover those with their own evidence.
