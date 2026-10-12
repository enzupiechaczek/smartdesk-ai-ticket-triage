# Day 4 Regression Test Results

Tested on a fresh clone of merged `main` at `57a7fae`, so these results come from the
exact code that was demonstrated, not from an older branch.

## Result summary

| Group | Cases | Passed | Failed |
| --- | --- | --- | --- |
| API validation | 11 | 11 | 0 |
| Priority rule | 13 | 13 | 0 |
| Unsafe input | 4 | 4 | 0 |
| **Total** | **28** | **28** | **0** |

Reopened bugs: **0**. The four previously reclassified findings were retested and all
four are still resolved, so none was reopened.

## Defects found while following the README

These are setup and documentation defects. They are not test-case failures, but they
block a new user, so they are reported here.

| # | Severity | Defect | Effect on a new user |
| --- | --- | --- | --- |
| 1 | High | README step 2 creates the virtual environment at `backend\venv` but then tells you to activate `backend\.venv\Scripts\Activate.ps1` | The activate command fails, the virtual environment stays inactive |
| 2 | High | The README never tells you to run `python ai/train.py` | `/api/health` returns 200 and looks healthy, but the first ticket submission returns HTTP 500 with `RuntimeError: Run python ai/train.py first` |
| 3 | Medium | If the activate step is skipped or fails, `pip install -r requirements.txt` succeeds while installing into the global Python | The virtual environment stays empty and nothing reports the mistake |
| 4 | Low | The README troubleshooting entry for the PowerShell policy suggests `.venv\Scripts\activate.bat`, which is also the wrong path | The suggested fix does not exist; the real path is `backend\venv\Scripts\activate.bat` |

Defect 2 is the serious one. The health check gives false confidence: it answers
`{"service": "SmartDesk local API", "status": "ok"}` while the main feature is broken.

## How the run was performed

- Fresh clone of merged `main` at `57a7fae`, clean working tree, no local model and no
  held-out CSV, because both are git-ignored
- Followed README step 2 to create the virtual environment and install requirements
- Applied the missing training step, then started the app with `python backend/app.py`
- Sent each case to POST /api/tickets and compared the real status and body with the
  Expected column in `tests/test_cases.md`
- Checked the four unsafe-input cases in Chrome, then reloaded the page and re-checked
  the same cards
- Ran the built-in suite from README step 5: 17 tests, all pass
- Training run reported a cross-validation mean of 0.632 (+/- 0.198)

## API validation cases

| Test ID | Status | Result | Detail |
| --- | --- | --- | --- |
| TC-ValidAccess-001 | 201 | Pass | category `access`, ticket id 1 |
| TC-ValidBilling-002 | 201 | Pass | category `billing`, ticket id 2 |
| TC-ValidTechnical-003 | 201 | Pass | category `technical`, ticket id 3 |
| TC-BlankSubject-004 | 400 | Pass | `{ "error": "Subject is required (max 100 characters)" }` |
| TC-BlankDescription-005 | 400 | Pass | `{ "error": "Description is required (max 500 characters)" }` |
| TC-101CharacterSubject-006 | 400 | Pass | `{ "error": "Subject is required (max 100 characters)" }` |
| TC-501CharacterDescription-007 | 400 | Pass | `{ "error": "Description is required (max 500 characters)" }` |
| TC-DuplicateTicket-008 | 201 | Pass | 1st id 4, 2nd id 5; both returned 201 |
| TC-HTMLLikeText-009 | 201 | Pass | tags stored literally, ticket id 6 |
| TC-AmbiguousTicket-010 | 201 | Pass | tags stored literally, ticket id 7 |
| TC-MalformedJson-011 | 400 | Pass | `{ "error": "Request body must be a JSON object" }` |

## Priority rule cases

| Test ID | Status | Priority | Expected | Result |
| --- | --- | --- | --- | --- |
| TC-Priority-012 | 201 | urgent | urgent | Pass |
| TC-Priority-013 | 201 | urgent | urgent | Pass |
| TC-Priority-014 | 201 | normal | normal | Pass |
| TC-Priority-015 | 201 | normal | normal | Pass |
| TC-Priority-016 | 201 | urgent | urgent | Pass |
| TC-Priority-017 | 201 | urgent | urgent | Pass |
| TC-Priority-018 | 201 | urgent | urgent | Pass |
| TC-Priority-019 | 201 | normal | normal | Pass |
| TC-Priority-020 | 201 | normal | normal | Pass |
| TC-Priority-021 | 201 | ordering | urgent submitted first stays above | Pass |
| TC-Priority-022 | 201 | urgent | urgent | Pass |
| TC-Priority-023 | 201 | urgent | urgent | Pass |
| TC-Priority-024 | 201 | urgent | urgent | Pass |

TC-Priority-021 detail: urgent id 20 at position 0; normal id 21 at position 9; urgent submitted first.

## Unsafe input cases

| Test ID | Input | Status | Observed in Chrome after reload | Result |
| --- | --- | --- | --- | --- |
| TC-HTMLBold-001 | `<b>bold</b>` | 201 | Card shows the literal text `<b>bold</b>`. No `b` element created, HTML contains `&lt;`. | Pass |
| TC-Script-002 | `<script>alert(1)</script>` | 201 | Card shows the literal text `<script>alert(1)</script>`. No `script` element created and no alert appeared. | Pass |
| TC-Image-003 | `<img src=x>` | 201 | Card shows the literal text `<img src=x>`. No `img` element created, nothing requested. | Pass |
| TC-Spaces-004 | `spaces only` | 400 | Rejected with `Description is required (max 500 characters)`. The browser form also blocks submit, so no POST is sent from the page. | Pass |

## Screenshots

26 of the 28 cases have a screenshot from this run, named day4-<test-id>.png so they do not
collide with the evidence already in the repository from the earlier merged pull requests. That older
evidence is deliberately left untouched: it belongs to those PRs and is not part of this run.

| Screenshot | Covers |
| --- | --- |
| day4-TC-Priority-013 to 022, 024 | the urgent cards, each showing Priority: urgent |
| day4-TC-Priority-014, 015, 019, 020 | the normal cards, each showing Priority: normal |
| day4-TC-Priority-021 | the dashboard with the urgent cards above the normal ones; the exact ids and positions are in the priority table above |
| day4-TC-ValidAccess-001 to 003 | the valid tickets, 201 with the subject and description unchanged |
| day4-TC-BlankSubject-004, TC-BlankDescription-005, TC-101CharacterSubject-006, TC-501CharacterDescription-007, TC-MalformedJson-011 | the 400 responses with the documented error messages |
| day4-TC-DuplicateTicket-008 | both duplicate cards |
| day4-TC-HTMLLikeText-009 | the card with the literal text <b>Login Problem</b> |
| day4-TC-AmbiguousTicket-010 | the ambiguous ticket, one valid category |
| day4-TC-Script-002, day4-TC-Image-003, day4-TC-HTMLLikeText-009-rendering | the literal tag text after a reload, not rendered |
| day4-TC-Spaces-004 | the rejected spaces-only input |
| day4-dashboard-priority-urgent | the top of the dashboard after the run |

Still missing: **day4-TC-Priority-024** (Production issue / Please investigate). That case is
recorded as Pass in the table above, so only its image is outstanding.
