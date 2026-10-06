# SmartDesk test cases

All inputs below are synthetic. Exercise submissions through `POST /api/tickets` unless noted. For accepted tickets, verify the returned ticket is saved and appears in `GET /api/tickets`. Actual results and evidence remain unfilled until the application exists and cases are run.

| Test ID | Input | Steps | Expected result | Actual result | Pass/Fail | Evidence |
|---|---|---|---|---|---|---|
| B-T01 | Subject: `Cannot sign in`; description: `The password reset link says my account is locked.` | Submit; inspect response and ticket list. | HTTP 201; category `access`; ticket is saved and returned in the list. | Not run (application not yet available). | Not run | Pending execution. |
| B-T02 | Subject: `Unexpected renewal charge`; description: `I was charged twice for this month's subscription.` | Submit; inspect response and ticket list. | HTTP 201; category `billing`; ticket is saved and returned in the list. | Not run (application not yet available). | Not run | Pending execution. |
| B-T03 | Subject: `Dashboard will not load`; description: `The page returns an error after I connect to the office network.` | Submit; inspect response and ticket list. | HTTP 201; category `technical`; ticket is saved and returned in the list. | Not run (application not yet available). | Not run | Pending execution. |
| B-T04 | Subject: `   `; description: `I cannot open the account settings page.` | Submit with a whitespace-only subject. | HTTP 400 with a JSON error message; no ticket is saved. | Not run (application not yet available). | Not run | Pending execution. |
| B-T05 | Subject: `Settings page issue`; description: empty string. | Submit with a blank description. | HTTP 400 with a JSON error message; no ticket is saved. | Not run (application not yet available). | Not run | Pending execution. |
| B-T06 | Subject: exactly 101 `S` characters; description: `I cannot sign in.` | Submit; inspect validation response. | HTTP 400 with a JSON error message because subject exceeds 100 characters; no ticket is saved. | Not run (application not yet available). | Not run | Pending execution. |
| B-T07 | Subject: `Network issue`; description: exactly 501 `D` characters. | Submit; inspect validation response. | HTTP 400 with a JSON error message because description exceeds 500 characters; no ticket is saved. | Not run (application not yet available). | Not run | Pending execution. |
| B-T08 | Submit twice: Subject `Cannot access invoice`; description `The invoice page is unavailable.` | Submit the same payload twice; inspect responses and ticket list. | Both submissions are handled without a server error; each creates a saved ticket (two records) unless duplicate suppression is explicitly added to the contract. | Not run (application not yet available). | Not run | Pending execution. |
| B-T09 | Subject: `Formatting check`; description: `Please display <b>test</b> literally in my account notes.` | Submit; inspect response, saved value, and rendered ticket card. | HTTP 201; literal text is retained and rendered as text, not interpreted as markup; category is one supported label. | Not run (application not yet available). | Not run | Pending execution. |
| B-T10 | Subject: `It stopped working`; description: `Sometimes I see a charge and sometimes the screen freezes. I am not sure what happened.` | Submit; inspect response category and confidence. | HTTP 201; returns one supported category (`access`, `billing`, or `technical`) with confidence 0.0–1.0; record for manual ambiguity review without asserting a predetermined label. | Not run (application not yet available). | Not run | Pending execution. |

## Notes for execution

- `docs/architecture.md` specifies HTTP 201 for accepted tickets and HTTP 400 with `{"error":"message"}` for invalid requests.
- The 100-character subject and 500-character description limits are expectations from this assignment; confirm them with Group A1 before treating them as implemented contract.
- No duplicate suppression behavior is documented. The current expectation is that each valid submission creates a ticket; confirm with Group A1.
