# Day 4 Regression Test Results

## 1. Run provenance

| Item | Value |
| --- | --- |
| Run date | 2026-10-12, 02:26 to 02:40 local for the main run, 06:00 to 06:05 for the evidence reruns |
| Platform | Microsoft Windows 11 Pro 10.0.26200, PowerShell 5.1 |
| Python | 3.14.8, virtual environment at `backend\venv` inside the clone |
| Tested commit | `57a7fae65a7e8df9ec2fb35a131291ff93c6ddb9`, "Merge pull request #39" |
| Tested tree | `464d4c2c05097043baf739580dc761c0c1069ed9`, 79 files |
| Report branch | `b-username123212312-day4-regression` |

### 1.1 How the tested tree was compared with GitHub main

`git clone` from the GitHub URL failed on this network. The disclosed error was:

```
error: RPC failed; curl 56 Recv failure: Connection was reset
fatal: early EOF
fatal: fetch-pack: invalid index-pack output
```

It was retried with `--depth 1` and with `--filter=blob:none` and failed the same way. A control
clone of a small unrelated repository completed in 2 seconds, so the network was up; transfers above
roughly 120 KB were being reset.

The fresh clone was therefore taken from the local repository, which already had `origin/main`
fetched from GitHub. The comparison that establishes equivalence:

```
$ git rev-parse 57a7fae^{tree}
464d4c2c05097043baf739580dc761c0c1069ed9
$ git rev-parse origin/main^{tree}
464d4c2c05097043baf739580dc761c0c1069ed9
$ git ls-tree -r 57a7fae
$ git ls-tree -r origin/main
$ compare both listings
file-by-file listing IDENTICAL, 79 entries
```

The trees are identical and the 79-entry listing matches line for line, so the tested code is
byte-for-byte the code on GitHub `main`.

### 1.2 What this does and does not establish

It establishes that the tested code equals merged `main` at `57a7fae`.

An earlier draft of this report claimed the tested code was "the exact code that was demonstrated".
That claim is **withdrawn**. No demo commit is recorded anywhere in the repository, so the tested SHA
is the only defensible reference point and no demonstration version can be asserted.

## 2. Commands, in the order they were run

### Stage A, README only, on a clean clone

```
$ git clone --depth 1 --single-branch --branch main <url> smartdesk-fresh-clone
error: RPC failed; curl 56 Recv failure: Connection was reset

$ python -m venv .\backend\venv
exit 0, creates backend\venv

$ . .\backend\.venv\Scripts\Activate.ps1
The term '.\backend\.venv\Scripts\Activate.ps1' is not recognized as the name of a cmdlet,
function, script file, or operable program.

$ pip install -r .\backend\requirements.txt
Requirement already satisfied: flask-3.1.3 in
  C:\Users\youse\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages
exit 0
```

`backend\venv\Lib\site-packages` contained 0 packages after that command.

**Stage A did not succeed.** The three failures are findings D1 to D3 in section 4.

### Stage B, corrections applied

```
$ .\backend\venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt
Successfully installed blinker-1.9.0 click-8.5.0 cloudpickle-3.1.2 flask-3.1.3
  itsdangerous-2.2.0 jinja2-3.1.6 joblib-1.6.0 markupsafe-3.0.4 narwhals-2.27.1
  numpy-2.5.4 scikit-learn-1.9.1 scipy-1.18.1 threadpoolctl-3.7.0 werkzeug-3.1.9

# Windows Application Control blocked the numpy, scipy and scikit-learn extension DLLs.
$ .\backend\venv\Scripts\python.exe -m pip install --force-reinstall --no-cache-dir numpy
$ .\backend\venv\Scripts\python.exe -m pip install --force-reinstall --no-cache-dir scipy
$ .\backend\venv\Scripts\python.exe -m pip install --force-reinstall --no-cache-dir scikit-learn
# after each, the corresponding import succeeded

$ .\backend\venv\Scripts\python.exe ai\train.py
Cross-validation accuracy per fold: [0.875, 0.429, 0.429, 0.857, 0.571]
Cross-validation mean accuracy: 0.632 (+/- 0.198)
Saved model.joblib

$ .\backend\venv\Scripts\python.exe backend\app.py
Running on http://127.0.0.1:5000
```

The training step is **not** in the README. Without it the health check still answers 200 while the
first ticket submission fails:

