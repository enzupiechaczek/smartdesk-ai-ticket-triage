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

## Task 2933 

> **Note:** The statement 'No genuine bugs found' applies specifically to earlier API-contract and payload validation checks (which strictly met backend specifications), and does not contradict the new model-quality classification entry below.

> **Task 2933 Bug Log Audit & Verification Notes (Original vs. Updated)**
> 
> * **Preservation of Exact Tested Inputs & Typos:**
>   * **What was previously recorded:** The bug log used generalized or polished input strings.
>   * **What was changed:** Restored the exact, authentic submitted test input including historical transcription variants (such as subject `"accesss issue"` with triple 's') to match the recorded retest payload and screenshot evidence precisely.
> 
> * **Session Attribution & Explicit Timestamps:**
>   * **What was previously recorded:** Test timing and commit references were loosely described.
>   * **What was changed:** Explicitly documented the exact commit hash `880adfa49912bb0e213c11f63ddbf73cd7657cf4` alongside the precise timestamp `2026-10-09 18:51:00 EEST` for the retest session.
> 
> * **Payload Verification & Historical Comparison:**
>   * **What was previously recorded:** The result was noted without structured verification of the JSON response fields.
>   * **What was changed:** Added explicit verification against the response payload evidence confirming ID 24, category `billing`, confidence `0.444`, and priority `normal`. Also explicitly contrasted this with the earlier run on `2026-10-08` which returned `access` at `0.41` confidence.

| Title | Steps to reproduce | Expected | Actual | Severity (high, medium, low) | Evidence | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| Email-update request classified as billing instead of access | 1. Check commit `880adfa49912bb0e213c11f63ddbf73cd7657cf4` on 2026-10-09 18:51:00 EEST.<br>2. Open ticket form.<br>3. Enter subject `"accesss issue"` and description `"How can I update the registered email address on my workspace account?"`.<br>4. Click submit.<br>5. Check created ticket #24 and observe returned AI category in API response and Dashboard. | Create ticket successfully with category "access". | The form submitted successfully. In DevTools Network, `POST /api/tickets` returned HTTP 201 Created with generated ID 24 on commit `880adfa49912bb0e213c11f63ddbf73cd7657cf4` (tested 2026-10-09 18:51:00 EEST). The AI categorized it as billing with 0.444 confidence and normal priority. After reloading the dashboard, ticket #24 remained visible with all data intact. Note: Verified against response payload evidence confirming `{ "category": "billing","confidence": 0.444, "created_at": "2026-10-09T15:51:33.224008+00:00", "description": "How can I update the registered email address on my workspace account?","id": 24,"priority": "normal","subject": "accesss issue"}` An earlier run on 2026-10-08 returned access at 0.41 confidence , Request payload frames and status headers are omitted in capture | Pending triage | ![retest screenshot](evidences/task-2933/vaildaccessonpageretest.png) | Pending coordination |

