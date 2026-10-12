# Test Evidence: built-in unit tests

Date: 12/10/2026 (DD/MM/YYYY), no-model run logged at 22:28 (UTC+07:00)
Checkout: working folder `smartdesk-ai-ticket-triage` (not a disposable clone)
Commit: 853ac6b4913676afa7156c6b2486d962533348d1(recorded at the time of testing, was not added when file was edited later)
OS: Windows 11 (build number not recorded), PowerShell
Python: 3.14 (patch version not recorded). The traceback shows the global
`Python314` install, so no `.venv` was active for this run.

This file is separate from `startupevidence.md`, which records the manual
startup session at commit 3030606. Nothing there covers these test runs.

## What was checked

The top-level `sys.exit(1)` model guard in `backend/app.py` had been removed
by a pulled commit. This file records whether the tests can still be
imported and discovered without a generated model.

Command (both runs):

```
python -m unittest discover -s backend -p "test_*.py" -v
```

## Run 1: no model (`ai/model.joblib` absent)

The tester reported that no model had been generated. A `Test-Path` check was
not recorded.

Result:

```
Ran 17 tests in 0.072s

FAILED (failures=1)
```

- Discovery and import: worked. All 17 tests were found and run, with no
  `SystemExit` or import error.
- Passed: 16 tests (all of `test_priority` and all of
  `CreateTicketValidationTests` except one).
- Failed: `test_api.CreateTicketValidationTests.test_valid_ticket_is_created`

  ```
  AssertionError: 500 != 201
  ```

  Cause, from the logged traceback: `create_ticket` (`backend/app.py`, line 63)
  calls `predict_category` (`ai/predictor.py`, line 13), which raises
  `RuntimeError("Run python ai/train.py first")` when there is no model.

Conclusion: the tests can be imported and discovered without a model. One
test needs a trained model at runtime, which is expected because creating a
ticket runs the classifier. No model was committed.

## Run 2: trained model

Same checkout, same test command, run after the no-model run. The `ai/train.py`
output, a `Test-Path` check for the model and the exit code were not recorded.
The previously failing test passing indicates a model was available.

Result:

```
Ran 17 tests in 1.718s

OK
```

- All 17 tests passed, including
  `test_valid_ticket_is_created`, which returned 500 in Run 1.
- The run printed `ResourceWarning: unclosed database in <sqlite3.Connection
...>` three times (once in `test_blank_or_too_long_description_is_rejected`
  and twice in `test_valid_ticket_is_created`). These are warnings, not
  failures, and suggest SQLite connections are not being closed. Not
  investigated or changed here.

Still to record:

- `git status --short` and `git check-ignore -v ai/model.joblib`, to show the
  model is ignored and not committed

## Observation, pending team decision

Without a model, `POST /api/tickets` returns HTTP 500 with a logged traceback,
while `GET /api/health` returns HTTP 503 with a clear message. Whether
ticket creation should also return a clean 503 is an API behaviour question
and has not been decided or changed here.

## Not tested

- macOS
- Native Linux and WSL (this file covers Windows only)