```
$ GET /api/health
200  {"service": "SmartDesk local API", "status": "ok"}

$ POST /api/tickets  {"subject":"Login broken","description":"I cannot access my account"}
500
RuntimeError: Run python ai/train.py first          # ai/predictor.py line 13
```

### Stage C, the regression run, after the corrections

This is the stage the 28 results come from. Because Stage A failed, **these 28 passes do not show
that first-time setup works from the README as written.**

## 3. Built-in test suite

```
$ .\backend\venv\Scripts\python.exe -m unittest discover -s backend -p "test_*.py" -v
test_blank_or_too_long_description_is_rejected ... ok
test_blank_or_too_long_subject_is_rejected ... ok
test_body_must_be_a_json_object ... ok
test_description_must_be_a_string ... ok
test_missing_description_is_rejected ... ok
test_missing_or_invalid_json_is_rejected ... ok
test_missing_subject_is_rejected ... ok
test_null_body_is_rejected ... ok
test_rejected_tickets_are_not_saved ... ok
test_subject_must_be_a_string ... ok
test_valid_ticket_is_created ... ok
test_documented_examples ... ok
test_down_as_a_whole_word_is_urgent ... ok
test_download_does_not_trigger_down ... ok
test_every_urgent_phrase_matches ... ok
test_no_phrase_is_normal ... ok
test_phrase_in_subject_only_is_urgent ... ok
----------------------------------------------------------------------
Ran 17 tests in 1.650s

OK
exit status: 0
```

The same run also printed, during `backend/test_api.py`:

```
ResourceWarning: unclosed database in <sqlite3.Connection object at 0x000001D3BED924D0>
```

That is a new low-severity finding, D5.

## 4. Findings, proposed for triage

Severity below is **proposed**, not agreed. Ownership is **pending**. These are new findings. They are
separate from the historical statement in `tests/bug_log.md` that no open bugs were carried forward
after an earlier reclassification, and they have not been triaged.

| ID | Proposed severity | Finding | README or test command | Observed output |
| --- | --- | --- | --- | --- |
| D1 | High | README creates the venv at `backend\venv` but tells you to activate `backend\.venv` | `. .\backend\.venv\Scripts\Activate.ps1` | `is not recognized as the name of a cmdlet` |
| D2 | High | README never says to run `python ai/train.py` | `python backend/app.py`, then submit a ticket | health returns 200 `"status": "ok"`, first POST returns HTTP 500, `RuntimeError: Run python ai/train.py first` |
| D3 | Medium | After the failed activation, `pip install -r requirements.txt` exits 0 while installing into the global interpreter | `pip install -r .\backend\requirements.txt` | `Requirement already satisfied ... in C:\Users\youse\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages`, while `backend\venv\Lib\site-packages` held 0 packages |
| D4 | Low | The PowerShell troubleshooting note gives the wrong path too | `.venv\Scripts\activate.bat` | that path does not exist; the real one is `backend\venv\Scripts\activate.bat` |
| D5 | Low | `backend/test_api.py` leaves a sqlite connection open | `python -m unittest discover -s backend` | `ResourceWarning: unclosed database in <sqlite3.Connection object>` |
| D6 | Medium | `tests/test_cases.md` states that browser validation blocked the spaces-only ticket and that no POST was sent. Observed on this fresh clone, the browser does send the POST and the server rejects it with 400. The recorded cause is wrong | `tests/test_cases.md`, TC-Spaces-004, Actual result column | see section 7.2 |

**D3 is a consequence of D1**, not an independent fault in pip. It is listed separately because a
silent install into the global interpreter is its own hazard once activation has failed. The
interpreter that ran the failing `pip install` was the global one at
`C:\Users\youse\AppData\Local\Python\pythoncore-3.14-64`, not the clone's venv.

D1, D2 and D4 are README defects. D5 is test-code. D6 is a test-documentation defect. All of these
should be coordinated with Hassan's startup work in PR #44 rather than duplicated, and nothing here
overwrites a fix that has landed there. **This branch changes no README, no test code and no
application code**; it only adds a report and evidence.

## 5. API contract evidence

Every request and every full response is in
[day4-api-evidence.md](evidences/day4-api-evidence.md). That file contains the 24 main-run cases with
their full request bodies and full response bodies, plus fresh reruns of the four unsafe-input cases,
of TC-Priority-021 and of TC-DuplicateTicket-008.

