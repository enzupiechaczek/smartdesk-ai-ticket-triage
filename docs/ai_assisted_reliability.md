# AI-assisted API reliability improvement

## Outcome and attribution

This is my scoped AI-assisted improvement to SmartDesk. I directed the work, manually reviewed the implementation, questioned the exception-handling boundary and completed browser verification. Perplexity inspected source and drafted the changes under my direction. The original application remains attributed to the EARTech interns who built it under my instruction.

Human review and scoped browser verification are complete, and recorded CI jobs passed. Final documentation CI/readiness/merge are still pending; no merged result is claimed here. [PR #54](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/54) is the delivery record.

Baseline: `ffff8ecef5a05bc0fc78a7a7603f9c9e7fd1e76f`. Manually reviewed/tested revision: `0b4d29df7bca548b4cf48472ef1ac9c3f45d72df`. Later evidence-only commits must not be relabelled as the revision I tested.

## Problem and implementation

Source inspection found an unhandled missing-model RuntimeError in the valid-ticket path and API tests that depended on a locally trained artifact. A fresh baseline runtime comparison was not performed.

- ModelUnavailableError distinguishes missing model files and remains a RuntimeError subclass for compatibility.
- Valid submissions with that known condition return an actionable JSON 503 before insertion; validation retains its 400 contract and successful creation its 201 contract.
- Unexpected loading/prediction errors are not broadly caught.
- Database operations explicitly close connections after reads or transaction completion.
- API tests use mocked prediction and a fresh temporary database per test, checking stored fields, duplicate IDs, priority/whitespace and failure without insertion.
- Predictor tests cover missing/disappearing files and propagation of unrelated loading faults.
- Read-only-permissions CI runs backend, evaluator and predictor tests without training or generating model/development-database artifacts.

Implementation commits: `29c306ea57a6e555c55afb7e0acca0f4539c9f0d` (production changes), `4af46abaa13cf9b579480f3d5a69690df0457ba5` (tests), `22246e62bb59330a62c285eeadec3b667bcc195a` (workflow/case-study draft), and `0b4d29df7bca548b4cf48472ef1ac9c3f45d72df` (initial evidence record).

## My human review decision

On 2026-10-14 I confirmed that my manual code review was complete and the changes looked correct. My specific remaining question was whether unexpected faults in ai/predictor.py were broadly swallowed. I requested a double-check of the predictor, regression tests and API caller.

The double-check found only FileNotFoundError around joblib.load is translated to ModelUnavailableError; the API catches only that specific subclass. Prediction/result processing is outside the loading try block. There is no broad Exception/RuntimeError handler, fabricated prediction or silent fallback. I accepted the explanation and confirmed my questions were resolved.

Qualification accepted for this scope: any FileNotFoundError raised inside joblib.load is classified as model unavailability, not necessarily only disappearance of the top-level file. Corrupt-model recovery/full readiness remain outside scope. This is my actual review decision, not a claim that I independently injected every possible fault.

## My browser verification and screenshots

I used a separate clone, smartdesk-pr54-manual, at the full reviewed revision above, with a separate environment and server on 127.0.0.1:5054. The checkout screenshot records `2026-10-14T15:21:29.8781017+02:00`. Browser: Microsoft Edge/InPrivate; exact browser/Python/package versions were not captured in these images.

[All five original screenshots are attached in my GitHub evidence comment](https://github.com/enzupiechaczek/smartdesk-ai-ticket-triage/pull/54#issuecomment-6169879789), posted on 2026-10-14 at 13:47:57 UTC. They are GitHub comment attachments, not committed binary files.

| Scenario | Observed result and evidence boundary |
| --- | --- |
| Missing model | Subject PR54 missing-model check; description Synthetic test of controlled model-unavailable handling. Screenshot shows the actionable page message and POST 503. I reported completing the checks as expected, including no saved ticket. Complete error JSON and an empty API listing are not separately displayed in the screenshot set. |
| Model present | After training in the separate test copy, I submitted PR54 successful persistence check / Synthetic test after training the local model. Screenshots show Network 201, saved message and matching dashboard text, technical at displayed 54% confidence, normal priority. This is not an accuracy benchmark. |
| Real refresh | I pressed browser refresh and confirmed the ticket remained. Screenshot shows the retained ticket and a new tickets fetch returning 200. This is a browser observation, not repeated automated test-client GET calls. |
| API value matching | I reported the prescribed API-record/value checks worked as expected. The supplied images do not display the ticket ID/full JSON, so these remain tester-reported observations, not screenshot-transcribed values. |

Screenshot inventory: Screenshot-2026-10-14-152150.jpg (checkout/version), error-3.jpg (missing-model), pr54-success-response-4.jpg (201), ticket-dashboard-success-2.jpg (ticket details), refresh-success-5.jpg (refresh). GitHub attachment display names may omit filename suffixes.

The missing-model screenshot includes Unexpected token '|'. I confirmed that I accidentally entered text into DevTools Console. This was a tester-input mistake, not a SmartDesk defect. The original evidence and explanation are retained.

## Automated evidence

[CI status record](evidence/pr54/ci-status.md) preserves both successful jobs, branch revisions and UTC timestamps. GitHub check conclusions were verified; exact counts, installed versions and executed synthetic merge SHA were not retrieved from logs and are not claimed.

Commands:

```text
python -m unittest discover -s backend -p "test_*.py" -v
python -m unittest discover -s tests -p "test_evaluate_heldout.py" -v
python -m unittest discover -s tests -p "test_predictor_availability.py" -v
```

## Evidence ledger

| Item | Status |
| --- | --- |
| Source inspection and implementation | Complete, with identified baseline and commits |
| My manual code review | Complete; exception-boundary question resolved |
| Scoped browser verification | Complete, with screenshot-visible/tester-reported distinctions |
| Screenshot availability | Five attachments verified in the linked GitHub comment |
| CI aggregate outcome | Two successful jobs recorded for 22246e6 and 0b4d29d |
| Exact CI counts/environment/execution SHA | Not captured; optional precision, not claimed |
| Fresh baseline runtime comparison | Not performed; scope limitation, not a fabricated before/after result |
| Final documentation CI, readiness and merge | Pending; use PR status and eventual merge commit |

## Limitations and AI oversight

Mocked tests prove contracts/storage, not model accuracy. Health is a file-existence check, not full readiness. Dependencies are unpinned; Actions use major-version tags; CI covers Ubuntu/Python 3.12. My Windows browser session is separately recorded, not a Windows automated-suite result. I trained only the separate test copy; no accuracy gain or production readiness is claimed. Historical model metrics and deferred A2/Group B requirements remain separate.

The AI workflow included source inspection, proposed scope, branch-only confirmations, implementation, CI and my review/testing. An incomplete first confirmation preview was withdrawn without a commit and replaced by exact-content confirmations. That was a process correction, not a test result. No invented time savings, authorship claims, hidden ticket values or unobserved tests belong in the portfolio.
