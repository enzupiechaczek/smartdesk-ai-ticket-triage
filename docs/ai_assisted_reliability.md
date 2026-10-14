# AI-assisted API reliability improvement

## Status and attribution

Implementation awaiting validation and Enzu's final code review; not a completed or merged result. Baseline: main commit `ffff8ecef5a05bc0fc78a7a7603f9c9e7fd1e76f` on 2026-10-14. SmartDesk's original application was built by EARTech interns under Enzu's instruction. This follow-up is not sole authorship of their original work.

Enzu selected the reliability scope and approved branch-only commits. Perplexity inspected source and drafted code, tests, workflow and this document. Final human code review, actual runtime validation and merge remain pending. Approving a proposed write is not evidence of line-by-line review or successful tests.

Implementation commits:

- `29c306ea57a6e555c55afb7e0acca0f4539c9f0d`: missing-model handling and explicit database connection closure.
- `4af46abaa13cf9b579480f3d5a69690df0457ba5`: isolated API tests and model-loading boundary tests.

## Source-inspected problem

The baseline predictor raises RuntimeError when the model file is missing. The valid-ticket API path does not handle that condition. Its success-path test calls the real predictor and depends on a locally generated model. The baseline API suite shares one temporary database. These are source observations; a fresh baseline runtime reproduction has not been recorded for this improvement.

## Changes and engineering decisions

- ModelUnavailableError distinguishes missing model files, including a file disappearing between the existence check and loading. It remains a RuntimeError subclass for compatibility.
- The API catches only that exception and returns JSON 503 with training instructions before insertion. Existing invalid-input 400 and successful-create 201 behavior is retained by design and awaits verification.
- Unexpected prediction/loading faults are not broadly swallowed. Corrupt-model recovery and full readiness checks are outside scope.
- API tests mock prediction at the application boundary, use a new temporary database per test and restore patched state during cleanup. Application import is prevented from initializing a development database in this test module.
- Tests check persisted response fields, repeated GET retrieval, duplicate IDs, priority/whitespace handling, safe missing-model errors, and failure without insertion. Repeated GET is not a browser-refresh test.
- Database operations explicitly close connections after reads or transaction completion; write transactions still commit on success and roll back on errors.
- CI runs backend, evaluator and predictor-boundary tests without model training. It uses contents: read, a ten-minute timeout and no application secrets. It checks that model/development-database artifacts are absent.

## Verification plan

Use a clean checkout and an isolated environment with backend/requirements.txt installed. From the repository root:

```text
python -m unittest discover -s backend -p "test_*.py" -v
python -m unittest discover -s tests -p "test_evaluate_heldout.py" -v
python -m unittest discover -s tests -p "test_predictor_availability.py" -v
```

Proposed contract for a valid submission with a missing model:

```text
503 {"error": "Model not trained. Run python ai/train.py"}
```

Invalid input must still be rejected before prediction. Successful creation must return 201 and a matching stored record. Health behavior is unchanged: it checks model-file existence, not model loading or database readiness.

For baseline comparison use a separate checkout of ffff8ec, preserving development data. Record actual commands, dates/timezone, Python/dependency versions, tested commit, exit status and genuine outputs. Never reconstruct unsaved results. CI records its checkout SHA, UTC time and environment; a PR CI run may test GitHub's synthetic merge commit rather than the branch head. Record both identifiers accurately.

## Evidence ledger

| Item | Status |
| --- | --- |
| Source inspection | Completed by assistant against identified baseline |
| Fresh baseline runtime reproduction | Pending |
| Implementation and tests | Committed on feature branch; not merged |
| Local runtime execution | Pending; no passing test count claimed |
| CI run URL, tested SHA and outcomes | Pending until actual execution |
| Enzu review findings and requested corrections | Pending |
| Manual browser checks with/without a model | Pending; mocks do not prove browser behavior |
| PR link and final merge commit | Pending |

Update this ledger with actual evidence before presenting completed outcomes in a job application. A failed CI run is evidence to investigate, not a result to omit.

## AI direction and human oversight

Prompt summary: Enzu requested an inspectable example of an AI tool improving SmartDesk. The assistant proposed graceful missing-model handling, isolated tests, CI and an evidence document. Enzu authorized the scope, branch and reviewed write confirmations. The assistant avoided broad RuntimeError handling and claims that mocked API tests establish model accuracy.

A first commit-confirmation preview was incomplete. The assistant withdrew that proposal without committing it and reissued smaller exact-content confirmations. Record this as a process correction, not a code-test result. Add Enzu's actual code-review decisions here after review; do not invent rejected suggestions, time savings or final approval.

## Limitations

Prediction is mocked in API-contract tests. Model-boundary tests mock file/loading behavior; they do not evaluate a trained model. Backend dependency versions remain unpinned as in existing requirements, so this workflow is not a locked environment. Action versions use major-version tags, not immutable commit pins. CI currently proposes Ubuntu/Python 3.12 only; Windows execution is not established.

No production readiness, accuracy gain, retraining or complete browser E2E success is claimed. Historical model metrics and deferred A2/Group B follow-ups remain separate. No models, databases, private evaluation CSVs, secrets or real customer data belong in this PR or its evidence.