| Case | HTTP | Category | Confidence | Priority | Result |
| --- | --- | --- | --- | --- | --- |
| TC-ValidAccess-001 | 201 | access | 0.768 | normal | Pass |
| TC-ValidBilling-002 | 201 | billing | 0.642 | normal | Pass |
| TC-ValidTechnical-003 | 201 | technical | 0.661 | normal | Pass |
| TC-BlankSubject-004 | 400 | - | - | - | Pass |
| TC-BlankDescription-005 | 400 | - | - | - | Pass |
| TC-101CharacterSubject-006 | 400 | - | - | - | Pass |
| TC-501CharacterDescription-007 | 400 | - | - | - | Pass |
| TC-DuplicateTicket-008 | 201, 201 | access, access | 0.785, 0.785 | normal | Pass |
| TC-HTMLLikeText-009 | 201 | access | 0.69 | normal | Pass |
| TC-AmbiguousTicket-010 | 201 | access | 0.51 | normal | Pass |
| TC-MalformedJson-011 | 400 | - | - | - | Pass |

### TC-AmbiguousTicket-010

The input is `{"subject":"Help needed","description":"i need help"}`. An earlier draft of this report
described this case as "tags stored literally", which was text copied from TC-HTMLLikeText-009 and
does not describe this input at all. The actual observation:

```
HTTP 201
{
  "category": "access",
  "confidence": 0.51,
  "created_at": "...",
  "description": "i need help",
  "id": 7,
  "priority": "normal",
  "subject": "Help needed"
}
```

Contract checks: 201; subject returned unchanged as `Help needed`; description returned unchanged as
`i need help`; `access` is one of the three valid categories; confidence 0.51 is between 0 and 1;
priority is one of the two valid values; `created_at` present. There is no tag handling in this case.

## 6. Priority rule results

| Case | HTTP | Priority returned | Expected | Result |
| --- | --- | --- | --- | --- |
| TC-Priority-012 | 201 | urgent | urgent | Pass |
| TC-Priority-013 | 201 | urgent | urgent, capital DOWN | Pass |
| TC-Priority-014 | 201 | normal | normal, download is not down | Pass |
| TC-Priority-015 | 201 | normal | normal | Pass |
| TC-Priority-016 | 201 | urgent | urgent, phrase in subject only | Pass |
| TC-Priority-017 | 201 | urgent | urgent, phrase in description only | Pass |
| TC-Priority-018 | 201 | urgent | urgent | Pass |
| TC-Priority-019 | 201 | normal | normal, breakdown is not down | Pass |
| TC-Priority-020 | 201 | normal | normal | Pass |
| TC-Priority-022 | 201 | urgent | urgent, phrase in description only | Pass |
| TC-Priority-023 | 201 | urgent | urgent, phrase in description only | Pass |
| TC-Priority-024 | 201 | urgent | urgent, phrase in subject only | Pass |

### TC-Priority-021, ordering

The case submits the urgent ticket TC-Priority-013 first, then the normal ticket TC-Priority-015,
then reads `GET /api/tickets`. The database was emptied first, so this rerun produced its own ids.

| Ticket | id | created_at | priority | position in GET |
| --- | --- | --- | --- | --- |
| Server DOWN, urgent, submitted first | 25 | 2026-10-12T03:00:21.738225+00:00 | urgent | 0 |
| Printer issue, normal, submitted second | 26 | 2026-10-12T03:00:21.751422+00:00 | normal | 6 |

Both creation timestamps are 13 ms apart and the urgent ticket is the older of the two. After
reloading the dashboard in Chrome the same order was still shown, with `Server DOWN` at position 0 and
`Printer issue` at position 6 of 7 cards. Ordering therefore does not follow creation order alone.
**Pass.**

Full requests, responses, the complete `GET /api/tickets` listing and the reload positions are in
[day4-api-evidence.md](evidences/day4-api-evidence.md).

## 7. Unsafe input

### 7.1 Rendering and network observations

These were taken from Chrome against the running app, with the DOM and the network log as the
evidence rather than an image alone.

| Case | Input | API | DOM observation | Network observation |
| --- | --- | --- | --- | --- |
| TC-HTMLBold-001 | `<b>bold</b>` | 201, stored literal | card found, no `b` element inside it, card HTML contains `&lt;b` | not applicable, a bold tag references no URL |
| TC-Script-002 | `<script>alert(1)</script>` | 201, stored literal | card found, no `script` element inside it, card HTML contains `&lt;script`, no alert fired | page loaded with 1 script request, `app.js`, which is the app's own script and not ticket content |
| TC-Image-003 | `<img src=x>` | 201, stored literal | card found, no `img` element inside it, card HTML contains `&lt;img` | **0 requests of type image, 0 requests addressed to `x`** |
| TC-Spaces-004 | `" "` | 400 `Description is required (max 500 characters)` | no card created | see 7.2 |

The complete request log for the page containing the image ticket was:

```
document    304  http://127.0.0.1:5000/
stylesheet  304  http://127.0.0.1:5000/styles.css
script      304  http://127.0.0.1:5000/app.js
fetch       200  http://127.0.0.1:5000/api/tickets
fetch       400  http://127.0.0.1:5000/api/tickets
```

Five requests in total, none of type `image`, none addressed to `x`, and the only script request is
the app's own `app.js`. All three unsafe-input cards were on the page when this log was taken. The
claim that nothing is requested for the image is therefore backed by the network log, not inferred
from the rendered text.

### 7.2 TC-Spaces-004, and the correction behind D6

`tests/test_cases.md` records for this case: "Browser validation blocked submission; no POST sent."
Observed on this fresh clone, that is **not** what happens for a single space.

`frontend/index.html` marks both fields `required`, and `required` in HTML is satisfied by any
non-empty string, including a space. Measured in the browser:

| Scenario | `textarea.checkValidity()` | POST sent | Result |
| --- | --- | --- | --- |
| Description is `" "`, subject filled | `true` | **yes, 1 request** | server returned 400, page showed `Description is required (max 500 characters)`, no card created |
| Description is `" "`, subject left empty | `false` for the form | no | HTML5 `required` blocked the submit, 0 requests |

So the browser does block submission when a field is genuinely empty, but it does **not** block a
spaces-only description. The request is sent and the server rejects it. The rejection behaviour the
case is about is correct and the case passes; what is wrong is the recorded cause.

The API 400 and the browser behaviour are reported here as two separate observations. The 400 came
from sending the body straight to the API with a request tool; the browser behaviour above came from
clicking Submit on the form. Neither is used as evidence for the other.

## 8. Evidence coverage for all 28 cases

Complete means the case has its own recorded evidence of its own input and its own result. Every one
of the 28 cases has a full request and a full response recorded in
[day4-api-evidence.md](evidences/day4-api-evidence.md).

| Case | Result | Image | Other evidence | State |
| --- | --- | --- | --- | --- |
| TC-ValidAccess-001 | Pass | `day4-TC-ValidAccess-001.png` | full response | Complete |
| TC-ValidBilling-002 | Pass | `day4-TC-ValidBilling-002.png` | full response | Complete |
| TC-ValidTechnical-003 | Pass | `day4-TC-ValidTechnical-003.png` | full response | Complete |
| TC-BlankSubject-004 | Pass | `day4-TC-BlankSubject-004.png` | full response | Complete |
| TC-BlankDescription-005 | Pass | `day4-TC-BlankDescription-005.png` | full response | Complete |
| TC-101CharacterSubject-006 | Pass | `day4-TC-101CharacterSubject-006.png` | full response | Complete |
| TC-501CharacterDescription-007 | Pass | `day4-TC-501CharacterDescription-007.png` | full response | Complete |
| TC-DuplicateTicket-008 | Pass | `day4-TC-DuplicateTicket-008.png` | both responses and the stored pair | Complete |
| TC-HTMLLikeText-009 | Pass | `day4-TC-HTMLLikeText-009.png`, `day4-TC-HTMLLikeText-009-rendering.png` | full response, DOM check | Complete |
| TC-AmbiguousTicket-010 | Pass | `day4-TC-AmbiguousTicket-010.png` | full response | Complete |
| TC-MalformedJson-011 | Pass | `day4-TC-MalformedJson-011.png` | full response | Complete |
| TC-Priority-012 | Pass | `day4-TC-Priority-012.png` | full response | Complete |
| TC-Priority-013 | Pass | `day4-TC-Priority-013.png` | full response | Complete |
| TC-Priority-014 | Pass | `day4-TC-Priority-014.png` | full response | Complete |
| TC-Priority-015 | Pass | `day4-TC-Priority-015.png` | full response | Complete |
| TC-Priority-016 | Pass | `day4-TC-Priority-016.png` | full response | Complete |
| TC-Priority-017 | Pass | `day4-TC-Priority-017.png` | full response | Complete |
| TC-Priority-018 | Pass | `day4-TC-Priority-018.png` | full response | Complete |
| TC-Priority-019 | Pass | `day4-TC-Priority-019.png` | full response | Complete |
| TC-Priority-020 | Pass | `day4-TC-Priority-020.png` | full response | Complete |
| TC-Priority-021 | Pass | `day4-TC-Priority-021.png` | both timestamps, full GET listing, reload positions | Complete |
| TC-Priority-022 | Pass | `day4-TC-Priority-022.png` | full response | Complete |
| TC-Priority-023 | Pass | `day4-TC-Priority-023.png` | full response | Complete |
| TC-Priority-024 | Pass | **none** | full response, HTTP 201 priority urgent | Complete on response, image missing |
| TC-HTMLBold-001 | Pass | **none** | full response, DOM check, 0 network requests | Complete on DOM and response, image missing |
| TC-Script-002 | Pass | `day4-TC-Script-002.png` | full response, no `script` element, no alert | Complete |
| TC-Image-003 | Pass | `day4-TC-Image-003.png` | full response, no `img` element, 0 image requests | Complete |
| TC-Spaces-004 | Pass | `day4-TC-Spaces-004.png` | full 400 response, browser network measurement | Complete |

26 cases are complete on their own evidence. Two, TC-Priority-024 and TC-HTMLBold-001, lack an image
but both have a full recorded response, and TC-HTMLBold-001 also has a direct DOM and network
measurement.

`day4-dashboard-priority-urgent.png` shows the top of the dashboard after the main run. It is a
general view and is not counted as the evidence for any single case.

The evidence already in the repository from the earlier merged pull requests is untouched. All new
files carry the `day4-` prefix so they sit alongside that evidence rather than replacing it.

## 9. Historical findings retested

`tests/bug_log.md` records no open bugs and lists four earlier findings that were
**reclassified**, not fixed. Reclassified means the original report was wrong about the cause. It does
not mean a code fault was repaired and closed. All four were retested here.

| Reclassified finding | Original claim | Fresh-clone observation | Now |
| --- | --- | --- | --- |
| TC-ValidAccess-001 | Unexpected category | 201, category `access`, confidence 0.768 | Still reclassified |
| TC-ValidBilling-002 | Unexpected category | 201, category `billing`, confidence 0.642 | Still reclassified |
| TC-101CharacterSubject-006 | Wrong error message | 400 `Subject is required (max 100 characters)`, matches the README contract | Still reclassified |
| TC-501CharacterDescription-007 | Wrong error message | 400 `Description is required (max 500 characters)`, matches the README contract | Still reclassified |

No historical finding is reopened. The six findings in section 4 are new and separate, and have not
been triaged.

## 10. Model quality, not a pass or fail condition

The training run reported a cross-validation mean of 0.632 (+/- 0.198). `docs/model_evaluation.md`
reports 0.625 for the 20% test split, which holds only 8 tickets, and names the cross-validation
figure the more reliable one.

TC-Script-002 was predicted `technical`. No expected category was ever agreed for that input, so this
is recorded as an observation only and is **not** called a misclassification. Whether `technical` is
the right category for a script-input ticket is a question for the model owners.

## 11. Task

**2941, Run the full regression test from a fresh clone of main.**

The branch description originally listed 2934, which is the unsafe-input subset. That is a subset of
this work rather than the whole of it: the four unsafe-input cases are included here, alongside the
other 24, so all 28 cases are covered under 2941. 2934 remains covered by this run and needs no
separate work.

## 12. Summary

- 28 cases: 28 pass, 0 fail.
- 4 historical findings retested, all four still reclassified, none reopened.
- 6 new findings, severity proposed and ownership pending, for coordination with PR #44. D2 is the
  one that blocks a new user: the README never says to train the model, and `/api/health` still
  reports 200 while every ticket submission fails.
- Evidence: 26 cases complete on their own evidence, 2 missing an image only, every case has a full
  recorded request and response.
- The 28 passes come from Stage C, after corrections. Stage A, the README exactly as written, did
  not succeed.
